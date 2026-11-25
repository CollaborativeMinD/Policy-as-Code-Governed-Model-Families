# estimation_detection

Historical family notes from the supplied archive. The current filenames, interfaces, and observed working baseline are in [README.md](README.md).

**Family tail:** `README.estimation_detection.md`

## Why this family exists
Twin-vs-reality divergence, anomaly detection, linear filtering, safe fusion, IMM mode update, and delayed-measurement consistency.

## Cross-domain use cases
radar/EO track fusion; swarm state estimation; navigation drift; edge anomaly telemetry.

## Optimal use
Use for telemetry trust, sensor fusion, track management, and reality-vs-twin drift monitoring.

## Do not use when
Do not assume these cover every nonlinear or adversarial edge case without the appropriate companion law.

## Canonical formulas in this family

- **C.5** `c_5__estimation_detection__covariance_weighted_sensor_fusion.py`: Covariance-weighted sensor fusion
  - Symbolic form: `P⁻¹ = P₁⁻¹ + P₂⁻¹ ; x̂ = P(P₁⁻¹ x̂₁ + P₂⁻¹ x̂₂)`
  - Why kept: Base compendium law canonicalized for searchability.
- **M5.1** `m5_1__estimation_detection__weighted_divergence_between_reality_and_twin.py`: Weighted divergence between reality and twin
  - Symbolic form: `Δ(t) = ||x_real(t) − x_twin(t)||_W`
  - Why kept: Base compendium law canonicalized for searchability.
- **M5.1a** `m5_1a__estimation_detection__robust_multivariate_deviation_score.py`: Robust multivariate deviation score
  - Symbolic form: `D_M(x) = sqrt((x − μ)^T Σ⁻¹ (x − μ))`
  - Why kept: Base compendium law canonicalized for searchability.
- **M5.1b** `m5_1b__estimation_detection__streaming_standardized_deviation.py`: Streaming standardized deviation
  - Symbolic form: `Z_t = (x_t − μ_t) / σ_t ; μ_t = μ_{t−1} + (x_t − μ_{t−1})/t ; M_{2,t} = M_{2,t−1} + (x_t − μ_{t−1})(x_t − μ_t) ; σ_t² = M_{2,t}/(t−1)`
  - Why kept: Base compendium law canonicalized for searchability.
- **M5.2** `m5_2__estimation_detection__kalman_filter_prediction_and_update.py`: Kalman filter prediction and update
  - Symbolic form: `x̂_{k|k−1} = A x̂_{k−1|k−1} + B u_{k−1}; K_k = P Hᵀ (H P Hᵀ + R)^{-1}; x̂_{k|k} = x̂_{k|k−1} + K_k (z_k − H x̂_{k|k−1})`
  - Why kept: Base compendium law canonicalized for searchability.
- **M5.3** `m5_3__estimation_detection__unknown_correlation_safe_fusion_covariance_intersection.py`: unknown-correlation_safe_fusion_(covariance_intersection)
  - Symbolic form: `P^-1 = ω P_a^-1 + (1-ω) P_b^-1 ; x = P [ω P_a^-1 x_a + (1-ω) P_b^-1 x_b]`
  - Why kept: Critical safe-fusion primitive when cross-correlations are unknown.
- **M5.4** `m5_4__estimation_detection__imm_mode_probability_update.py`: imm_mode_probability_update
  - Symbolic form: `mu_j^+ = (likelihood_j * sum_i mu_i^- Pi_ij) / normalization`
  - Why kept: Portable maneuver-model estimation primitive.
- **M5.5** `m5_5__estimation_detection__delay_adjusted_innovation_consistency_statistic.py`: delay-adjusted_innovation_consistency_statistic
  - Symbolic form: `J = nu^T S^-1 nu * (1 + lambda_a dt/tau + lambda_s g_seq + lambda_d rho_dyn)`
  - Why kept: Needed when delayed telemetry would otherwise poison estimators.

## Underlying formula concepts

These laws are reusable starting primitives for humans, agents, and HIL operators. Pair them with timing, provenance, and authority shelves whenever the thread is mission-critical.
