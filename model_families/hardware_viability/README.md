# Hardware viability

## Subdirectories

- [actuator](actuator/README.md)
- [electrical](electrical/README.md)
- [memory](memory/README.md)
- [queue](queue/README.md)
- [resonance](resonance/README.md)
- [thermal](thermal/README.md)
- [time_control_enforcement](time_control_enforcement/README.md)

## Model files

- [converging_terminal_pressure.py](converging_terminal_pressure.py) — Converging terminal pressure
- [minimum terminal horizon.py](minimum%20terminal%20horizon.py) — Minimum terminal horizon
- [predictive_hardware_viability_state.py](predictive_hardware_viability_state.py) — Predictive hardware viability state
- [recovery_time_inflation.py](recovery_time_inflation.py)

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../model_policy_engine/README.md)

- [hardware_viability/converging_terminal_pressure](../../model_policy_engine/policies/hardware_viability/converging_terminal_pressure_policy.toml)
- [hardware_viability/minimum terminal horizon](../../model_policy_engine/policies/hardware_viability/minimum%20terminal%20horizon_policy.toml)
- [hardware_viability/predictive_hardware_viability_state](../../model_policy_engine/policies/hardware_viability/predictive_hardware_viability_state_policy.toml)
- [hardware_viability/recovery_time_inflation](../../model_policy_engine/policies/hardware_viability/recovery_time_inflation_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
converging_terminal_pressure.py
  compute_converging_terminal_pressure = 0.31
minimum terminal horizon.py
  compute_minimum_terminal_horizon = {"dominant_driver": "THERMAL", "minimum_terminal_horizon_s": 0.4}
predictive_hardware_viability_state.py
  compute_predictive_hardware_viability_state = {"converging_terminal_pressure": 0.3, "dominant_driver": "thermal", "memory_margin_pct": 20.0, "minimum_terminal_horizon_s": 10.0, "queue_margin_items": 300.0, "status": "NOMINAL", "thermal_margin_c": 15.0}
recovery_time_inflation.py
  evaluate_recovery_state = {"baseline_recovery_time_s": 2.0, "divergence_pressure": 0.35, "phase_code": 1, "phase_label": "GRACEFUL_DEGRADATION", "recovery_margin_s": 4.0, "recovery_ratio": 0.5, "recovery_time_s": 4.0, "rti": 2.0, "rti_growth_per_s": 1.0, "terminal_required": false, "ttv_s": 8.0}
  deterministic_exponential_recovery_trace = [1.0, 0.36787944117144233, 0.1353352832366127]
  theoretical_exponential_recovery_time_s = 4.605170185988092
  estimate_recovery_time_s = 2.0
  evaluate_recovery_state = "NOMINAL_RECOVERY"
  evaluate_recovery_state = "LAWFUL_RECOVERY_PRESSURE"
  evaluate_recovery_state = "ESCROW_OR_TERMINAL_REQUIRED"
  RecoveryTraceConfig rejected invalid input
  RecoveryTimeInflationConfig rejected invalid input
PASS hardware_viability
```

<!-- end-observed-output -->

## converging_terminal_pressure.py

### Model context from the archive

HW-GOV-002 — converging terminal pressure.

### Entry points

- `compute_converging_terminal_pressure(thermal_pressure_ratio: float, memory_pressure_ratio: float, queue_pressure_ratio: float, horizon_pressure_ratio: float, weights: Tuple[float, float, float, float]=(0.3, 0.2, 0.2, 0.3))`

### Original formula record

- **Formula id**  HW-GOV-002
- **Name**  Converging terminal pressure
- **Symbolic form**  `P_term = clip(w_T p_T + w_M p_M + w_Q p_Q + w_H p_H, 0, 1)`
- **Typed inputs**  `thermal_pressure_ratio` (float), `memory_pressure_ratio` (float), `queue_pressure_ratio` (float), `horizon_pressure_ratio` (float), `weights` (Tuple[float, float, float, float])
- **Units**  `thermal_pressure_ratio` (unitless), `memory_pressure_ratio` (unitless), `queue_pressure_ratio` (unitless), `horizon_pressure_ratio` (unitless), `weights` (unitless), `output` (unitless)
- **Assumptions**  Pressure ratios must already be normalized into [0,1]. This law is a degradative pressure summary, not a sole decision oracle or corpse-threshold replacement.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_hardware_viability_governance.py`, `rtm_link=lambda_laws.hw_gov_002__hardware_viability_governance__converging_terminal_pressure`, `ssot_gate=notebooks/hw_gov_002__hardware_viability_governance__converging_terminal_pressure.ipynb`

## minimum terminal horizon.py

### Model context from the archive

HW-GOV-001 — minimum terminal horizon.

### Entry points

- `MinimumTerminalHorizon` (type)
- `compute_minimum_terminal_horizon(thermal_horizon_s: float, memory_horizon_s: float, queue_horizon_s: float)`

### Original formula record

- **Formula id**  HW-GOV-001
- **Name**  Minimum terminal horizon
- **Symbolic form**  `H_min = min(H_T, H_M, H_Q)`
- **Typed inputs**  `thermal_horizon_s` (float), `memory_horizon_s` (float), `queue_horizon_s` (float)
- **Units**  `thermal_horizon_s` (s), `memory_horizon_s` (s), `queue_horizon_s` (s), `output` (MinimumTerminalHorizon)
- **Assumptions**  Input horizons are short-horizon earliest credible violation estimates. Infinite horizons are allowed and mean no current predicted breach on that driver.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_hardware_viability_governance.py`, `rtm_link=lambda_laws.hw_gov_001__hardware_viability_governance__minimum_terminal_horizon`, `ssot_gate=notebooks/hw_gov_001__hardware_viability_governance__minimum_terminal_horizon.ipynb`

## predictive_hardware_viability_state.py

### Model context from the archive

HW-GOV-003 — predictive hardware viability state.

### Entry points

- `HardwareViabilityState` (type)
- `compute_predictive_hardware_viability_state(thermal_margin_c: float, memory_margin_pct: float, queue_margin_items: float, minimum_terminal_horizon_s: float, converging_terminal_pressure: float, dominant_driver: Optional[str], critical_horizon_s: float=3.0, degraded_thermal_margin_c: float=7.0, degraded_memory_margin_pct: float=10.0, degraded_queue_margin_items: float=200.0, degraded_pressure_floor: float=0.45)`

### Original formula record

- **Formula id**  HW-GOV-003
- **Name**  Predictive hardware viability state
- **Symbolic form**  `state = classify(m_T, m_M, m_Q, H_min, P_term)`
- **Typed inputs**  `thermal_margin_c` (float), `memory_margin_pct` (float), `queue_margin_items` (float), `minimum_terminal_horizon_s` (float), `converging_terminal_pressure` (float), `dominant_driver` (Optional[str]), `critical_horizon_s` (float), `degraded_thermal_margin_c` (float), `degraded_memory_margin_pct` (float), `degraded_queue_margin_items` (float), `degraded_pressure_floor` (float)
- **Units**  `thermal_margin_c` (C), `memory_margin_pct` (pct), `queue_margin_items` (items), `minimum_terminal_horizon_s` (s), `converging_terminal_pressure` (unitless), `dominant_driver` (label), `critical_horizon_s` (s), `degraded_thermal_margin_c` (C), `degraded_memory_margin_pct` (pct), `degraded_queue_margin_items` (items), `degraded_pressure_floor` (unitless), `output` (HardwareViabilityState)
- **Assumptions**  Hard threshold breach outranks prediction. The critical horizon defines when the substrate is safety-critical even before corpse-threshold breach. Degraded thresholds are soft caution bands for safe derate and retreat preparation.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_hardware_viability_governance.py`, `rtm_link=lambda_laws.hw_gov_003__hardware_viability_governance__predictive_hardware_viability_state`, `ssot_gate=notebooks/hw_gov_003__hardware_viability_governance__predictive_hardware_viability_state.ipynb`

## recovery_time_inflation.py

### Current interface

- The numerical implementation uses Python scalars and sequences. Vector and matrix outputs use lists and nested lists.
- Recovery configuration uses frozen keyword-only dataclasses. Pydantic model serialization and schema methods are removed. Contract symbols and expressions are strings, and the functions take scalar inputs. Trace helpers accept one-dimensional sequences.

### Entry points

- `RecoveryTimeInflationConfig` (type)
- `RecoveryTraceConfig` (type)
- `RecoveryTimeInflationSymbolicContract` (type)
- `RecoveryTimeInflationResult` (type)
- `build_symbolic_contract()`
- `evaluate_recovery_state(*, recovery_time_s: float, baseline_recovery_time_s: float, ttv_s: float, previous_rti: float=1.0, dt_s: float=1.0, config: RecoveryTimeInflationConfig | None=None)`
- `deterministic_exponential_recovery_trace(time_s: list[float], *, amplitude: float, tau_s: float)`
- `theoretical_exponential_recovery_time_s(*, amplitude: float, threshold_abs: float, tau_s: float)`
- `estimate_recovery_time_s(time_s: list[float], signal: list[float], *, threshold_abs: float, dwell_samples: int=5)`
- `symbolic_contract()`

Additional reference comparisons during migration: 269.
