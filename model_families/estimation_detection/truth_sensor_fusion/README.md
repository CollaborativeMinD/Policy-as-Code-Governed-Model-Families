# Truth sensor fusion

### Use cases

Use this set when model predictions and live sensor evidence disagree, or when a new alarm must be weighted against prior truth.

Examples:

- sensor fusion and covariance-based correction,
- false-positive suppression,
- intelligence/telemetry belief updates,
- COP truth arbitration.

### Non-use cases

Do not use this set as:

- a full nonlinear estimator,
- a replacement for EKF/UKF/particle filtering where nonlinear dynamics dominate,
- a truth engine without calibrated noise parameters,
- a substitute for sensor provenance validation.

## Model files

- [ground_truth_arbitrator.py](ground_truth_arbitrator.py) — Ground Truth Arbitrator
- [intelligence_update.py](intelligence_update.py) — Intelligence Update

## Regression suites

- [test_truth_sensor_fusion.py](test_truth_sensor_fusion.py)

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../model_policy_engine/README.md)

- [estimation_detection/truth_sensor_fusion/ground_truth_arbitrator](../../../model_policy_engine/policies/estimation_detection/truth_sensor_fusion/ground_truth_arbitrator_policy.toml)
- [estimation_detection/truth_sensor_fusion/intelligence_update](../../../model_policy_engine/policies/estimation_detection/truth_sensor_fusion/intelligence_update_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
ground_truth_arbitrator.py
  compute_scalar_kalman_update = {"innovation": 2.0, "kalman_gain": 0.5, "p_new": 1.0, "p_predict": 2.0, "x_new": 11.0, "x_predict": 10.0}
  lambdified_update = -16.0
intelligence_update.py
  compute_bayes_posterior = 0.30000000000000004
  lambdified = 1.5
test_truth_sensor_fusion.py: 2 passed, 0 skipped
PASS estimation_detection/truth_sensor_fusion
```

<!-- end-observed-output -->

## ground_truth_arbitrator.py

### Model context from the archive

PCC-06 — Ground Truth Arbitrator, scalar Kalman filter.

Paper law:
    Predict: x_predict = F*x_previous + B*u
    Update:  x_new = x_predict + K*(z_sensor - H*x_predict)

Runtime role:
    Dynamically weighs the physics model against the jitter/noise of live sensor truth.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_expression_update()`
- `lambdified_update()`
- `compute_scalar_kalman_update(x_previous: float, p_previous: float, control: float, sensor: float, F: float=1.0, B: float=0.0, H: float=1.0, Q: float=0.0, R: float=1.0)`

### Original formula record

- **Formula id**  PCC-06
- **Name**  Ground Truth Arbitrator
- **Family**  truth_sensor_fusion
- **Symbolic form**  `x_{pred}=Fx_{prev}+Bu;\quad x_{new}=x_{pred}+K(z-Hx_{pred})`
- **Typed inputs**  `x_previous` (float), `p_previous` (float), `control` (float), `sensor` (float), `F` (float), `B` (float), `H` (float), `Q` (float), `R` (float)
- **Output**  dict
- **Units**  state units
- **Runtime class**  runtime_safe

Additional reference comparisons during migration: 5.

## intelligence_update.py

### Model context from the archive

PCC-07 — Intelligence Update, Bayes theorem.

Paper law:
    P(A|B) = P(B|A) P(A) / P(B)

Runtime role:
    Weighs a new alarm against prior belief to suppress panic and false positives.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_expression()`
- `lambdified()`
- `compute_bayes_posterior(p_b_given_a: float, p_a: float, p_b: float)`

### Original formula record

- **Formula id**  PCC-07
- **Name**  Intelligence Update
- **Family**  truth_sensor_fusion
- **Symbolic form**  `P(A|B)=\frac{P(B|A)P(A)}{P(B)}`
- **Typed inputs**  `p_b_given_a` (float), `p_a` (float), `p_b` (float)
- **Output**  float
- **Units**  probability
- **Runtime class**  runtime_safe

Additional reference comparisons during migration: 5.
