"""Admission and math regressions through ordinary, independently loaded model files."""
import math
import re
from itertools import combinations
from decimal import Decimal, localcontext
from fractions import Fraction
from types import SimpleNamespace
import unittest

import test_model_policies as fixtures

QUEUE = "network-and-compute/compute_queueing_limits/"
THERMAL = "hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_rc_envelope/"


class RuntimeReviewTests(unittest.TestCase):
    setUp = fixtures.ModelAdmissionTests.setUp
    provision = fixtures.ModelAdmissionTests.provision
    draft = fixtures.ModelAdmissionTests.draft
    update = fixtures.ModelAdmissionTests.update

    def test_scalar_sequence_and_record_types(self):
        trust = self.provision("ai_governance/genai_trust_governance/context_saturation_index")
        for bad in (True, 1.5):
            with self.subTest(bad=bad), self.assertRaisesRegex(ValueError, "conflict_count"):
                trust.context_saturation_index(0, bad, 0)
        refs = self.provision("ai_governance/genai_governance/evidence_coverage_ratio")
        with self.assertRaisesRegex(ValueError, "required_refs"):
            refs.evidence_coverage_ratio([1], ["1"])
        rec = self.provision("hardware_viability/recovery_time_inflation")
        with self.assertRaises(TypeError):
            rec.PHASE_LABELS[0] = "unknown"
        fake = SimpleNamespace(**vars(rec.RecoveryTimeInflationConfig()))
        with self.assertRaisesRegex(ValueError, "config"):
            rec.evaluate_recovery_state(recovery_time_s=1, baseline_recovery_time_s=1, ttv_s=2, config=fake)

    def test_exact_scaling_laws(self):
        amdahl = self.provision(QUEUE + "amdahl_cluster_limit")
        queue = self.provision(QUEUE + "littles_law_queue")
        for p in (Fraction(0), Fraction(1, 8), Fraction(3, 4), Fraction(1)):
            for workers in (1, 2, 7, 4096):
                serial_time = 1 - p
                elapsed = serial_time + p / workers
                self.assertAlmostEqual(amdahl.compute_amdahl_speedup(float(p), workers), float(1 / elapsed))
                self.assertEqual(queue.compute_little_law_queue_length(workers, float(p)), float(workers * p))

    def test_thermal_crossings_against_decimal(self):
        heat = self.provision(THERMAL + "time_to_temperature_threshold")
        cool = self.provision(THERMAL + "cooldown_time_to_rearm")
        for sign, model, compute in ((1, heat, heat.compute_time_to_temperature_threshold),
                                     (-1, cool, cool.compute_cooldown_time_to_rearm)):
            for change in (1e-16, 0.25, 25, math.nextafter(100.0, 0.0)):
                args = (0, sign * change, sign * 100, 50)
                with localcontext() as ctx:
                    ctx.prec = 85
                    start, target, eq, tau = map(Decimal, args)
                    expected = float(-tau * ((target - eq) / (start - eq)).ln())
                for func in (compute, model.lambdified()):
                    with self.subTest(sign=sign, change=change, function=func.__name__):
                        self.assertTrue(math.isclose(func(*args), expected, rel_tol=2e-14),
                                        (args, expected))

    def test_generator_edges_reusable_within_one_call(self):
        graph = self.provision("network-and-compute/network_execution_bounds/k_connectivity_survival")
        edges = [("a", "b"), ("b", "c"), ("c", "a")]
        self.assertTrue(graph.has_two_independent_paths(iter("abc"), iter(edges)))

    def test_alias_observes_published_policy(self):
        mid = "ai_governance/genai_governance/stale_evidence_decay"
        model = self.provision(mid)
        evaluate = model.stale_evidence_decay
        before = evaluate(5, 10)
        draft = self.draft(mid).read_text()
        default = re.search(r'decay_power = .*?("default" = [\d.]+)', draft).group(1)
        self.update(mid, default, '"default" = 3.0, fixed = true')
        self.assertNotEqual(before, evaluate(5, 10))
        self.assertEqual(evaluate(5, 10), 0.125)
        with self.assertRaisesRegex(ValueError, "fixed"):
            evaluate(5, 10, 2)

    def test_sensor_posterior_against_independent_scalar_fusion(self):
        update = self.provision("estimation_detection/kalman_filter").kalman_predict_update
        for prior, noise in ((4, 1), (1, 4), (10**18, 1), (1, 10**18)):
            state, cov = update([[1]], [[0]], [[1]], [0], [[prior]], [0], [2], [[0]], [[noise]])
            posterior = Fraction(prior * noise, prior + noise)
            self.assertTrue(math.isclose(cov[0][0], float(posterior), rel_tol=1e-14), (prior, noise, cov))
            self.assertTrue(math.isclose(state[0], float(2 * posterior / noise), rel_tol=1e-14))

    def test_two_layer_heat_balance(self):
        model = self.provision("hardware_viability/thermal/thermal_truth/thermal_two_layer/two_layer_temperature_step")
        for conduction in (0, 1, 5):
            for dt in (0, 0.25, 1):
                skin, core = model.compute_two_layer_temperature_step(
                    30, 10, 20, 0, 0, 0, 1, 5, 20, conduction, 3, 2, dt)
                self.assertAlmostEqual(5 * (skin - 30) + 20 * (core - 10), 5 * dt)

    def test_vertex_connectivity_by_enumerating_vertex_cuts(self):
        compute = self.provision("graph-survivability/graph_survivability").compute_vertex_connectivity
        def separates(graph, removed):
            remaining = set(graph).difference(removed)
            seen = set()
            pending = [next(iter(remaining))]
            while pending:
                node = pending.pop()
                if node not in seen:
                    seen.add(node)
                    pending.extend((graph[node] & remaining) - seen)
            return seen != remaining
        for n in range(1, 6):
            edges = list(combinations(range(n), 2))
            for mask in range(1 << len(edges)):
                graph = {i: set() for i in range(n)}
                for index, (a, b) in enumerate(edges):
                    if mask & (1 << index):
                        graph[a].add(b)
                        graph[b].add(a)
                expected = next((k for k in range(n - 1) if any(
                    separates(graph, cut) for cut in combinations(graph, k))), n - 1)
                self.assertEqual(compute(graph), expected, (n, mask))

    def test_admitted_mapping_values_reach_lookup(self):
        mid = "hardware_viability/time_control_enforcement/pavlovian_reflex_state_machine"
        model = self.provision(mid)
        old = 'transitions = { "annotation" = "Mapping[tuple[str, str], str]" }'
        rows = '[{key = ["idle", "tick"], value = "ready"}]'
        self.update(mid, old, old[:-1] + f', allowed = [{rows}], default = {rows} }}')
        self.assertEqual(model.compute_next_state("idle", 2, 1, "tick"), "ready")
        with self.assertRaisesRegex(ValueError, "outside admitted set"):
            model.compute_next_state("idle", 2, 1, "tick", {("idle", "tick"): "other"})

    def test_source_drift_fails_at_binding(self):
        from model_policy_engine import ModelPolicy
        mid = "ai_governance/genai_governance/stale_evidence_decay"
        for body, reason in (
            ("def another(): pass", "missing runtime implementation"),
            ("def compute_stale_evidence_decay(age_s): pass", "parameters differ"),
            ("def compute_stale_evidence_decay(age_s, freshness_margin_s, decay_power=2): pass", "default to TOML"),
            ("def compute_stale_evidence_decay(age_s, freshness_margin_s, decay_power): pass"
             "\ndef another(): pass", "missing TOML operation"),
        ):
            ns = {"__name__": "test_model"}
            exec(body, ns)
            with self.subTest(reason=reason), self.assertRaisesRegex(ValueError, reason):
                ModelPolicy(mid).bind(ns)

    def test_thermal_crossings_at_binary64_extremes(self):
        heat = self.provision(THERMAL + "time_to_temperature_threshold")
        for args in ((0., 1e-16, 1e308, 1e308), (-1e308, 0., 1e308, 1.),
                     (-1e308, 0., 1e-300, 1.)):
            with localcontext() as ctx:
                ctx.prec = 700
                start, target, eq, tau = map(Decimal.from_float, args)
                expected = float(-tau * ((target - eq) / (start - eq)).ln())
            got = heat.compute_time_to_temperature_threshold(*args)
            self.assertTrue(math.isclose(got, expected, rel_tol=2e-14), (args, expected, got))

    def test_shared_sensor_observation(self):
        update = self.provision("estimation_detection/kalman_filter").kalman_predict_update
        x, p = update([[1, 0], [0, 1]], [[0], [0]], [[1, 1]], [0, 0],
                      [[2, 0], [0, 3]], [0], [6], [[0, 0], [0, 0]], [[1]])
        for a, b in zip(x + p[0] + p[1], [2, 3, Fraction(4, 3), -1, -1, Fraction(3, 2)]):
            self.assertAlmostEqual(a, float(b))

    def test_length_ceiling_stops_a_stream_early(self):
        mid = "network-and-compute/network_execution_bounds/k_connectivity_survival"
        graph = self.provision(mid)
        old = 'nodes = { "annotation" = "Iterable[str]" }'
        self.update(mid, old, old[:-1] + ', max_items = 2 }')
        def nodes():
            yield from ("a", "b", "c")
            self.fail("read past the first excess item")
        with self.assertRaisesRegex(ValueError, "max_items"):
            graph.has_two_independent_paths(nodes(), ())

    def test_radio_power_budget_in_linear_units(self):
        radio = self.provision("space-and-comms/communications_and_radar")
        linear = (4, 2, 8, 5, 1.25, 1)
        expected_watts = Fraction(4 * 2 * 8, 5) / Fraction(5, 4)
        received = radio.compute_received_power_db(*(10 * math.log10(x) for x in linear))
        self.assertAlmostEqual(10 ** (received / 10), float(expected_watts))
