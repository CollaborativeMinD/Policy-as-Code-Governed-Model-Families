# Thermal cross domain models

### Claim boundary

These are reduced-order thermal support laws. They are runtime-safe candidates, not certification-grade thermal models. They require calibration and substrate evidence before mission promotion.

## Subdirectories

- [power_thermal_coupling](power_thermal_coupling/README.md)
- [thermal_environment_validity](thermal_environment_validity/README.md)
- [thermal_rc_envelope](thermal_rc_envelope/README.md)
- [thermal_telemetry_governance](thermal_telemetry_governance/README.md)
- [thermal_timing_authority](thermal_timing_authority/README.md)

## Admitted model policies

This directory runs fixtures for the models in the linked family directories. Each model owns its policy. The smoke run provisions the shipped settings. [Policy setup and publication](../../../../../model_policy_engine/README.md)

## Working baseline

Run `python smoke_test.py` in this directory. This directory aggregates the child runners.

<!-- observed-output -->

```text
conversion_loss_temperature_margin.py
  compute_conversion_loss_temperature_margin = 45.0
  lambdified = 18.200000000000003
duty_cycle_temperature_margin.py
  compute_duty_cycle_temperature_margin = 35.0
  lambdified = -21.0
effective_duty_cycle_power.py
  compute_effective_duty_cycle_power = 15.0
  lambdified_2term = 44.0
test_power_thermal_coupling.py: 3 passed, 0 skipped
PASS hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/power_thermal_coupling
cooling_assumption_mismatch_margin.py
  compute_cooling_assumption_mismatch_margin = 0.5
  lambdified = 1.0
test_thermal_environment_validity.py: 1 passed, 0 skipped
PASS hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_environment_validity
cooldown_time_to_rearm.py
  compute_cooldown_time_to_rearm = 78.84573603642701
  lambdified = 78.84573603642701
equilibrium_temperature_under_load.py
  compute_equilibrium_temperature_under_load = 45.0
  lambdified = 14.0
time_to_temperature_threshold.py
  compute_time_to_temperature_threshold = 87.54687373538998
  lambdified = 87.54687373538998
  compute_time_to_temperature_threshold = Infinity
test_thermal_rc_envelope.py: 3 passed, 0 skipped
PASS hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_rc_envelope
freshness_at_use_margin.py
  compute_freshness_at_use_margin = 3.0
  lambdified = 5.0
multisensor_consistency_margin.py
  compute_multisensor_consistency_margin = 2.0
  lambdified = -1.0
sampling_observability_margin.py
  compute_sampling_observability_margin = 5.0
  lambdified = -2.5
slew_rate_plausibility_margin.py
  compute_slew_rate_plausibility_margin = 1.0
  lambdified = 4.75
test_thermal_telemetry_governance.py: 4 passed, 0 skipped
PASS hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_telemetry_governance
clock_derate_fraction.py
  compute_clock_derate_fraction = 0.75
  lambdified_unclipped = 6.0
deadline_margin_under_derate.py
  compute_deadline_margin_under_derate = 0.0
  lambdified = 1.25
recovery_hysteresis_margin.py
  compute_recovery_hysteresis_margin = 5.0
  lambdified = 1.0
thermal_authority_scale.py
  compute_thermal_authority_scale = 0.2
test_thermal_timing_authority.py: 4 passed, 0 skipped
PASS hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_timing_authority
PASS hardware_viability/thermal/thermal_truth/thermal_cross_domain_models
```

<!-- end-observed-output -->
