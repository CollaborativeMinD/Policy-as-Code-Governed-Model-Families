# Queue

## Model files

- [queue_margin.py](queue_margin.py) — Queue margin
- [time_to_queue_violation.py](time_to_queue_violation.py) — Time to queue violation

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../model_policy_engine/README.md)

- [hardware_viability/queue/queue_margin](../../../model_policy_engine/policies/hardware_viability/queue/queue_margin_policy.toml)
- [hardware_viability/queue/time_to_queue_violation](../../../model_policy_engine/policies/hardware_viability/queue/time_to_queue_violation_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
queue_margin.py
  compute_queue_margin = 7
time_to_queue_violation.py
  compute_time_to_queue_violation = 11.666666666666668
PASS hardware_viability/queue
```

<!-- end-observed-output -->

## queue_margin.py

### Model context from the archive

HW-QUEUE-001 — queue margin.

### Entry points

- `compute_queue_margin(queue_backlog_items: int, queue_crit_items: int)`

### Original formula record

- **Formula id**  HW-QUEUE-001
- **Name**  Queue margin
- **Symbolic form**  `m_Q = Q_crit - Q`
- **Typed inputs**  `queue_backlog_items` (int), `queue_crit_items` (int)
- **Units**  `queue_backlog_items` (items), `queue_crit_items` (items), `output` (items)
- **Assumptions**  Use when backlog count is a meaningful proxy for substrate timing stress and the critical queue threshold is tied to deadline or service survivability, not aesthetics.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_hardware_viability_governance.py`, `rtm_link=lambda_laws.hw_queue_001__hardware_viability_governance__queue_margin`, `ssot_gate=notebooks/hw_queue_001__hardware_viability_governance__queue_margin.ipynb`

## time_to_queue_violation.py

### Model context from the archive

HW-QUEUE-002 — time to queue violation.

### Entry points

- `compute_time_to_queue_violation(queue_backlog_items: int, queue_crit_items: int, dQ_dt_items_per_s: float)`

### Original formula record

- **Formula id**  HW-QUEUE-002
- **Name**  Time to queue violation
- **Symbolic form**  `H_Q = (Q_crit - Q) / dQ_dt, dQ_dt > 0 ; +inf otherwise`
- **Typed inputs**  `queue_backlog_items` (int), `queue_crit_items` (int), `dQ_dt_items_per_s` (float)
- **Units**  `queue_backlog_items` (items), `queue_crit_items` (items), `dQ_dt_items_per_s` (items/s), `output` (s)
- **Assumptions**  Use when queue growth is monotonic enough over the local horizon to estimate imminent service collapse.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_hardware_viability_governance.py`, `rtm_link=lambda_laws.hw_queue_002__hardware_viability_governance__time_to_queue_violation`, `ssot_gate=notebooks/hw_queue_002__hardware_viability_governance__time_to_queue_violation.ipynb`
