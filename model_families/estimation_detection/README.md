# Estimation detection

Twin-vs-reality divergence, anomaly detection, linear filtering, safe fusion, IMM mode update, and delayed-measurement consistency.

### Optimal use

Use for telemetry trust, sensor fusion, track management, and reality-vs-twin drift monitoring.

### Do not use when

Do not assume these cover every nonlinear or adversarial edge case without the appropriate companion law.

## Subdirectories

- [truth_sensor_fusion](truth_sensor_fusion/README.md)

## Model files

- [chi_hardware_coefficient.py](chi_hardware_coefficient.py) — Hardware Coefficient
- [chi_squared_reality_gap_monitor.py](chi_squared_reality_gap_monitor.py) — Reality Gap Monitor
- [delay-adjusted-innovation-consistency.py](delay-adjusted-innovation-consistency.py) — Delay-Adjusted Innovation Consistency Statistic
- [IMM-mode-probability-update.py](IMM-mode-probability-update.py) — IMM Mode Probability Update
- [kalman_filter.py](kalman_filter.py) — Kalman filter prediction and update
- [mahalanobis.py](mahalanobis.py) — Robust multivariate deviation score
- [streaming_deviation.py](streaming_deviation.py) — Streaming standardized deviation
- [unknown-correlation-safe-fusion.py](unknown-correlation-safe-fusion.py) — Unknown-Correlation Safe Fusion (Covariance Intersection)
- [weighted_divergence.py](weighted_divergence.py) — Weighted divergence between reality and twin
- [z_score_universal_stress_metric.py](z_score_universal_stress_metric.py) — Universal Stress Metric

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../model_policy_engine/README.md)

- [estimation_detection/chi_hardware_coefficient](../../model_policy_engine/policies/estimation_detection/chi_hardware_coefficient_policy.toml)
- [estimation_detection/chi_squared_reality_gap_monitor](../../model_policy_engine/policies/estimation_detection/chi_squared_reality_gap_monitor_policy.toml)
- [estimation_detection/delay-adjusted-innovation-consistency](../../model_policy_engine/policies/estimation_detection/delay-adjusted-innovation-consistency_policy.toml)
- [estimation_detection/IMM-mode-probability-update](../../model_policy_engine/policies/estimation_detection/IMM-mode-probability-update_policy.toml)
- [estimation_detection/kalman_filter](../../model_policy_engine/policies/estimation_detection/kalman_filter_policy.toml)
- [estimation_detection/mahalanobis](../../model_policy_engine/policies/estimation_detection/mahalanobis_policy.toml)
- [estimation_detection/streaming_deviation](../../model_policy_engine/policies/estimation_detection/streaming_deviation_policy.toml)
- [estimation_detection/unknown-correlation-safe-fusion](../../model_policy_engine/policies/estimation_detection/unknown-correlation-safe-fusion_policy.toml)
- [estimation_detection/weighted_divergence](../../model_policy_engine/policies/estimation_detection/weighted_divergence_policy.toml)
- [estimation_detection/z_score_universal_stress_metric](../../model_policy_engine/policies/estimation_detection/z_score_universal_stress_metric_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
chi_hardware_coefficient.py
  compute_hardware_coefficient = 0.44559760983162217
  lambdified = 0.4569895542260725
chi_squared_reality_gap_monitor.py
  compute_chi_squared_gap = 0.0
  lambdified = 0.3333333333333333
delay-adjusted-innovation-consistency.py
  compute_delay_adjusted_innovation_consistency = 5.27027027027027
IMM-mode-probability-update.py
  compute_imm_mode_probability_update = [0.7913043478260869, 0.20869565217391306]
  compute_imm_mode_probability_update = [0.5, 0.5]
  compute_imm_mode_probability_update rejected invalid input
kalman_filter.py
  kalman_predict_update = [[3.861111111111111, 2.7777777777777777], [[0.4305555555555554, 0.13888888888888884], [0.13888888888888884, 0.8222222222222223]]]
  kalman_predict_update rejected invalid input
mahalanobis.py
  compute_mahalanobis_distance = 2.078847767442581
  compute_mahalanobis_distance rejected invalid input
streaming_deviation.py
  update_streaming_deviation = [0.475, 0.6074999999999999, -0.16666666666666657]
unknown-correlation-safe-fusion.py
  compute_covariance_intersection = [[1.985672049124403, 1.19103934500796], [[2.498294291562429, 0.02274277916761428], [0.022742779167614285, 1.3634296110984763]]]
  compute_covariance_intersection rejected invalid input
weighted_divergence.py
  compute_weighted_divergence = 2.5298221281347035
z_score_universal_stress_metric.py
  compute_z_score = -0.04999999999999999
  lambdified = -0.25
PASS estimation_detection
```

<!-- end-observed-output -->

## chi_hardware_coefficient.py

### Model context from the archive

PCC-05 — Hardware Coefficient, composite mission vector.

Paper law:
    chi = (T_cpu/T_max * L_cpu/L_max * M_mem/M_max) * S(Z)

Runtime role:
    Models nonlinear cascading hardware pressure and gates whether a node should detach or derate.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.
- The absent decision-gate helper was replaced by the logistic function specified by this module’s original symbolic expression.

### Entry points

- `compute_sigmoid(value: float)`
- `symbolic_expression()`
- `lambdified()`
- `compute_hardware_coefficient(cpu_temp: float, cpu_temp_max: float, cpu_load: float, cpu_load_max: float, memory_used: float, memory_max: float, anomaly_z: float)`

### Original formula record

- **Formula id**  PCC-05
- **Name**  Hardware Coefficient
- **Family**  state_validation_anomaly_detection
- **Symbolic form**  `\chi=\left(\frac{T_{cpu}}{T_{max}}\frac{L_{cpu}}{L_{max}}\frac{M_{mem}}{M_{max}}\right)S(Z)`
- **Typed inputs**  `cpu_temp` (float), `cpu_temp_max` (float), `cpu_load` (float), `cpu_load_max` (float), `memory_used` (float), `memory_max` (float), `anomaly_z` (float)
- **Output**  float
- **Units**  unitless pressure
- **Runtime class**  runtime_safe

Additional reference comparisons during migration: 5.

## chi_squared_reality_gap_monitor.py

### Model context from the archive

PCC-02 — Reality Gap Monitor, chi-squared residual law.

Paper law:
    chi^2 = sum((O - E)^2 / E)

Runtime role:
    Measures total friction between expected digital twin behavior and observed hardware.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_expression()`
- `lambdified()`
- `compute_chi_squared_gap(observed: Sequence[float], expected: Sequence[float])`

### Original formula record

- **Formula id**  PCC-02
- **Name**  Reality Gap Monitor
- **Family**  state_validation_anomaly_detection
- **Symbolic form**  `\chi^2=\sum_i\frac{(O_i-E_i)^2}{E_i}`
- **Typed inputs**  `observed` (Sequence[float]), `expected` (Sequence[float])
- **Output**  float
- **Units**  unitless residual
- **Runtime class**  runtime_safe

Additional reference comparisons during migration: 5.

## delay-adjusted-innovation-consistency.py

### Model context from the archive

Proposed formula M5.5 — Delay-Adjusted Innovation Consistency Statistic.

Purpose:
    Upgrade the standard innovation consistency test by penalizing delayed, sequence-gapped,
    or dynamically stale measurements before acceptance.

Symbolic form:
    J_daic = ν^T S^-1 ν * [1 + λ_a Δt/τ + λ_s g_seq + λ_d ρ_dyn]

### Current interface

- The numerical implementation uses Python scalars and sequences. Vector and matrix outputs use lists and nested lists.

### Entry points

- `compute_delay_adjusted_innovation_consistency(residual: Iterable[float], innovation_covariance: Iterable[Iterable[float]], measurement_age_s: float, cadence_s: float, sequence_gap: int=0, dynamic_staleness: float=0.0, lambda_age: float=1.0, lambda_seq: float=0.5, lambda_dyn: float=1.0)`

### Original formula record

- **Formula id**  M5.5
- **Name**  Delay-Adjusted Innovation Consistency Statistic
- **Family**  estimation_detection
- **Symbolic form**  `J = nu^T S^-1 nu * (1 + lambda_a dt/tau + lambda_s g_seq + lambda_d rho_dyn)`
- **Typed inputs**  `residual` (ArrayLike[float]), `innovation_covariance` (ArrayLike[float]), `measurement_age_s` (float), `cadence_s` (float), `sequence_gap` (int), `dynamic_staleness` (float)
- **Units**  `residual` (measurement units), `innovation_covariance` (measurement units^2), `measurement_age_s` (s), `cadence_s` (s), `sequence_gap` (count), `dynamic_staleness` (unitless), `output` (unitless)
- **Assumptions**  Innovation covariance is positive definite. dynamic_staleness is a normalized mismatch term reflecting how badly recent dynamics invalidate old measurements.
- **Proposed runtime class**  candidate_runtime_safe
- **Proposed deployment class**  candidate_prototype
- **Strengthens**  temporal coherence, delayed telemetry logic, innovation gating, plant realism

Additional reference comparisons during migration: 51.

## IMM-mode-probability-update.py

### Model context from the archive

Proposed formula M5.4 — IMM Mode Probability Update.

Purpose:
    Update maneuver-mode probabilities for a Markov-switching estimator bank.

Symbolic form:
    c̄_j = Σ_i μ_i^- Π_ij
    μ_j^+ = [Λ_j c̄_j] / [Σ_k Λ_k c̄_k]

### Current interface

- The numerical implementation uses Python scalars and sequences. Vector and matrix outputs use lists and nested lists.

### Entry points

- `compute_imm_mode_probability_update(mode_probabilities: Iterable[float], transition_matrix: Iterable[Iterable[float]], likelihoods: Iterable[float])`

### Original formula record

- **Formula id**  M5.4
- **Name**  IMM Mode Probability Update
- **Family**  estimation_detection
- **Symbolic form**  `mu_j^+ = (likelihood_j * sum_i mu_i^- Pi_ij) / normalization`
- **Typed inputs**  `mode_probabilities` (ArrayLike[float]), `transition_matrix` (ArrayLike[float]), `likelihoods` (ArrayLike[float])
- **Units**  `all_inputs` (unitless probabilities or likelihoods), `output` (unitless probabilities)
- **Assumptions**  Transition matrix is row-stochastic, likelihoods are nonnegative, and all entries correspond to the same ordered mode bank.
- **Proposed runtime class**  candidate_runtime_safe
- **Proposed deployment class**  candidate_prototype
- **Strengthens**  maneuver-class tracking, plant fidelity, hostile telemetry realism

Additional reference comparisons during migration: 52.

## kalman_filter.py

### Model context from the archive

M5.2 — Kalman filter prediction and update

This module implements the discrete linear Kalman filter with prediction
and update steps:

    x̂_{k|k−1} = A x̂_{k−1|k−1} + B u_{k−1}
    P_{k|k−1} = A P_{k−1|k−1} Aᵀ + Q
    K_k = P_{k|k−1} Hᵀ (H P_{k|k−1} Hᵀ + R)^{-1}
    x̂_{k|k} = x̂_{k|k−1} + K_k (z_k − H x̂_{k|k−1})
    P_{k|k} = (I − K_k H) P_{k|k−1}.

The filter assumes additive process noise ``Q`` and measurement noise ``R``.

### Current interface

- The numerical implementation uses Python scalars and sequences. Vector and matrix outputs use lists and nested lists.

### Entry points

- `kalman_predict_update(A: Sequence[Sequence[float]], B: Sequence[Sequence[float]], H: Sequence[Sequence[float]], x_prev: Sequence[float], P_prev: Sequence[Sequence[float]], u_prev: Sequence[float], z_k: Sequence[float], Q: Sequence[Sequence[float]], R: Sequence[Sequence[float]])`

### Original formula record

- **Formula id**  M5.2
- **Name**  Kalman filter prediction and update
- **Symbolic form**  `x̂_{k|k−1} = A x̂_{k−1|k−1} + B u_{k−1}; K_k = P Hᵀ (H P Hᵀ + R)^{-1}; x̂_{k|k} = x̂_{k|k−1} + K_k (z_k − H x̂_{k|k−1})`
- **Typed inputs**  `A` (Sequence[Sequence[float]]), `B` (Sequence[Sequence[float]]), `H` (Sequence[Sequence[float]]), `x_prev` (Sequence[float]), `P_prev` (Sequence[Sequence[float]]), `u_prev` (Sequence[float]), `z_k` (Sequence[float]), `Q` (Sequence[Sequence[float]]), `R` (Sequence[Sequence[float]])
- **Units**  `A` (unitless), `B` (unitless), `H` (unitless), `x_prev` (state), `P_prev` (state²), `u_prev` (control), `z_k` (measurement), `Q` (state²), `R` (measurement²), `output` (tuple)
- **Assumptions**  Matrices have compatible dimensions.  Q and R are positive semi‑definite.
- **Runtime class**  offline_only
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_kalman_filter.py::test_kalman_filter`, `rtm_link=lambda_laws.kalman_filter`, `ssot_gate=notebooks/gate_kalman_filter.ipynb`

Additional reference comparisons during migration: 51.

## mahalanobis.py

### Model context from the archive

M5.1a — Robust multivariate deviation score

This module computes the Mahalanobis distance between a sample vector
``x`` and a distribution with mean ``μ`` and covariance matrix ``Σ``:

    D_M(x) = sqrt((x − μ)^T Σ⁻¹ (x − μ)).

The Mahalanobis distance scales the deviation by the covariance
structure, providing a dimensionless measure of deviation.  It is
useful for anomaly detection and outlier scoring.

### Current interface

- The numerical implementation uses Python scalars and sequences. Vector and matrix outputs use lists and nested lists.

### Entry points

- `compute_mahalanobis_distance(x: Sequence[float], mu: Sequence[float], Sigma: Sequence[Sequence[float]])`

### Original formula record

- **Formula id**  M5.1a
- **Name**  Robust multivariate deviation score
- **Symbolic form**  `D_M(x) = sqrt((x − μ)^T Σ⁻¹ (x − μ))`
- **Typed inputs**  `x` (Sequence[float]), `mu` (Sequence[float]), `Sigma` (Sequence[Sequence[float]])
- **Units**  `x` (unit), `mu` (unit), `Sigma` (unit²), `output` (unitless)
- **Assumptions**  Sigma must be positive definite and match the dimension of x and mu.
- **Runtime class**  offline_only
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_mahalanobis.py::test_mahalanobis_distance`, `rtm_link=lambda_laws.mahalanobis`, `ssot_gate=notebooks/gate_mahalanobis.ipynb`

Additional reference comparisons during migration: 52.

## streaming_deviation.py

### Model context from the archive

M5.1b — Streaming standardized deviation

This module implements incremental computation of the mean, second
moment, and standardized deviation (z‑score) in a streaming context.  The
update formulas are:

    μ_t = μ_{t−1} + (x_t − μ_{t−1}) / t
    M_{2,t} = M_{2,t−1} + (x_t − μ_{t−1}) (x_t − μ_t)
    σ_t² = M_{2,t} / (t − 1)  (for t > 1)
    Z_t = (x_t − μ_t) / σ_t.

When ``t`` = 1, the variance is undefined and ``Z_t`` returns 0.

### Entry points

- `update_streaming_deviation(x_t: float, mu_prev: float, M2_prev: float, t: int)`

### Original formula record

- **Formula id**  M5.1b
- **Name**  Streaming standardized deviation
- **Symbolic form**  `Z_t = (x_t − μ_t) / σ_t ; μ_t = μ_{t−1} + (x_t − μ_{t−1})/t ; M_{2,t} = M_{2,t−1} + (x_t − μ_{t−1})(x_t − μ_t) ; σ_t² = M_{2,t}/(t−1)`
- **Typed inputs**  `x_t` (float), `mu_prev` (float), `M2_prev` (float), `t` (int)
- **Units**  `x_t` (unit), `mu_prev` (unit), `M2_prev` (unit²), `t` (), `output` (tuple)
- **Assumptions**  t ≥ 1.  For t = 1, the variance is undefined and Z_t is set to 0.
- **Runtime class**  offline_only
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_streaming_deviation.py::test_streaming_deviation`, `rtm_link=lambda_laws.streaming_deviation`, `ssot_gate=notebooks/gate_streaming_deviation.ipynb`

## unknown-correlation-safe-fusion.py

### Model context from the archive

Proposed formula M5.3 — Unknown-Correlation Safe Fusion (Covariance Intersection).

Purpose:
    Fuse two estimates of a shared state without requiring knowledge of their cross-correlation.

Symbolic form:
    P_CI^-1 = ω P_a^-1 + (1-ω) P_b^-1
    x_CI = P_CI [ω P_a^-1 x_a + (1-ω) P_b^-1 x_b]

### Current interface

- The numerical implementation uses Python scalars and sequences. Vector and matrix outputs use lists and nested lists.

### Entry points

- `compute_covariance_intersection(x_a: Iterable[float], p_a: Iterable[Iterable[float]], x_b: Iterable[float], p_b: Iterable[Iterable[float]], omega: float=0.5)`

### Original formula record

- **Formula id**  M5.3
- **Name**  Unknown-Correlation Safe Fusion (Covariance Intersection)
- **Family**  estimation_detection
- **Symbolic form**  `P^-1 = ω P_a^-1 + (1-ω) P_b^-1 ; x = P [ω P_a^-1 x_a + (1-ω) P_b^-1 x_b]`
- **Typed inputs**  `x_a` (ArrayLike[float]), `p_a` (ArrayLike[float]), `x_b` (ArrayLike[float]), `p_b` (ArrayLike[float]), `omega` (float in [0,1])
- **Units**  `x_a` (state units), `p_a` (state units^2), `x_b` (state units), `p_b` (state units^2), `omega` (unitless), `output_state` (state units), `output_covariance` (state units^2)
- **Assumptions**  Covariance matrices are symmetric positive definite and describe estimates of the same state.
- **Proposed runtime class**  candidate_runtime_safe
- **Proposed deployment class**  candidate_prototype
- **Strengthens**  telemetry trust, estimation under hidden correlation, multi-agent fusion realism, truth ceilings

Additional reference comparisons during migration: 52.

## weighted_divergence.py

### Model context from the archive

M5.1 — Weighted divergence between reality and twin

This module computes the weighted divergence between the real system
state and its digital twin:

    Δ(t) = ||x_real(t) − x_twin(t)||_W,

where ``||v||_W = sqrt(vᵀ W v)`` and ``W`` is a positive semi‑definite
weighting matrix.  The divergence quantifies the difference between
real and simulated trajectories.

### Current interface

- The numerical implementation uses Python scalars and sequences. Vector and matrix outputs use lists and nested lists.

### Entry points

- `compute_weighted_divergence(x_real: Sequence[float], x_twin: Sequence[float], W: Sequence[Sequence[float]])`

### Original formula record

- **Formula id**  M5.1
- **Name**  Weighted divergence between reality and twin
- **Symbolic form**  `Δ(t) = ||x_real(t) − x_twin(t)||_W`
- **Typed inputs**  `x_real` (Sequence[float]), `x_twin` (Sequence[float]), `W` (Sequence[Sequence[float]])
- **Units**  `x_real` (state), `x_twin` (state), `W` (unitless), `output` (state)
- **Assumptions**  W must be positive semi‑definite and dimensions must match x_real and x_twin.
- **Runtime class**  offline_only
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_weighted_divergence.py::test_weighted_divergence`, `rtm_link=lambda_laws.weighted_divergence`, `ssot_gate=notebooks/gate_weighted_divergence.ipynb`

Additional reference comparisons during migration: 51.

## z_score_universal_stress_metric.py

### Model context from the archive

PCC-01 — Universal Stress Metric, Z-score.

Paper law:
    Z = (x_live - mu_baseline) / sigma_baseline

Runtime role:
    Converts noisy telemetry into standard deviations from baseline.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_expression()`
- `lambdified()`
- `compute_z_score(x_live: float, mu_baseline: float, sigma_baseline: float)`

### Original formula record

- **Formula id**  PCC-01
- **Name**  Universal Stress Metric
- **Family**  state_validation_anomaly_detection
- **Symbolic form**  `Z=\frac{x_{live}-\mu_{baseline}}{\sigma_{baseline}}`
- **Typed inputs**  `x_live` (float), `mu_baseline` (float), `sigma_baseline` (float)
- **Output**  float
- **Units**  standard deviations
- **Runtime class**  runtime_safe

Additional reference comparisons during migration: 5.
