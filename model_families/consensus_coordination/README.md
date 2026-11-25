# Consensus coordination

Agreement, quorum survival, and liar-node resistance under delay, loss, and partition.

### Optimal use

Use when multiple nodes or roles must agree enough to act without central certainty.

### Do not use when

Do not use as a complete tactical comms protocol or timing model.

## Model files

- [Byzantine trust-weighted agreement.py](Byzantine%20trust-weighted%20agreement.py) — Byzantine trust-weighted agreement
- [Delay-loss consensus stability.py](Delay-loss%20consensus%20stability.py) — Delay-loss consensus stability
- [Partitioned quorum survival.py](Partitioned%20quorum%20survival.py) — Partitioned quorum survival

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../model_policy_engine/README.md)

- [consensus_coordination/Byzantine trust-weighted agreement](../../model_policy_engine/policies/consensus_coordination/Byzantine%20trust-weighted%20agreement_policy.toml)
- [consensus_coordination/Delay-loss consensus stability](../../model_policy_engine/policies/consensus_coordination/Delay-loss%20consensus%20stability_policy.toml)
- [consensus_coordination/Partitioned quorum survival](../../model_policy_engine/policies/consensus_coordination/Partitioned%20quorum%20survival_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
Byzantine trust-weighted agreement.py
  compute_byzantine_trust_weighted_agreement = [0.7777777777777778, 0.8]
  compute_byzantine_trust_weighted_agreement rejected invalid input
Delay-loss consensus stability.py
  compute_delay_loss_consensus_stability = 0.005794642780094374
Partitioned quorum survival.py
  compute_partitioned_quorum_survival = 0.6000000000000001
PASS consensus_coordination
```

<!-- end-observed-output -->

## Byzantine trust-weighted agreement.py

### Model context from the archive

N1.3 — Byzantine trust-weighted agreement

Robust agreement score around a trust-weighted median estimate. It
suppresses liar-node influence better than a plain average while
remaining cheap enough for edge screening.

Symbolic form
-------------
    A_byz = 1 - (sum_i w_i * |x_i - x_hat|) / (sum_i w_i * delta)
    x_hat = weighted_median(x, w)

### Current interface

- The numerical implementation uses Python scalars and sequences. Vector and matrix outputs use lists and nested lists.

### Entry points

- `compute_byzantine_trust_weighted_agreement(values: Sequence[float], trust_weights: Sequence[float], tolerance: float, eps: float=1e-09)`

### Original formula record

- **Formula id**  N1.3
- **Name**  Byzantine trust-weighted agreement
- **Family**  contested_edge_networks
- **Symbolic form**  `A_byz = 1 - (sum_i w_i * |x_i - x_hat|) / (sum_i w_i * delta); x_hat = weighted_median(x, w)`
- **Typed inputs**  `values` (Sequence[float]), `trust_weights` (Sequence[float]), `tolerance` (float)
- **Units**  `values` (domain units), `trust_weights` (unitless), `tolerance` (domain units), `output` (unitless)
- **Assumptions**  Trust weights are non-negative and already encode upstream telemetry, provenance, or role trust.
- **Recommended runtime class**  runtime_safe
- **Recommended deployment class**  prototype
- **Blindspots hit**  contested edge-network realism, liar-node resistance, bounded human or agent cognition under disagreement, telemetry trust

Additional reference comparisons during migration: 51.

## Delay-loss consensus stability.py

### Model context from the archive

N1.1 — Delay-loss consensus stability

Simple contested-network law for degrading consensus strength as delay,
loss, and jitter worsen.

Symbolic form
-------------
    S_cons = lambda2 * exp(-tau_net / tau_cons) * (1 - p_loss) * (1 - min(j / j_max, 1))

### Entry points

- `compute_delay_loss_consensus_stability(algebraic_connectivity: float, network_delay_s: float, consensus_time_constant_s: float, loss_probability: float, network_jitter_s: float, jitter_budget_s: float)`

### Original formula record

- **Formula id**  N1.1
- **Name**  Delay-loss consensus stability
- **Family**  contested_edge_networks
- **Symbolic form**  `S_cons = lambda2 * exp(-tau_net / tau_cons) * (1 - p_loss) * (1 - min(j / j_max, 1))`
- **Typed inputs**  `algebraic_connectivity` (float), `network_delay_s` (float), `consensus_time_constant_s` (float), `loss_probability` (float), `network_jitter_s` (float), `jitter_budget_s` (float)
- **Units**  `algebraic_connectivity` (unitless), `network_delay_s` (s), `consensus_time_constant_s` (s), `loss_probability` (unitless), `network_jitter_s` (s), `jitter_budget_s` (s), `output` (unitless)
- **Assumptions**  Algebraic connectivity is derived from the active graph. The law is intentionally compact for edge runtime screening, not final certification.
- **Recommended runtime class**  runtime_safe
- **Recommended deployment class**  prototype
- **Blindspots hit**  contested edge-network realism, consensus under delay and loss, swarm coordination, relay mesh survivability

## Partitioned quorum survival.py

### Model context from the archive

N1.2 — Partitioned quorum survival

Determines whether any surviving partition still holds enough trusted
authority weight to continue lawful action.

Symbolic form
-------------
    Q_survive = max_k(W_auth,k) / W_quorum - 1

### Entry points

- `compute_partitioned_quorum_survival(partition_authority_weights: Sequence[float], quorum_threshold_weight: float)`

### Original formula record

- **Formula id**  N1.2
- **Name**  Partitioned quorum survival
- **Family**  contested_edge_networks
- **Symbolic form**  `Q_survive = max_k(W_auth,k) / W_quorum - 1`
- **Typed inputs**  `partition_authority_weights` (Sequence[float]), `quorum_threshold_weight` (float)
- **Units**  `partition_authority_weights` (authority weight), `quorum_threshold_weight` (authority weight), `output` (unitless)
- **Assumptions**  Each partition weight already excludes dead, revoked, or untrusted members. Positive output means at least one lawful partition still exists.
- **Recommended runtime class**  runtime_safe
- **Recommended deployment class**  prototype
- **Blindspots hit**  contested edge-network realism, authority seams, swarm under partition, custody transfer or quorum collapse
