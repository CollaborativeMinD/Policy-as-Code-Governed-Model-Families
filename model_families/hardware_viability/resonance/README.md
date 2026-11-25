# Resonance

Resonance separation, transmissibility, preload retention, and structural survivability gates.

### Optimal use

Use when payload or platform survivability depends on vibration separation, base motion leakage, or fastener integrity.

### Do not use when

Do not use as full structural FEA or material qualification testing.

## Model files

- [Base-excitation-transmissibility.py](Base-excitation-transmissibility.py) — Base-excitation transmissibility
- [Fastener-preload-retention-margin.py](Fastener-preload-retention-margin.py) — Fastener preload retention margin
- [Resonance-separation-margin.py](Resonance-separation-margin.py) — Resonance separation margin

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../model_policy_engine/README.md)

- [hardware_viability/resonance/Base-excitation-transmissibility](../../../model_policy_engine/policies/hardware_viability/resonance/Base-excitation-transmissibility_policy.toml)
- [hardware_viability/resonance/Fastener-preload-retention-margin](../../../model_policy_engine/policies/hardware_viability/resonance/Fastener-preload-retention-margin_policy.toml)
- [hardware_viability/resonance/Resonance-separation-margin](../../../model_policy_engine/policies/hardware_viability/resonance/Resonance-separation-margin_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
Base-excitation-transmissibility.py
  compute_base_excitation_transmissibility = {"frequency_ratio": 0.8, "transmissibility": 1.3520377540143105, "transmitted_acceleration": 0.9464264278100173}
Fastener-preload-retention-margin.py
  compute_fastener_preload_retention_margin = {"joint_secure": false, "mechanical_loss": 1.1, "retained_preload": -0.6640000000000001, "retention_margin": -1.5533333333333335, "thermal_loss": -0.036}
Resonance-separation-margin.py
  compute_resonance_separation_margin = {"critical_forcing_frequency_hz": 12.0, "critical_natural_frequency_hz": 10.0, "minimum_separation_ratio": 0.16666666666666666, "required_exclusion_ratio": 0.2, "resonance_clear": false, "signed_margin": -0.033333333333333354}
  compute_resonance_separation_margin = {"critical_forcing_frequency_hz": 10.0, "critical_natural_frequency_hz": 8.0, "minimum_separation_ratio": 0.2, "required_exclusion_ratio": 0.2, "resonance_clear": true, "signed_margin": 0.0}
PASS hardware_viability/resonance
```

<!-- end-observed-output -->

## Base-excitation-transmissibility.py

### Model context from the archive

M4.1b — Base-excitation transmissibility

Classical mounting law for how much base motion leaks into a protected payload.

### Entry points

- `compute_base_excitation_transmissibility(forcing_frequency_hz: float, natural_frequency_hz: float, damping_ratio: float, base_acceleration: float)`

### Original formula record

- **Formula id**  M4.1b
- **Name**  Base-excitation transmissibility
- **Family**  Structural dynamics and mounting survivability
- **Symbolic form**  `T(r,zeta) = sqrt((1 + (2 zeta r)^2) / ((1 - r^2)^2 + (2 zeta r)^2))`
- **Typed inputs**  `forcing_frequency_hz` (float), `natural_frequency_hz` (float), `damping_ratio` (float), `base_acceleration` (float)
- **Units**  `forcing_frequency_hz` (Hz), `natural_frequency_hz` (Hz), `damping_ratio` (unitless), `base_acceleration` (m/s^2), `output` (transmissibility_dict)
- **Assumptions**  Single dominant mode, linear mount, harmonic base excitation.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype

## Fastener-preload-retention-margin.py

### Model context from the archive

M4.1c — Fastener preload retention margin

Rejects mounting stories that survive in CAD but unwind under vibration,
thermal mismatch, and external joint loading.

### Entry points

- `compute_fastener_preload_retention_margin(initial_preload: float, joint_stiffness: float, alpha_joint: float, alpha_clamped: float, grip_length: float, delta_temperature: float, external_separating_load: float, load_loss_factor: float, minimum_retained_preload: float)`

### Original formula record

- **Formula id**  M4.1c
- **Name**  Fastener preload retention margin
- **Family**  Structural dynamics and mounting survivability
- **Symbolic form**  `F_remain = F0 - k_eq*(alpha_j - alpha_c)*L*DeltaT - gamma*F_ext ; m = (F_remain - F_min)/F_min`
- **Typed inputs**  `initial_preload` (float), `joint_stiffness` (float), `alpha_joint` (float), `alpha_clamped` (float), `grip_length` (float), `delta_temperature` (float), `external_separating_load` (float), `load_loss_factor` (float), `minimum_retained_preload` (float)
- **Units**  `initial_preload` (N), `joint_stiffness` (N/m), `alpha_joint` (1/K), `alpha_clamped` (1/K), `grip_length` (m), `delta_temperature` (K), `external_separating_load` (N), `load_loss_factor` (unitless), `minimum_retained_preload` (N), `output` (preload_dict)
- **Assumptions**  First-pass retained-clamp estimate. Positive delta_temperature follows the sign convention applied by the caller.
- **Runtime class**  offline_only
- **Deployment class**  prototype

## Resonance-separation-margin.py

### Model context from the archive

M4.1a — Resonance separation margin

Measures whether dominant forcing frequencies are too close to structural
natural frequencies to trust the packaging and mounting story.

### Current interface

- The numerical implementation uses Python scalars and sequences. Vector and matrix outputs use lists and nested lists.

### Entry points

- `compute_resonance_separation_margin(natural_frequencies_hz: Sequence[float], forcing_frequencies_hz: Sequence[float], exclusion_ratio: float=0.2)`

### Original formula record

- **Formula id**  M4.1a
- **Name**  Resonance separation margin
- **Family**  Structural dynamics and mounting survivability
- **Symbolic form**  `m_sep = min_{i,j} (|f_n,i - f_exc,j| / f_exc,j) with negative margin when forcing lies inside an exclusion band`
- **Typed inputs**  `natural_frequencies_hz` (Sequence[float]), `forcing_frequencies_hz` (Sequence[float]), `exclusion_ratio` (float)
- **Units**  `natural_frequencies_hz` (Hz), `forcing_frequencies_hz` (Hz), `exclusion_ratio` (unitless), `output` (margin_dict)
- **Assumptions**  Dominant-mode screening law for early rejection. Not a replacement for full modal test or FEA.
- **Runtime class**  offline_only
- **Deployment class**  prototype

Additional reference comparisons during migration: 52.
