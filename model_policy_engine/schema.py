"""Validate signed model documents against their installed call and record contracts."""
import ast
from collections.abc import Mapping
from dataclasses import dataclass
from functools import lru_cache
import math
from pathlib import Path
import re
import tomllib
from types import MappingProxyType

TEMPLATES = Path(__file__).with_name("policies")
UNSET = object()


@lru_cache(maxsize=1)
def catalog():
    ids = {}
    for path in sorted(TEMPLATES.rglob("*_policy.toml")):
        with path.open("rb") as source:
            model_id = tomllib.load(source)["model_id"]
        if model_id in ids:
            raise ValueError(f"Duplicate installed model ID {model_id}")
        ids[model_id] = path.relative_to(TEMPLATES)
    return MappingProxyType(ids)


@lru_cache(maxsize=None)
def contract(model_id):
    if model_id not in catalog():
        raise ValueError(f"Unknown model_id {model_id!r}")
    with (TEMPLATES / catalog()[model_id]).open("rb") as source:
        return freeze(tomllib.load(source))


def freeze(value):
    if isinstance(value, dict):
        return MappingProxyType({k: freeze(v) for k, v in value.items()})
    if isinstance(value, list):
        return tuple(freeze(x) for x in value)
    return value


def materialize(value):
    if isinstance(value, Mapping):
        return {k: materialize(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [materialize(x) for x in value]
    return value


def typed(value, node, record_fields=None, relations=()):
    """Check TOML literals only. Runtime-only Python objects remain caller inputs."""
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        return typed(value, node.left, record_fields, relations) or typed(value, node.right, record_fields, relations)
    if isinstance(node, ast.Constant):
        return value is None and node.value is None
    if isinstance(node, ast.Name):
        name = node.id
        if name in ("float", "int"):
            return type(value) in ((float, int) if name == "float" else (int,)) and math.isfinite(value)
        if name in ("bool", "str"):
            return type(value) is {"bool": bool, "str": str}[name]
        if record_fields is not None and name in record_fields:
            fields = record_fields[name]
            if isinstance(fields, tuple):
                return value in fields
            if not isinstance(value, Mapping) or set(value) - fields.keys():
                return False
            for key, spec in fields.items():
                if key not in value:
                    if default_value(spec) is UNSET:
                        return False
                elif not typed(value[key], annotation(spec["annotation"]), record_fields, relations):
                    return False
                else:
                    if spec.get("fixed") and materialize(value[key]) != materialize(default_value(spec)):
                        raise ValueError(f"{name}.{key} is fixed by policy")
                    check_value(key, spec, value[key])
            values = {key: value.get(key, default_value(spec)) for key, spec in fields.items()}
            check_relations(relations, name, values)
            return True
        if name == "Hashable":
            return type(value) in (str, int, bool, float)
        if name == "Vector":
            return isinstance(value, (list, tuple)) and all(type(x) in (int, float) and math.isfinite(x) for x in value)
        if name in ("Any", "object"):
            return value is None or type(value) in (bool, int, float, str, list, tuple, dict)
        return False
    if not isinstance(node, ast.Subscript):
        return False
    name = getattr(node.value, "id", "")
    parts = node.slice.elts if isinstance(node.slice, ast.Tuple) else [node.slice]
    if name == "Optional":
        return value is None or typed(value, parts[0], record_fields, relations)
    if name in ("dict", "Dict", "Mapping"):
        if isinstance(value, Mapping):
            items = value.items()
        elif isinstance(value, (list, tuple)) and all(isinstance(row, Mapping) and set(row) == {"key", "value"} for row in value):
            items = [(row["key"], row["value"]) for row in value]
        else:
            return False
        keys = set()
        for key, item in items:
            if not typed(key, parts[0], record_fields, relations) or not typed(item, parts[1], record_fields, relations):
                return False
            hash_key = tuple(key) if isinstance(key, (tuple, list)) else key
            if hash_key in keys:
                return False
            keys.add(hash_key)
        return True
    if not isinstance(value, (list, tuple)):
        return False
    if name in ("tuple", "Tuple") and len(parts) > 1 and not (
        isinstance(parts[-1], ast.Constant) and parts[-1].value is Ellipsis
    ):
        return len(value) == len(parts) and all(typed(x, t, record_fields, relations) for x, t in zip(value, parts))
    return name in ("tuple", "Tuple", "Iterable", "Sequence", "list", "List") and all(typed(x, parts[0], record_fields, relations) for x in value)


@lru_cache(maxsize=None)
def annotation(text):
    return ast.parse(text, mode="eval").body


def default_value(field):
    if field.get("none"):
        return None
    if "default" not in field:
        return UNSET
    value = materialize(field["default"])
    if isinstance(value, list) and (field.get("tuple_default") or field["annotation"].startswith(("tuple[", "Tuple[", "Vector"))):
        return tuple(value)
    return value


def check_value(label, field, value, *, check_allowed=True):
    if value is None and (field.get("none") or typed(None, annotation(field["annotation"]))):
        if "allowed" in field:
            raise ValueError(f"{label} outside admitted set")
        return
    if field.get("finite") and (type(value) not in (int, float) or not math.isfinite(value)):
        raise ValueError(f"{label} must be finite")
    if any(key in field for key in ("items_ge", "items_gt", "sum_eq")):
        if not isinstance(value, (tuple, list)) or not all(type(x) in (int, float) and math.isfinite(x) for x in value):
            raise ValueError(f"{label} requires finite numeric items")
        if "items_ge" in field and any(x < field["items_ge"] for x in value):
            raise ValueError(f"{label} violates item lower bound")
        if "items_gt" in field and any(x <= field["items_gt"] for x in value):
            raise ValueError(f"{label} violates strict item lower bound")
        if "sum_eq" in field and not math.isclose(math.fsum(value), field["sum_eq"], rel_tol=1e-12, abs_tol=1e-12):
            raise ValueError(f"{label} violates the required sum")
    scalar = field["annotation"]
    if ("allowed" in field or field.get("fixed") or field.get("finite")) and scalar in ("int", "float", "bool", "str") and not typed(value, annotation(scalar)):
        raise ValueError(f"{label}: expected {scalar}")
    if check_allowed and "allowed" in field and materialize(value) not in materialize(field["allowed"]):
        raise ValueError(f"{label} outside admitted set")
    for key, op in (("gt", float.__gt__), ("ge", float.__ge__), ("lt", float.__lt__), ("le", float.__le__)):
        if key in field:
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not op(float(value), field[key]):
                raise ValueError(f"{label} violates {key} {field[key]}")
    for key in ("min_items", "max_items"):
        if key in field:
            count = len(value)
            if (key == "min_items" and count < field[key]) or (key == "max_items" and count > field[key]):
                raise ValueError(f"{label} violates {key} {field[key]}")


def validate_field(label, field, base, record_fields, relations):
    keys = {"items_ge", "items_gt", "sum_eq", "finite", "tuple_default", "annotation", "default", "none", "fixed", "gt", "ge", "lt", "le", "allowed", "min_items", "max_items"}
    if not isinstance(field, dict) or set(field) - keys or field.get("annotation") != base["annotation"]:
        raise ValueError(f"{label}: unknown field option or incompatible annotation")
    if field.get("tuple_default") != base.get("tuple_default"):
        raise ValueError(f"{label}: incompatible default container")
    for key in ("none", "fixed", "finite"):
        if key in field and type(field[key]) is not bool:
            raise ValueError(f"{label}: {key} requires a boolean")
    if field.get("none") and ("default" in field or not base.get("none") and not typed(None, annotation(base["annotation"]))):
        raise ValueError(f"{label}: invalid null default")
    kind = field["annotation"].replace("Optional[", "").replace(" | None", "").rstrip("]")
    if (field.get("finite") or any(k in field for k in ("gt", "ge", "lt", "le"))) and kind not in ("float", "int", "Any"):
        raise ValueError(f"{label}: numeric bounds on a nonnumeric field")
    if any(k in field for k in ("min_items", "max_items")) and kind in ("int", "float", "bool"):
        raise ValueError(f"{label}: length constraint on a scalar")
    if any(key in field for key in ("items_ge", "items_gt", "sum_eq")):
        node = annotation(field["annotation"])
        members = node.slice.elts if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Tuple) else [getattr(node, "slice", None)]
        numeric = all(getattr(n, "id", None) in ("float", "int") or isinstance(n, ast.Constant) and n.value is Ellipsis for n in members)
        if not numeric or getattr(node.value, "id", None) not in ("list", "List", "tuple", "Tuple", "Sequence"):
            raise ValueError(f"{label}: item constraint requires a numeric sequence")
    for key in ("gt", "ge", "lt", "le", "items_ge", "items_gt", "sum_eq"):
        if key in field and (type(field[key]) not in (int, float) or not math.isfinite(field[key])):
            raise ValueError(f"{label}: invalid {key}")
    for key in ("min_items", "max_items"):
        if key in field and (type(field[key]) is not int or field[key] < 0):
            raise ValueError(f"{label}: invalid length")
    if field.get("min_items", 0) > field.get("max_items", math.inf):
        raise ValueError(f"{label}: empty length interval")
    lower = max(field.get("ge", -math.inf), field.get("gt", -math.inf))
    upper = min(field.get("le", math.inf), field.get("lt", math.inf))
    if lower > upper or lower == upper and (field.get("gt") == lower or field.get("lt") == upper):
        raise ValueError(f"{label}: empty numeric interval")
    if "allowed" in field:
        if not isinstance(field["allowed"], list) or not field["allowed"]:
            raise ValueError(f"{label}: empty or invalid admissible set")
        for item in field["allowed"]:
            if not typed(item, annotation(base["annotation"]), record_fields, relations):
                raise ValueError(f"{label}: incompatible admissible value")
            check_value(label, field, item)
    default = default_value(field)
    if default is UNSET and ("default" in base or base.get("none") or field.get("fixed")):
        raise ValueError(f"{label}: missing default")
    if default is not UNSET:
        if default is not None and not typed(default, annotation(base["annotation"]), record_fields, relations):
            raise ValueError(f"{label}: incompatible TOML default")
        check_value(label, field, default)


@dataclass(frozen=True)
class AdmittedModel:
    version: str
    model_id: str
    calls: Mapping
    settings: Mapping
    relations: tuple
    enums: Mapping


def check_relations(relations, operation, values):
    for relation in relations:
        if relation["call"] != operation:
            continue
        left, right = (values.get(relation[k], UNSET) for k in ("left", "right"))
        if left is UNSET or right is UNSET:
            continue
        op = relation["op"]
        if op == "lt":
            ok = left < right
        elif op == "le":
            ok = left <= right
        elif op == "same_length":
            ok = len(left) == len(right)
        elif op == "member":
            ok = left in right
        else:
            ok = set(left).isdisjoint(right)
        if not ok:
            raise ValueError(f"{operation}: {relation['left']} must be {relation['op']} {relation['right']}")


def admit(model_id, doc):
    base = contract(model_id)
    if set(doc) - {"relations"} != set(base) - {"relations"} or doc.get("model_id") != model_id:
        raise ValueError(f"Expected complete policy for {model_id}")
    if not isinstance(doc["settings"], dict):
        raise ValueError("settings must be a table")
    if not isinstance(doc["records"], list):
        raise ValueError("records must be an array")
    if not isinstance(doc["version"], str) or not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", doc["version"]):
        raise ValueError("Invalid policy version")
    calls = doc["calls"]
    if not isinstance(calls, dict) or calls.keys() != base["calls"].keys() or not all(isinstance(v, dict) for v in calls.values()):
        raise ValueError("Policy operation set does not match the installed model")
    if tuple(doc.get("records", [])) != base["records"]:
        raise ValueError("Policy record list does not match the model")
    enums = doc.get("enums", {})
    if enums != base.get("enums", {}) or not isinstance(enums, dict):
        raise ValueError("Enum wire members must match the installed contract")
    for call, fields in [("settings", doc["settings"]), *calls.items()]:
        original = base["settings"] if call == "settings" else base["calls"][call]
        if fields.keys() != original.keys() or any(not isinstance(spec, dict) or spec.get("annotation") != original[key]["annotation"]
                                                   for key, spec in fields.items()):
            raise ValueError(f"Missing, unknown or incompatible fields in {call}")
    record_fields = {name: calls[name] for name in base["records"]}
    record_fields.update({name: tuple(items.values()) for name, items in enums.items()})
    settings = doc["settings"]
    relations = doc.get("relations", [])
    if not isinstance(relations, list):
        raise ValueError("relations must be an array")
    for rule in relations:
        if not isinstance(rule, dict) or set(rule) != {"call","left","right","op"} or rule["op"] not in ("le", "lt", "member", "same_length", "disjoint"):
            raise ValueError("Invalid relation")
        if not all(isinstance(item, str) for item in rule.values()):
            raise ValueError("Invalid relation field")
        fields = settings if rule["call"] == "settings" else calls.get(rule["call"], {})
        if not isinstance(fields, dict):
            raise ValueError("Relation operation requires a table")
        if any(rule[k] not in fields for k in ("left", "right")) or (rule["op"] in ("lt", "le") and any(fields[rule[k]]["annotation"] not in ("int", "float") for k in ("left", "right"))):
            raise ValueError("Unknown relation field")
        def is_container(key):
            kind = fields[rule[key]]["annotation"].split("[")[0]
            return kind in ("Vector", "tuple", "Tuple", "list", "List", "str", "Sequence", "dict", "Dict", "Mapping")
        if rule["op"] in ("same_length", "disjoint") and not all(is_container(k) for k in ("left", "right")):
            raise ValueError("Relation requires two containers")
        if rule["op"] == "member" and not is_container("right"):
            raise ValueError("Membership requires a container")
    for name, fields, source in [("settings", settings, base["settings"]), *(
        (call, fields, base["calls"][call]) for call, fields in calls.items()
    )]:
        if not isinstance(fields, dict) or fields.keys() != source.keys():
            raise ValueError(f"Missing or unknown fields in {name}")
        for key, field in fields.items():
            validate_field(f"{name}.{key}", field, source[key], record_fields, relations)
    for call, fields in [("settings", settings), *calls.items()]:
        check_relations(relations, call, {k: default_value(v) for k,v in fields.items()})
    return AdmittedModel(doc["version"], model_id, freeze(calls), freeze(settings), tuple(freeze(r) for r in relations), freeze(enums))

