"""A model's single dependency for admitted configuration on ordinary calls."""
from collections.abc import Iterable, Mapping, Sized
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from enum import Enum
from functools import wraps
import inspect
import ast

from .schema import annotation, UNSET, check_relations, check_value, contract, default_value, materialize
from .runtime_types import checked
from .store import load_model


class ModelPolicy:
    default = UNSET

    def __init__(self, model_id):
        self.model_id = model_id
        self._records = {}
        self._enums = {}
        self._current = ContextVar(model_id, default=None)

    @contextmanager
    def _scope(self):
        current = self._current.get()
        if current is not None:
            yield current
            return
        admitted = load_model(self.model_id)
        token = self._current.set(admitted)
        try:
            yield admitted
        finally:
            self._current.reset(token)

    def value(self, name):
        with self._scope() as policy:
            field = policy.settings[name]
            return self._literal(default_value(field), annotation(field["annotation"]))

    def enum(self, name, module):
        with self._scope() as policy:
            cls = Enum(name, dict(policy.enums[name]), module=module)
        self._enums[name] = cls
        return cls

    def record(self, **options):
        def decorate(cls):
            with self._scope() as policy:
                fields = policy.calls[cls.__name__]
                # Use contract order for positional constructor compatibility.
                order = contract(self.model_id)["calls"][cls.__name__]
                cls.__annotations__ = {key: fields[key]["annotation"] for key in order}
                for key in order:
                    if "default" in order[key] or order[key].get("none"):
                        setattr(cls, key, UNSET)
            cls = dataclass(**options)(cls)
            self._records[cls.__name__] = cls
            cls.__init__ = self._wrap(cls.__name__, cls.__init__)
            return cls
        return decorate

    def _literal(self, value, node):
        if value is None:
            return None
        if isinstance(node, ast.Name):
            if node.id in self._enums:
                return self._enums[node.id](value)
            if node.id in self._records:
                fields = self._current.get().calls[node.id]
                return self._records[node.id](**{key: self._literal(item, annotation(fields[key]["annotation"]))
                                                 for key, item in value.items()})
            if node.id == "Vector":
                return tuple(value)
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
            branch = node.right if isinstance(node.left, ast.Constant) else node.left
            return self._literal(value, branch)
        if isinstance(node, ast.Subscript):
            kind = getattr(node.value, "id", "")
            parts = node.slice.elts if isinstance(node.slice, ast.Tuple) else [node.slice]
            if kind in ("dict", "Dict", "Mapping"):
                items = value.items() if isinstance(value, Mapping) else ((row["key"], row["value"]) for row in value)
                return {self._literal(key, parts[0]): self._literal(item, parts[1]) for key, item in items}
            if kind == "Optional":
                return self._literal(value, parts[0])
            if isinstance(value, (list, tuple)):
                members = (parts if kind in ("tuple", "Tuple") and len(parts) > 1 and
                           not isinstance(parts[-1], ast.Constant) else [parts[0]] * len(value))
                items = [self._literal(item, part) for item, part in zip(value, members)]
                return tuple(items) if kind in ("tuple", "Tuple") or isinstance(value, tuple) else items
        return value

    def _check_record(self, value, policy):
        name = type(value).__name__
        if type(value) is not self._records.get(name):
            return
        fields = policy.calls[name]
        values = {key: getattr(value, key) for key in fields}
        for key, field in fields.items():
            self._check_explicit(key, field, values[key], policy, True)
        check_relations(policy.relations, name, values)

    def _check_explicit(self, key, field, value, policy, check_records):
        node = annotation(field["annotation"])
        visit = (lambda record: self._check_record(record, policy)) if check_records else None
        if value is not None and "max_items" in field:
            limit = field["max_items"]
            if (isinstance(node, ast.Subscript) and getattr(node.value, "id", "") == "Iterable"
                    and isinstance(value, Iterable) and not isinstance(value, Sized)):
                items = []
                for item in value:
                    if len(items) == limit:
                        raise ValueError(f"{key} violates max_items {limit}")
                    items.append(item)
                value = tuple(items)
            if isinstance(value, Sized) and len(value) > limit:
                raise ValueError(f"{key} violates max_items {limit}")
        value = checked(value, node, key, self._records, self._enums, visit)
        if field.get("fixed") and materialize(value) != materialize(self._literal(default_value(field), node)):
            raise ValueError(f"{self.model_id}.{key} is fixed by policy")
        if "allowed" in field and not any(
            materialize(value) == materialize(self._literal(materialize(item), node)) for item in field["allowed"]
        ):
            raise ValueError(f"{key} outside admitted set")
        check_value(key, field, value.value if isinstance(value, Enum) else value, check_allowed=False)
        return value

    def _wrap(self, operation, function):
        signature = inspect.signature(function)
        declared = contract(self.model_id)["calls"][operation]
        parameters = set(signature.parameters) - {"self", "cls"}
        if parameters != declared.keys():
            raise ValueError(f"{self.model_id}.{operation}: runtime parameters differ from TOML")
        for name in parameters:
            if signature.parameters[name].default not in (inspect.Parameter.empty, UNSET):
                raise ValueError(f"{self.model_id}.{operation}.{name}: move the default to TOML")

        @wraps(function)
        def governed(*args, **kwargs):
            entering = self._current.get() is None
            with self._scope() as policy:
                fields = policy.calls[operation]
                bound = signature.bind_partial(*args, **kwargs)
                if entering and "self" in bound.arguments and not operation.endswith(".__init__"):
                    owner = bound.arguments["self"]
                    if operation != type(owner).__name__:
                        self._check_record(owner, policy)
                        for key in policy.calls.get(type(owner).__name__ + ".__init__", {}):
                            self._check_record(getattr(owner, key, None), policy)
                for name, field in fields.items():
                    value = bound.arguments.get(name, UNSET)
                    if value is UNSET:
                        value = default_value(field)
                        if value is UNSET:
                            continue
                        value = self._literal(value, annotation(field["annotation"]))
                        bound.arguments[name] = value
                    bound.arguments[name] = self._check_explicit(name, field, value, policy, entering)
                check_relations(policy.relations, operation, bound.arguments)
                return function(*bound.args, **bound.kwargs)
        return governed

    def evaluator(self, operation):
        """Bind an exported callable produced by a factory to its declared operation."""
        return lambda function: self._wrap(operation, function)

    def bind(self, namespace):
        """Wrap only this module's declared operations, preserving aliases and classes."""
        operations = contract(self.model_id)["calls"]
        wrappers = {}
        for operation in operations:
            owner, _, member = operation.partition(".")
            if owner not in namespace or (member and inspect.isclass(namespace[owner]) and
                                          member not in vars(namespace[owner])):
                raise ValueError(f"{self.model_id}.{operation}: missing runtime implementation")
        for name, obj in list(namespace.items()):
            if inspect.isfunction(obj) and obj.__globals__ is namespace:
                if obj.__name__ not in operations:
                    if not name.startswith("_"):
                        raise ValueError(f"{self.model_id}.{name}: missing TOML operation")
                    continue
                if obj not in wrappers:
                    wrappers[obj] = self._wrap(obj.__name__, obj)
                namespace[name] = wrappers[obj]
            elif inspect.isclass(obj) and obj.__module__ == namespace["__name__"]:
                for method, fn in list(vars(obj).items()):
                    key = f"{obj.__name__}.{method}"
                    if not method.startswith("_") and isinstance(fn, (staticmethod, classmethod, property)):
                        raise ValueError(f"{key}: unsupported public descriptor")
                    if not method.startswith("_") and inspect.isfunction(fn) and key not in operations:
                        raise ValueError(f"{key}: missing TOML operation")
                    if key in operations and inspect.isfunction(fn):
                        setattr(obj, method, self._wrap(key, fn))

