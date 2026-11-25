"""Validate Python call values against the annotation grammar used by model contracts."""
import ast
from collections.abc import Hashable, Iterable, Mapping, Sequence


class InputTypeError(ValueError):
    pass


def checked(value, node, label, records, enums, visit_record):
    def child(item, part):
        return checked(item, part, label, records, enums, visit_record)

    def reject():
        raise InputTypeError(f"{label}: expected {ast.unparse(node)}, got {type(value).__name__}")

    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        try:
            return child(value, node.left)
        except InputTypeError:
            return child(value, node.right)
    if isinstance(node, ast.Constant):
        if value is None and node.value is None:
            return value
        reject()
    if isinstance(node, ast.Name):
        kind = node.id
        if kind in records:
            if type(value) is not records[kind]:
                reject()
            if visit_record:
                visit_record(value)
        elif kind in enums:
            if type(value) is not enums[kind]:
                reject()
        elif kind == "Vector":
            if not isinstance(value, (list, tuple)) or any(type(x) not in (int, float) for x in value):
                reject()
            return tuple(value)
        elif kind not in ("Any", "object"):
            types = {"str": (str,), "bool": (bool,), "float": (float, int), "int": (int,)}
            if kind == "Hashable":
                if not isinstance(value, Hashable):
                    reject()
            elif type(value) not in types.get(kind, ()):
                reject()
        return value
    kind = node.value.id
    parts = node.slice.elts if isinstance(node.slice, ast.Tuple) else [node.slice]
    if kind == "Optional":
        return None if value is None else child(value, parts[0])
    if kind == "Callable":
        if not callable(value):
            reject()
        return value
    if kind in ("dict", "Dict", "Mapping"):
        if not isinstance(value, Mapping if kind == "Mapping" else dict):
            reject()
        replacement = None
        for key, item in value.items():
            child(key, parts[0])
            new = child(item, parts[1])
            if new is not item:
                if replacement is None:
                    replacement = dict(value)
                replacement[key] = new
        return value if replacement is None else replacement
    containers = {"tuple": tuple, "Tuple": tuple, "list": list, "List": list,
                  "Sequence": Sequence, "Iterable": Iterable}
    # JSON array pairs are part of the shipped Python replay interface.
    if kind in ("tuple", "Tuple") and isinstance(value, list):
        value = tuple(value)
    if kind not in containers or not isinstance(value, containers[kind]) or isinstance(value, (str, bytes)):
        reject()
    # Snapshot one-shot iterables once. Validation must not exhaust the model's input.
    if not isinstance(value, Sequence):
        value = tuple(value)
    fixed_tuple = kind in ("tuple", "Tuple") and len(parts) > 1 and not isinstance(parts[-1], ast.Constant)
    if fixed_tuple and len(value) != len(parts):
        reject()
    replacement = None
    for i, item in enumerate(value):
        new = child(item, parts[i] if fixed_tuple else parts[0])
        if new is not item:
            if replacement is None:
                replacement = list(value)
            replacement[i] = new
    if replacement is None:
        return value
    return tuple(replacement) if isinstance(value, tuple) else replacement
