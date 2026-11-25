# Memory

## Model files

- [memory_margin.py](memory_margin.py) — Memory margin
- [time_to_memory_violation.py](time_to_memory_violation.py) — Time to memory violation

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../model_policy_engine/README.md)

- [hardware_viability/memory/memory_margin](../../../model_policy_engine/policies/hardware_viability/memory/memory_margin_policy.toml)
- [hardware_viability/memory/time_to_memory_violation](../../../model_policy_engine/policies/hardware_viability/memory/time_to_memory_violation_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
memory_margin.py
  compute_memory_margin = 35.0
time_to_memory_violation.py
  compute_time_to_memory_violation = 58.333333333333336
PASS hardware_viability/memory
```

<!-- end-observed-output -->

## memory_margin.py

### Model context from the archive

HW-MEM-001 — memory margin.

### Entry points

- `compute_memory_margin(current_mem_pct: float, mem_crit_pct: float)`

### Original formula record

- **Formula id**  HW-MEM-001
- **Name**  Memory margin
- **Symbolic form**  `m_M = M_crit - M`
- **Typed inputs**  `current_mem_pct` (float), `mem_crit_pct` (float)
- **Units**  `current_mem_pct` (pct), `mem_crit_pct` (pct), `output` (pct)
- **Assumptions**  Use when memory use is expressed as a governed percent-of-capacity metric and the critical threshold is a real mission limit rather than a cosmetic dashboard line.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_hardware_viability_governance.py`, `rtm_link=lambda_laws.hw_mem_001__hardware_viability_governance__memory_margin`, `ssot_gate=notebooks/hw_mem_001__hardware_viability_governance__memory_margin.ipynb`

## time_to_memory_violation.py

### Model context from the archive

HW-MEM-002 — time to memory violation.

### Entry points

- `compute_time_to_memory_violation(current_mem_pct: float, mem_crit_pct: float, dM_dt_pct_per_s: float)`

### Original formula record

- **Formula id**  HW-MEM-002
- **Name**  Time to memory violation
- **Symbolic form**  `H_M = (M_crit - M) / dM_dt, dM_dt > 0 ; +inf otherwise`
- **Typed inputs**  `current_mem_pct` (float), `mem_crit_pct` (float), `dM_dt_pct_per_s` (float)
- **Units**  `current_mem_pct` (pct), `mem_crit_pct` (pct), `dM_dt_pct_per_s` (pct/s), `output` (s)
- **Assumptions**  Use when memory pressure is actually trending upward and the derivative is stable enough to represent short-horizon exhaustion risk.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_hardware_viability_governance.py`, `rtm_link=lambda_laws.hw_mem_002__hardware_viability_governance__time_to_memory_violation`, `ssot_gate=notebooks/hw_mem_002__hardware_viability_governance__time_to_memory_violation.ipynb`
