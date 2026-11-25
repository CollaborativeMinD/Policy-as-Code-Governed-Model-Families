"""Role ceilings and reviewed scalar task bindings for the local console."""
import hashlib
from pathlib import Path
import re
import tomllib

from .runtime_policy import RuntimePolicy

from model_policy_engine.schema import admit, catalog, TEMPLATES

ROOT = Path(__file__).resolve().parents[1]
TOOLS = {"viewer": {"inventory.read"}, "admin": {"inventory.read", "policy.open", "policy.apply"},
         "agent": {"inventory.read", "task.execute"}}
BINDINGS = {
    ("network-and-compute/compute_queueing_limits/littles_law_queue", "compute_little_law_queue_length"),
    ("ai_governance/genai_governance/stale_evidence_decay", "compute_stale_evidence_decay"),
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_config(path, pin):
    raw = path.read_bytes()
    if digest(raw) != pin:
        raise ValueError("Console policy digest mismatch")
    config = tomllib.loads(raw.decode())
    limits = RuntimePolicy.read(config)
    if ((set(config) - {"runtime"}) != {"version", "host", "port", "protocol", "poll_seconds", "roles", "tasks"}
            or type(config["version"]) is not int or config["version"] not in (1, 2)
            or config["host"] != "127.0.0.1" or config["protocol"] != "2026-07-28"
            or type(config["port"]) is not int or not 0 < config["port"] < 65536
            or type(config["poll_seconds"]) not in (int, float) or not 0.25 <= config["poll_seconds"] <= 300):
        raise ValueError("Invalid console transport or polling policy")
    if set(config["roles"]) != set(TOOLS):
        raise ValueError("Invalid role policy")
    for role, grants in config["roles"].items():
        if (not isinstance(grants, list) or len(grants) != len(set(grants))
                or not set(grants) <= TOOLS[role] or "inventory.read" not in grants):
            raise ValueError("Invalid tool grant")
    if "policy.apply" in config["roles"]["admin"] and "policy.open" not in config["roles"]["admin"]:
        raise ValueError("Publication requires opening its draft")
    if not isinstance(config["tasks"], dict):
        raise ValueError("Invalid task table")
    for name, task in config["tasks"].items():
        if (not re.fullmatch(r"[a-z][a-z0-9_]{0,63}", name)
                or set(task) != {"model", "operation", "inputs"}
                or (task["model"], task["operation"]) not in BINDINGS or not isinstance(task["inputs"], dict)):
            raise ValueError("Unbound task")
        source = tomllib.loads((TEMPLATES / catalog()[task["model"]]).read_text(encoding="utf8"))
        fields = source["calls"][task["operation"]]
        for key, value in task["inputs"].items():
            fields[key]["default"] = value
        if any("default" not in field and not field.get("none") for field in fields.values()):
            raise ValueError("Incomplete task inputs")
        admit(task["model"], source)
    config["runtime"] = limits
    return config
