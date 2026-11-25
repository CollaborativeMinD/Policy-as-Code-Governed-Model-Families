"""Exercise the same model and publication entry points used outside the bundle."""
import importlib.util
import json
import os
from pathlib import Path
import secrets
import sys
import tempfile
import unittest
from unittest.mock import patch

from model_policy_engine import store
from model_policy_engine.policy_loader import PolicyPayloadError, PolicySecurityError
from model_policy_engine.schema import TEMPLATES, catalog

MODELS = Path(__file__).resolve().parents[2] / "model_families"
RECOVERY = "hardware_viability/recovery_time_inflation"
OTHER = "space-and-comms/volley_successor"
SEARCH = "sampling_based_reachability_search/sampling_based_reachability"


class ModelAdmissionTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.home = Path(temp.name)
        self.enterContext(patch.dict(os.environ, MODEL_POLICY_HOME=str(self.home),
                                     MODEL_POLICY_KEYRING_FILE=str(self.home / "keys.json")))
        (self.home / "keys.json").write_text(json.dumps({
            "active_key_id": "test", "keys": {"test": secrets.token_hex(32)}
        }))
        self.addCleanup(store._cached_loader.cache_clear)

    def draft(self, model_id):
        return self.home / "drafts" / catalog()[model_id]

    def provision(self, model_id):
        relative = catalog()[model_id]
        draft = self.draft(model_id)
        draft.parent.mkdir(parents=True, exist_ok=True)
        draft.write_bytes((TEMPLATES / relative).read_bytes())
        store.publish(self.home, draft)
        path = MODELS / (model_id + ".py")
        name = path.stem
        spec = importlib.util.spec_from_file_location(name, path)
        model = importlib.util.module_from_spec(spec)
        self.enterContext(patch.dict(sys.modules, {name: model}))
        spec.loader.exec_module(model)
        return model

    def update(self, model_id, old, new):
        draft = self.draft(model_id)
        source = draft.read_text()
        self.assertIn(old, source)
        draft.write_text(source.replace(old, new, 1))
        return store.publish(self.home, draft)

    def test_live_edit_changes_one_model(self):
        model = self.provision(RECOVERY)
        second = self.provision(OTHER)
        other_files = [p for p in self.home.rglob("*") if p.is_file() and "volley_successor" in p.name]
        previous = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in other_files}
        data = dict(recovery_time_s=1.3, baseline_recovery_time_s=1, ttv_s=10, previous_rti=1.3)
        old = model.RecoveryTimeInflationConfig()
        self.assertEqual(model.evaluate_recovery_state(**data).phase_label, "GRACEFUL_DEGRADATION")
        self.assertEqual(second.update_volley_successor(2, 3, 1), 4)
        self.update(RECOVERY, '"default" = 1.25', '"default" = 1.5, fixed = true')
        self.assertEqual(model.evaluate_recovery_state(**data).phase_label, "NOMINAL_RECOVERY")
        with self.assertRaisesRegex(ValueError, "fixed"):
            model.evaluate_recovery_state(**data, config=old)
        self.assertEqual(second.update_volley_successor(2, 3, 1), 4)
        self.assertEqual(previous, {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in other_files})

    def test_rejects_wrong_id_invalid_schema_and_rollback_before_next_call(self):
        self.provision(OTHER)
        draft = self.draft(OTHER)
        source = draft.read_bytes()
        active = self.home / "active" / catalog()[OTHER]
        files = [active, active.with_suffix(".toml.manifest.json")]
        before = [p.read_bytes() for p in files]
        for old, new in ((OTHER, RECOVERY), ('"float"', '"str"'), ('"float"', '"float", default = 8, le = 5'),
                         ('"float"', '"float", fixed = true'), ('"float"', '"float", allowed = []')):
            with self.subTest(new=new), self.assertRaises(PolicyPayloadError):
                draft.write_bytes(source)
                self.update(OTHER, old, new)
            self.assertEqual(before, [p.read_bytes() for p in files])
        draft.write_bytes(source)
        with self.assertLogs("model_policy_engine.policy_loader"), self.assertRaises(PolicySecurityError):
            self.update(OTHER, 'version = "1.0.0"', 'version = "0.9.0"')
        self.assertEqual(before, [p.read_bytes() for p in files])

    def test_admissible_inputs_and_default_for_previously_required_argument(self):
        model = self.provision(OTHER)
        self.update(OTHER, 'delta_k = { "annotation" = "float" }',
                    'delta_k = { annotation = "float", default = 2, allowed = [2, 3] }')
        self.assertEqual(model.update_volley_successor(5, v_term_k=1), 6)
        self.assertEqual(model.update_volley_successor(5, 3, 1), 7)
        with self.assertRaisesRegex(ValueError, "outside admitted set"):
            model.update_volley_successor(5, 4, 1)

    def test_returned_evaluator_uses_current_policy(self):
        model_id = "network-and-compute/compute_queueing_limits/littles_law_queue"
        evaluate = self.provision(model_id).lambdified()
        self.assertEqual(evaluate(2, 3), 6)
        self.update(model_id, 'W = { annotation = "float" }',
                    'W = { annotation = "float", default = 4, fixed = true }')
        self.assertEqual(evaluate(2), 8)
        with self.assertRaisesRegex(ValueError, "fixed"):
            evaluate(2, 3)

    def test_toml_transition_mapping(self):
        model_id = "hardware_viability/time_control_enforcement/pavlovian_reflex_state_machine"
        model = self.provision(model_id)
        old = 'transitions = { "annotation" = "Mapping[tuple[str, str], str]" }'
        self.update(model_id, old, old[:-1] + ', default = [{key = ["idle", "tick"], value = "ready"}] }')
        self.assertEqual(model.compute_next_state("idle", 3, 1, "tick"), "ready")

    def test_internal_weights_rejected_or_applied(self):
        model_id = "ai_governance/genai_trust_governance/context_saturation_index"
        model = self.provision(model_id)
        self.assertEqual(model.compute_context_saturation_index(1, 0, 0), 0.5)
        with self.assertRaisesRegex(PolicyPayloadError, "sum"):
            self.update(model_id, "[0.5, 0.3, 0.2]", "[1.0, 0.3, 0.2]")
        self.assertEqual(model.compute_context_saturation_index(1, 0, 0), 0.5)
        self.update(model_id, "[1.0, 0.3, 0.2]", "[1.0, 0.0, 0.0]")
        self.assertEqual(model.compute_context_saturation_index(1, 0, 0), 1.0)

    def test_nested_record_defaults_rejected_before_publication(self):
        model = self.provision(SEARCH)
        config = model.demo_clear_path_config()
        self.assertIsInstance(config.bounds[0], model.Bounds)
        with self.assertRaisesRegex(PolicyPayloadError, "lower must be lt upper"):
            self.update(SEARCH, "{lower = -1.0, upper = 10.0}", "{lower = 12.0, upper = 10.0}")
        self.assertEqual(config, model.demo_clear_path_config())

    def test_restart_fallback_and_missing_first_admission(self):
        model = self.provision(OTHER)
        active = self.home / "active" / catalog()[OTHER]
        active.write_text("broken TOML\n")
        store._cached_loader.cache_clear()
        with self.assertLogs("model_policy_engine.policy_loader"):
            self.assertEqual(model.update_volley_successor(5, 2, 1), 6)
        self.assertTrue(any((self.home / "quarantine").rglob("incident.json")))
        store._cached_loader.cache_clear()
        lkg, = (self.home / "state").glob("lkg_*.json")
        lkg.unlink()
        with self.assertLogs("model_policy_engine.policy_loader"), self.assertRaises(PolicySecurityError):
            model.update_volley_successor(5, 2, 1)
        with patch.dict(os.environ, clear=True), self.assertRaisesRegex(PolicySecurityError, "MODEL_POLICY_HOME"):
            model.update_volley_successor(5, 2, 1)

    def test_version_binding_and_same_digest_epoch_on_reload(self):
        self.provision(OTHER)
        draft = self.draft(OTHER)
        active = self.home / "active" / catalog()[OTHER]
        manifest = active.with_suffix(".toml.manifest.json")
        original = json.loads(manifest.read_bytes())
        newer_stamp = original["issued_at_epoch"] + 1
        store.publish(self.home, draft, epoch=newer_stamp)
        state, = (self.home / "state").glob("lkg_*.json")
        self.assertEqual(json.loads(state.read_bytes())["issued_at_epoch"], newer_stamp)
        loader = store._loader(self.home, OTHER)
        data = json.loads(manifest.read_bytes())
        data["policy_version"] = "1.1.0"
        canonical = f"manifest:v3:test:{active.name}:1.1.0:{newer_stamp}:{data['sha256']}"
        data["hmac_sha256"] = loader._compute_hmac("test", canonical)
        manifest.write_text(json.dumps(data))
        with self.assertLogs("model_policy_engine.policy_loader"), self.assertRaises(PolicySecurityError):
            loader.load(active, allow_fallback=False)

