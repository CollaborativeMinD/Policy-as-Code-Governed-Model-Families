"""Standalone formula metadata types."""

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('base')

from typing import Dict, Optional


RuntimeClass = _policy.enum("RuntimeClass", __name__)
DeploymentClass = _policy.enum("DeploymentClass", __name__)


@_policy.record()
class FormulaMetadata:
    """Captures doctrinal metadata for a single formula implementation."""


    def to_dict(self) -> Dict[str, str]:
        """Serialize metadata to a plain dictionary.

        This helper makes it easy to emit the registry or embed
        metadata into evidence artifacts.
        """
        return {
            "formula_id": self.formula_id,
            "name": self.name,
            "symbolic_form": self.symbolic_form,
            "typed_inputs": self.typed_inputs,
            "units": self.units,
            "assumptions": self.assumptions,
            "runtime_class": self.runtime_class.value,
            "deployment_class": self.deployment_class.value,
            "tests": self.tests,
            "evidence_hooks": self.evidence_hooks,
            "rtm_link": self.rtm_link,
            "ssot_gate": self.ssot_gate,
        }

_policy.bind(globals())
