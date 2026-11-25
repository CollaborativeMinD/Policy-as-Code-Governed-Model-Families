# consensus_coordination

Historical family notes from the supplied archive. The current filenames, interfaces, and observed working baseline are in [README.md](README.md).

**Family tail:** `README.consensus_coordination.md`

## Why this family exists
Agreement, quorum survival, and liar-node resistance under delay, loss, and partition.

## Cross-domain use cases
drone swarm task agreement; distributed tracking; multi-ship route consensus; autonomous relay coordination.

## Optimal use
Use when multiple nodes or roles must agree enough to act without central certainty.

## Do not use when
Do not use as a complete tactical comms protocol or timing model.

## Canonical formulas in this family

- **CONS-COORD-003** `cons_coord_003__consensus_coordination__delay_loss_consensus_stability.py`: Delay-loss consensus stability
  - Symbolic form: `S_cons = lambda2 * exp(-tau_net / tau_cons) * (1 - p_loss) * (1 - min(j / j_max, 1))`
  - Why kept: Needed for contested or degraded networks.
  - Merged from: M2-6-DELAY-LOSS-JAM-CONSENSUS-MARGIN, M2-6A-DELAY-LOSS-PARTITION-CONSENSUS-VIABILITY, PROP-M2.6_delay_loss_aware_consensus_contraction_margin
- **CONS-COORD-004** `cons_coord_004__consensus_coordination__partitioned_quorum_survival.py`: Partitioned quorum survival
  - Symbolic form: `Q_survive = max_k(W_auth,k) / W_quorum - 1`
  - Why kept: Useful across swarms, relays, and distributed autonomy.
  - Merged from: CONS-COORD-002
- **CONS-COORD-005** `cons_coord_005__consensus_coordination__byzantine_trust_weighted_agreement.py`: Byzantine trust-weighted agreement
  - Symbolic form: `A_byz = 1 - (sum_i w_i * |x_i - x_hat|) / (sum_i w_i * delta); x_hat = weighted_median(x, w)`
  - Why kept: Captures liar-node resilience without mission-specific baggage.
- **M2.5** `m2_5__consensus_coordination__consensus_dynamics_over_graph_topology.py`: Consensus dynamics over graph topology
  - Symbolic form: `ẋ = −L x ; discrete: x_(k+1) = x_k − α L x_k`
  - Why kept: Base compendium law canonicalized for searchability.
- **M9.3** `m9_3__consensus_coordination__multi_agent_consensus_gate.py`: Multi-agent consensus gate
  - Symbolic form: `C(y₁, …, y_n) = 1[score(y₁, …, y_n) ≥ α]`
  - Why kept: Base compendium law canonicalized for searchability.

## Underlying formula concepts

These laws are reusable starting primitives for humans, agents, and HIL operators. Pair them with timing, provenance, and authority shelves whenever the thread is mission-critical.
