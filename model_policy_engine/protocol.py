"""Immutable standard-library records for the supplied loader's TOML-defined protocol."""
from dataclasses import asdict, field, make_dataclass
import json
from pathlib import Path
import re
import tomllib


with Path(__file__).with_name("protocol.toml").open("rb") as source:
    _schemas = tomllib.load(source)


def _validated(name, value, spec):
    kind = spec["type"]
    if kind == "tuple[str, ...]":
        if not isinstance(value, (tuple, list)) or any(type(item) is not str for item in value):
            raise ValueError(f"{name} requires a sequence of strings")
        value = tuple(value)
    elif type(value) is not {"str": str, "int": int, "bool": bool}[kind]:
        raise ValueError(f"{name} requires {kind}")
    if "pattern" in spec and not re.fullmatch(spec["pattern"], value):
        raise ValueError(f"{name} has invalid format")
    if "min_length" in spec and len(value) < spec["min_length"]:
        raise ValueError(f"{name} is too short")
    if "max_length" in spec and len(value) > spec["max_length"]:
        raise ValueError(f"{name} is too long")
    if "gt" in spec and value <= spec["gt"] or "ge" in spec and value < spec["ge"]:
        raise ValueError(f"{name} is below its lower bound")
    if "le" in spec and value > spec["le"]:
        raise ValueError(f"{name} exceeds its upper bound")
    return value


class _Record:
    def __post_init__(self):
        for name, spec in _schemas[type(self).__name__].items():
            object.__setattr__(self, name, _validated(name, getattr(self, name), spec))

    @classmethod
    def model_validate(cls, values):
        if not isinstance(values, dict):
            raise ValueError(f"{cls.__name__} requires an object")
        try:
            return cls(**values)
        except TypeError as exc:
            raise ValueError(f"Invalid fields for {cls.__name__}: {exc}") from exc

    @classmethod
    def model_validate_json(cls, data):
        return cls.model_validate(json.loads(data))

    def model_dump_json(self, *, indent=None):
        return json.dumps(asdict(self), ensure_ascii=False, indent=indent)


class _ActionRules(_Record):
    def __post_init__(self):
        super().__post_init__()
        if self.strict_mode and "*" in self.allowed_actions:
            raise ValueError("Wildcard '*' actions are forbidden when strict_mode is enabled.")


def _record(name, base=_Record):
    types = {"str": str, "int": int, "bool": bool, "tuple[str, ...]": tuple[str, ...]}
    fields = [(key, types[spec["type"]], field(default=spec["default"]) if "default" in spec else field())
              for key, spec in _schemas[name].items()]
    return make_dataclass(name, fields, bases=(base,), frozen=True, kw_only=True,
                          namespace={"__module__": __name__})


PolicyManifest = _record("PolicyManifest")
RollbackOverrideToken = _record("RollbackOverrideToken")
PersistedLKGEnvelope = _record("PersistedLKGEnvelope")
ConsumedTokensLedger = _record("ConsumedTokensLedger")
GoverningPolicy = _record("GoverningPolicy", _ActionRules)

