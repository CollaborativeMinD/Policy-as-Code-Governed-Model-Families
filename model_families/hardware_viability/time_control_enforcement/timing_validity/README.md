# Timing validity

Cross-product timestamp coherence margins for geometry, environment, forecast, and sensor fusion lanes.

### Use cases

- Ephemeris plus horizon fusion.
- Forecast plus map fusion.
- GNSS/map matching, sensor timestamp alignment, and asynchronous twin services.

### Non-use cases

- Do not use across mixed timebases.
- Do not treat temporal separation as correction for the source of drift.

## Model files

- [age_of_information.py](age_of_information.py) — Age-of-information at use law
- [ephemeris_horizon_coherence_margin.py](ephemeris_horizon_coherence_margin.py) — ephemeris_horizon_coherence_margin
- [mixed_stream_temporal_coherence.py](mixed_stream_temporal_coherence.py) — Mixed-stream temporal coherence score
- [sequence_replay_integrity.py](sequence_replay_integrity.py) — Sequence/replay integrity law

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../../model_policy_engine/README.md)

- [hardware_viability/time_control_enforcement/timing_validity/age_of_information](../../../../model_policy_engine/policies/hardware_viability/time_control_enforcement/timing_validity/age_of_information_policy.toml)
- [hardware_viability/time_control_enforcement/timing_validity/ephemeris_horizon_coherence_margin](../../../../model_policy_engine/policies/hardware_viability/time_control_enforcement/timing_validity/ephemeris_horizon_coherence_margin_policy.toml)
- [hardware_viability/time_control_enforcement/timing_validity/mixed_stream_temporal_coherence](../../../../model_policy_engine/policies/hardware_viability/time_control_enforcement/timing_validity/mixed_stream_temporal_coherence_policy.toml)
- [hardware_viability/time_control_enforcement/timing_validity/sequence_replay_integrity](../../../../model_policy_engine/policies/hardware_viability/time_control_enforcement/timing_validity/sequence_replay_integrity_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
age_of_information.py
  compute_age_of_information_margin = 0.5
ephemeris_horizon_coherence_margin.py
  compute_ephemeris_horizon_coherence_margin = 0.30000000000000004
mixed_stream_temporal_coherence.py
  compute_mixed_stream_temporal_coherence_score = 0.19999999999999996
sequence_replay_integrity.py
  compute_sequence_replay_integrity_score = 0
PASS hardware_viability/time_control_enforcement/timing_validity
```

<!-- end-observed-output -->

## age_of_information.py

### Model context from the archive

T1.1 — Age-of-information at use law

Purpose
-------
Measures freshness where it matters: at the moment a decision consumes the data,
not when the packet arrived and made everyone feel optimistic for five seconds.

### Entry points

- `compute_age_of_information_margin(time_generated: float, time_used: float, freshness_limit: float)`

### Original formula record

- **Formula id**  T1.1
- **Name**  Age-of-information at use law
- **Symbolic form**  `AoI_use = t_use - t_generated ; m_fresh = T_fresh_limit - AoI_use`
- **Typed inputs**  `time_generated` (float), `time_used` (float), `freshness_limit` (float)
- **Units**  `time_generated` (s), `time_used` (s), `freshness_limit` (s), `output` (s)
- **Assumptions**  Clocks are already mapped into a common timebase or bounded offset envelope.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Primary gaps closed**  temporal coherence, telemetry trust, contested edge-network realism, hardware timing closure

## ephemeris_horizon_coherence_margin.py

### Model context from the archive

TIME-COH-001 — ephemeris_horizon_coherence_margin

Purpose
-------
Blocks stale geometry fusion before it turns into a fake-green decision.

Assumptions
-----------
Both timestamps are expressed in the same timebase.

### Entry points

- `compute_ephemeris_horizon_coherence_margin(tau_align_s: float, t_ephem_s: float, t_horizon_s: float)`

### Original formula record

- **Formula id**  TIME-COH-001
- **Family**  timing_coherence
- **Name**  ephemeris_horizon_coherence_margin
- **Symbolic form**  `m_coh = tau_align_s - abs(t_ephem_s - t_horizon_s)`
- **Typed inputs**  `tau_align_s` (float), `t_ephem_s` (float), `t_horizon_s` (float)
- **Units**  `tau_align_s` (s), `t_ephem_s` (s), `t_horizon_s` (s), `output` (s)
- **Assumptions**  Both timestamps are expressed in the same timebase.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Blocks stale geometry fusion before it turns into a fake-green decision.
- **Status**  proposed_for_future_builds

## mixed_stream_temporal_coherence.py

### Model context from the archive

T1.2 — Mixed-stream temporal coherence score

Purpose
-------
Scores whether multiple individually valid streams still belong to the same
usable moment in reality. Fresh but jointly incoherent inputs are one of the
most annoying ways to die with beautifully formatted telemetry.

### Entry points

- `compute_mixed_stream_temporal_coherence_score(timestamps: Sequence[float], max_skew: float, sequence_gap_penalty: float=0.0)`

### Original formula record

- **Formula id**  T1.2
- **Name**  Mixed-stream temporal coherence score
- **Symbolic form**  `S_tc = max(0, 1 - max_ij |t_i - t_j| / Δt_max - γ_gap * G_seq)`
- **Typed inputs**  `timestamps` (Sequence[float]), `max_skew` (float), `sequence_gap_penalty` (float)
- **Units**  `timestamps` (s), `max_skew` (s), `sequence_gap_penalty` (unitless), `output` (unitless)
- **Assumptions**  Score is clamped to [0,1]. Lower values indicate mixed-stream incoherence even when packets are individually valid.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Primary gaps closed**  mixed-stream temporal coherence, freshness at use, telemetry trust as a family, identity agreement

## sequence_replay_integrity.py

### Model context from the archive

T1.3 — Sequence/replay integrity law

Purpose
-------
Flags rollback, duplication, and replay conditions across sequence, time, and
content continuity. This is the minimal level of paranoia required for systems
living on asynchronous links where old lies often arrive wrapped as valid packets.

### Entry points

- `compute_sequence_replay_integrity_score(seq_prev: int, seq_curr: int, time_prev: float, time_curr: float, hash_prev: str, hash_curr: str, allow_duplicate_hash: bool=False)`

### Original formula record

- **Formula id**  T1.3
- **Name**  Sequence/replay integrity law
- **Symbolic form**  `I_rep = 1[seq_k <= seq_k-1] + 1[t_k <= t_k-1] + 1[h_k == h_k-1 ∧ seq changed unexpectedly]`
- **Typed inputs**  `seq_prev` (int), `seq_curr` (int), `time_prev` (float), `time_curr` (float), `hash_prev` (str), `hash_curr` (str), `allow_duplicate_hash` (bool)
- **Units**  `seq_prev` (count), `seq_curr` (count), `time_prev` (s), `time_curr` (s), `output` (count / suspicion score)
- **Assumptions**  Any positive score warrants quarantine or downgrade unless the channel explicitly allows duplicates.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Primary gaps closed**  replay resistance, timestamp rollback rejection, sequence-gap coherence, temporal provenance governance
