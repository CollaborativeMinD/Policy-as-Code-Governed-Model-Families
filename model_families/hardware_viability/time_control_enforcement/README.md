# Time control enforcement

### Use cases

Use this set when the runtime must actuate smoothly, survive degraded actuation, enforce emergency deadlines, estimate collapse probability under randomized stress, or execute discrete reflex transitions.

### Non-use cases

Do not use this set as:

- a certified flight/robotics controller,
- a replacement for full rigid-body dynamics,
- a formal model checker,
- an actuator-authority module without hardware gates,
- a complete Monte Carlo campaign harness.

## Subdirectories

- [timing_validity](timing_validity/README.md)

## Model files

- [dead_mans_switch.py](dead_mans_switch.py) — Dead Man's Switch
- [monte_carlo_failure_predictor.py](monte_carlo_failure_predictor.py) — Crucible campaign failure predictor
- [pavlovian_reflex_state_machine.py](pavlovian_reflex_state_machine.py) — Pavlovian Reflex Gate
- [pid_control.py](pid_control.py) — Sniper's Breath

## Coverage exceptions

PCC-13, `degraded_inverse_kinematics.py`, is omitted from this distribution. Its symbolic accessor imports SymPy. The turret-aiming model is excluded from execution, migration and parity claims. The suite reports this case as skipped.

## Regression suites

- [test_time_control_enforcement.py](test_time_control_enforcement.py)

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../model_policy_engine/README.md)

- [hardware_viability/time_control_enforcement/dead_mans_switch](../../../model_policy_engine/policies/hardware_viability/time_control_enforcement/dead_mans_switch_policy.toml)
- [hardware_viability/time_control_enforcement/monte_carlo_failure_predictor](../../../model_policy_engine/policies/hardware_viability/time_control_enforcement/monte_carlo_failure_predictor_policy.toml)
- [hardware_viability/time_control_enforcement/pavlovian_reflex_state_machine](../../../model_policy_engine/policies/hardware_viability/time_control_enforcement/pavlovian_reflex_state_machine_policy.toml)
- [hardware_viability/time_control_enforcement/pid_control](../../../model_policy_engine/policies/hardware_viability/time_control_enforcement/pid_control_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
EXCLUDED degraded_inverse_kinematics.py (archived PCC-13)
dead_mans_switch.py
  verify_dead_mans_switch_trace = {"passed": true, "violations": []}
  lambdified_margin = -1.0
monte_carlo_failure_predictor.py
  failure_probability = 0.3333333333333333
  failed_indices = [1]
  IID standard_error = 0.2721655269759087
  lambdified ratio = 0.3333333333333333
  symbolic_expression = "failures / N"
  LHS and Sobol standard errors = [null, null]
  Sobol validity warning count = 2
  signed campaign deltas = {"LHS_minus_Sobol": -0.3333333333333333, "MC_minus_LHS": 0.3333333333333333, "MC_minus_Sobol": 0.0}
  inclusive gate = true
  terminal pocket gate = false
pavlovian_reflex_state_machine.py
  compute_reflex_gate = false
  compute_next_state = "ALTERNATE"
  lambdified_gate_margin = -1.0
pid_control.py
  compute_pid_control = 7.5
  lambdified = 56.0
test_time_control_enforcement.py: 4 passed, 1 skipped
  SKIP test_degraded_inverse_kinematics_identity: PCC-13 turret aiming model excluded from validation
PASS hardware_viability/time_control_enforcement
```

<!-- end-observed-output -->

## dead_mans_switch.py

### Model context from the archive

PCC-14 — Dead Man's Switch, finite-trace temporal enforcement.

Paper law:
    □(unsafe -> ◇_{<=tau} emergency)

Runtime role:
    If unsafe state appears, emergency must occur within a hard time limit.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_margin_expression()`
- `lambdified_margin()`
- `verify_dead_mans_switch_trace(trace: Sequence[dict[str, object]], tau_s: float)`

### Original formula record

- **Formula id**  PCC-14
- **Name**  Dead Man's Switch
- **Family**  time_control_enforcement
- **Symbolic form**  `\Box(unsafe\rightarrow\Diamond_{\le\tau} emergency)`
- **Typed inputs**  `trace` (Sequence[dict]), `tau_s` (float)
- **Output**  dict
- **Units**  temporal logic result
- **Runtime class**  runtime_safe

Additional reference comparisons during migration: 5.

## pavlovian_reflex_state_machine.py

### Model context from the archive

PCC-18 — Pavlovian Reflex Gate, discrete state transition.

Paper law:
    CS_j(x,t) = 1[g_j(x,t) >= theta_j] -> q_{t+1} = delta(q_t, sigma_j)

Runtime role:
    Converts thresholded guard signals into deterministic state transitions.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_gate_expression()`
- `lambdified_gate_margin()`
- `compute_reflex_gate(guard_value: float, threshold: float)`
- `compute_next_state(current_state: str, guard_value: float, threshold: float, event: str, transitions: Mapping[tuple[str, str], str])`

### Original formula record

- **Formula id**  PCC-18
- **Name**  Pavlovian Reflex Gate
- **Family**  time_control_enforcement
- **Symbolic form**  `CS_j(x,t)=\mathbf{1}[g_j(x,t)\ge\theta_j]\rightarrow q_{t+1}=\delta(q_t,\sigma_j)`
- **Typed inputs**  `current_state` (str), `guard_value` (float), `threshold` (float), `event` (str), `transitions` (Mapping[tuple[str,str], str])
- **Output**  str
- **Units**  state
- **Runtime class**  runtime_safe

Additional reference comparisons during migration: 5.

## pid_control.py

### Model context from the archive

PCC-12 — Sniper's Breath, PID control law.

Paper law:
    u(t) = Kp e(t) + Ki integral_0^t e(tau)dTau + Kd de(t)/dt

Runtime role:
    Smooth pursuit and correction without violent overshoot.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_expression()`
- `lambdified()`
- `compute_pid_control(error: float, integral_error: float, derivative_error: float, kp: float, ki: float, kd: float)`

### Original formula record

- **Formula id**  PCC-12
- **Name**  Sniper's Breath
- **Family**  time_control_enforcement
- **Symbolic form**  `u(t)=K_p e(t)+K_i\int_0^t e(\tau)d\tau+K_d\frac{de(t)}{dt}`
- **Typed inputs**  `error` (float), `integral_error` (float), `derivative_error` (float), `kp` (float), `ki` (float), `kd` (float)
- **Output**  float
- **Units**  control effort
- **Runtime class**  runtime_safe

Additional reference comparisons during migration: 5.

## monte_carlo_failure_predictor.py

**PCC-15 · Crucible Campaign Failure Predictor.** Count a trajectory once if any of its states fails the caller’s safety predicate. Divide the count by the number of supplied trajectories. The result is a dimensionless probability. The supplied record classifies the computation as runtime-safe. An empty campaign raises `ValueError`. An empty trajectory contains no failed state.

| Entry point | Contract |
|---|---|
| `compute_failure_probability(trajectories, safe_predicate, *, campaign_type="unspecified")` | Returns a frozen `CampaignFailureResult` with failed indices, counts, estimate, estimator note, warnings, and optional standard error. It supports `to_dict()` and read access by key. |
| `compute_campaign_failure_report(campaigns, safe_predicate)` | Runs each named campaign independently. Reports retain original labels. The delta for a pair is the earlier campaign’s probability minus the later campaign’s probability in mapping iteration order. |
| `evaluate_campaign_failure_gate(campaign_report, *, failure_probability_threshold, campaign_delta_threshold=None, unmodeled_terminal_pocket_detected=False)` | Requires every probability and every checked absolute delta to be at or below its threshold. A terminal-pocket flag fails the gate. Validity warnings are included in the notes. Returns a frozen `CampaignFailureGateResult`. |
| `symbolic_expression()` and `lambdified()(failures, N)` | Return the expression text `failures / N` and evaluate the scalar ratio, respectively. |

Supplied symbolic form: `\hat{P}_{fail}=\frac{1}{N}\sum_{i=1}^{N}\mathbf{1}[\exists t:x_i(t)\notin\Omega]`.

IID Monte Carlo reports the binomial standard error `sqrt(p * (1 - p) / N)`. Latin hypercube and Sobol estimates retain their point estimates and replicate-based uncertainty guidance. Sobol also reports a warning if the sample count is not a power of two. An unspecified or unknown campaign type retains the estimate and flags its uncertainty semantics.

The supplied computational functions, estimator notes, warnings, aliases, and report identifiers were retained. The SymPy accessor now returns text, and the callable factory uses Python division. The source comparison covered 44 campaign estimates, one full report, 24 gate configurations, three scalar ratios, and five rejection cases. All 77 matched. The original three-trajectory regression is active in the local suite.

Supplied source SHA-256: `8b0d6b10d010ea3ad35a7038fa786fe8da4e9c5c5add85e51f8fbb0fdf12cd77`.
