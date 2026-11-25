# Model families

The collection contains independently executable Python model files grouped by their original family. Use the directory links for formulas, inputs, assumptions, migration details, and observed output.

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../model_policy_engine/README.md)

- [base](../model_policy_engine/policies/base_policy.toml)
- [bounded_disturbance_admission](../model_policy_engine/policies/bounded_disturbance_admission_policy.toml)

The catalog covers 132 computational models and the base metadata types. Ordinary calls require an initialized policy deployment. The separately supplied campaign predictor and actuation solver each have their own policy. The two archived coverage exceptions are detailed below.

The 1.0.1 review records which public calls ran, which policies reached those calls, and which formulas have fresh independent numerical checks. [Verification report](../verification/Review.md)

## Running the collection

From this directory run `python smoke_test.py --tree`. Each runner disables site packages, uses a disposable policy deployment and executes the local models with the shared engine available. The working baselines were recorded on CPython 3.14.3. The smoke runners use `contextlib.chdir` and require Python 3.11 or later.

## Reference and parity

Input archive SHA-256 `323b50bf085820f86e853b6f414638208f75952dfbdc3cba13e637db96ef9752`. The migration retains the source tree and filenames. The dependency audit included static imports inside functions and the isolated execution of each migrated module. Directory smoke runners and regression suites are test infrastructure and explicitly load the files they check.

132 computational modules and the standalone `base.py` type module have reference fixtures. The upstream archive retains PCC-13. This distribution omits it and the wargame harness. Its symbolic accessor still imports SymPy. The source-claim ceiling gate implementation is absent. These two cases are reported as skips. The directory smoke fixtures contain 231 value comparisons, alongside the original 10 invalid-input checks and the local regression suites. During the original archive migration, 2,733 differential checks in the extended comparison run included exhaustive simple undirected graphs on one through five vertices, seeded matrix cases, rank-deficient allocations, scalar callable factories and recovery-phase boundaries. The extended count includes fixtures subsequently retained in the smoke runners. It also includes scaled matrices, negative quadratic forms, individual recovery metrics, and trace dwell windows. The original archive comparisons use relative tolerance `1e-9` and absolute tolerance `1e-10`. Decisions, labels, dictionary keys and sequence lengths must match. These results describe the fixtures and tested ranges.

Archived oracles ran separately with NumPy 2.4.4, SymPy 1.14.0, NetworkX 3.6.1 and Pydantic 2.12.5. Stale base imports were bound to the archived types. The thermal step and scenario harness used their archived helper implementations. The malformed AI candidate metadata assignment was closed in the reference loader. The missing sigmoid was reconstructed from the archived symbolic expression. Its numerical evidence is formula parity.

The separately supplied PCC-15 campaign predictor matched its source on 77 comparisons. Its original one-in-three regression now runs. [Campaign predictor and baseline](hardware_viability/time_control_enforcement/README.md#monte_carlo_failure_predictorpy)

The separately supplied V.1–V.3 actuation model uses a standard-library optimizer. All 130 comparison cases matched on the final `null_set` decision. The convergence status differed in 12 cases, and two jointly converged cases had numeric differences above `1e-4`. The family README and replay fixtures record the solver-specific results. [Actuation solver comparison](hardware_viability/actuator/README.md#comparison-with-the-supplied-scipy-implementation)

## Interface changes

- Arrays return as Python lists and nested lists. Tuple result order and dictionary keys are retained. Scalar symbolic accessors return expression text. Callable factories retain their scalar argument order.
- Graph connectivity accepts an undirected adjacency mapping. Recovery configuration uses frozen dataclasses with validation. Package-specific validation, symbolic algebra and array methods are outside the new interface.
- Formula records, standalone formula constants, and the electrical proposal registry are documented in each owning README. Import standalone metadata types directly from `base.py` when needed. Historical trace references in the records identify original material and are not runtime requirements.

## Subdirectories

- [ai_governance](ai_governance/README.md)
- [consensus_coordination](consensus_coordination/README.md)
- [environment_geometry](environment_geometry/README.md)
- [estimation_detection](estimation_detection/README.md)
- [graph-survivability](graph-survivability/README.md)
- [hardware_viability](hardware_viability/README.md)
- [network-and-compute](network-and-compute/README.md)
- [plant_fidelity](plant_fidelity/README.md)
- [provenance_governance](provenance_governance/README.md)
- [safety_pace](safety_pace/README.md)
- [sampling_based_reachability_search](sampling_based_reachability_search/README.md)
- [space-and-comms](space-and-comms/README.md)


## Model files

- [base.py](base.py)
- [bounded_disturbance_admission.py](bounded_disturbance_admission.py) — Bounded disturbance injection

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
base.py
  FormulaMetadata = {"assumptions": "finite", "deployment_class": "note", "evidence_hooks": null, "formula_id": "sample", "name": "Sample", "rtm_link": null, "runtime_class": "helper", "ssot_gate": null, "symbolic_form": "x", "tests": "sample", "typed_inputs": {"x": "float"}, "units": {"x": "m"}}
bounded_disturbance_admission.py
  compute_bounded_disturbance = [9.1, 5.2]
  compute_bounded_disturbance rejected invalid input
PASS .
```

<!-- end-observed-output -->

## base.py

### Current interface

- Standalone types retain their constructors, enum values and to_dict serialization. The formula files run independently of them.

### Entry points

- `RuntimeClass` (type)
- `DeploymentClass` (type)
- `FormulaMetadata` (type)

### Metadata type definitions from the archive

#### RuntimeClass

Enumerates the contexts in which a formula may execute.

* ``RUNTIME_SAFE`` – Safe for use during runtime with bounded
  computational cost and no external side effects.
* ``OFFLINE_ONLY`` – Intended for design‑time analysis or
  certification; should not be invoked in a live control loop.
* ``HELPER`` – Auxiliary functions that support other laws but
  should not be exposed as standalone mission logic.

#### DeploymentClass

Enumerates deployment postures for formulas.

* ``PROTOTYPE`` – Used during system prototyping or research.
* ``DEPLOYMENT`` – Approved for deployment in production systems.
* ``NOTE`` – Included for completeness but not intended for
  execution (e.g., convenience wrappers or explanatory notes).

#### FormulaMetadata

Captures doctrinal metadata for a single formula implementation.

Attributes
----------
formula_id : str
    The canonical identifier from Appendix A (e.g. ``"M1.2"``).
name : str
    A human‑readable name describing the formula.
symbolic_form : str
    The mathematical expression from the compendium.
typed_inputs : Dict[str, str]
    A mapping of input parameter names to a description of their
    expected type (e.g. ``{"x": "Vector[float]"}``).  Concrete type
    annotations in the implementation should correspond to these
    descriptions.
units : Dict[str, str]
    A mapping of input/output names to their physical units.  For
    dimensionless quantities use ``"unitless"``.
assumptions : str
    A concise description of any preconditions or model
    assumptions underlying the formula.
runtime_class : RuntimeClass
    Classification indicating whether the function may be used
    directly in a live control loop (``RUNTIME_SAFE``), only at
    design time (``OFFLINE_ONLY``), or as a helper (``HELPER``).
deployment_class : DeploymentClass
    Posture describing whether the implementation is ready for
    deployment, suitable for prototypes, or merely a note.
tests : str
    Path or identifier pointing to the test suite that verifies
    this formula (e.g. ``"tests/test_margin_to_death.py::test_basic"``).
evidence_hooks : Optional[str]
    A reference to an evidence generation harness in the
    ``lambda_evidence`` package, if applicable.
rtm_link : Optional[str]
    A stable link used by the runtime traceability matrix to refer
    back to this formula.  Typically this matches the module
    dotted path (e.g. ``"lambda_laws.margin_to_death"``).
ssot_gate : Optional[str]
    Identifier of the Single Source Of Truth (SSOT) notebook gate
    that must be executed before this formula may be promoted to
    deployment.

## bounded_disturbance_admission.py

### Model context from the archive

M3.1e — Bounded disturbance injection

This module enforces a bound on disturbances applied to a state–space
system and computes the resulting state derivative:

    w(t) ∈ W := { w : ||w|| ≤ w_max } ; ẋ = A x + B u + G w.

If the disturbance norm exceeds ``w_max``, an exception is raised.

### Current interface

- The numerical implementation uses Python scalars and sequences. Vector and matrix outputs use lists and nested lists.

### Entry points

- `compute_bounded_disturbance(A: Sequence[Sequence[float]], B: Sequence[Sequence[float]], G: Sequence[Sequence[float]], x: Sequence[float], u: Sequence[float], w: Sequence[float], w_max: float)`

### Original formula record

- **Formula id**  M3.1e
- **Name**  Bounded disturbance injection
- **Symbolic form**  `w(t) ∈ W := { w : ||w|| ≤ w_max } ; ẋ = A x + B u + G w`
- **Typed inputs**  `A` (Sequence[Sequence[float]]), `B` (Sequence[Sequence[float]]), `G` (Sequence[Sequence[float]]), `x` (Sequence[float]), `u` (Sequence[float]), `w` (Sequence[float]), `w_max` (float)
- **Units**  `A` (unitless), `B` (unitless), `G` (unitless), `x` (state), `u` (control), `w` (disturbance), `w_max` (disturbance), `output` (state/time)
- **Assumptions**  Matrices A, B, G must have compatible dimensions with x, u, w.  The disturbance vector w must satisfy ||w|| ≤ w_max.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_bounded_disturbance.py::test_bounded_disturbance`, `rtm_link=lambda_laws.bounded_disturbance`, `ssot_gate=notebooks/gate_bounded_disturbance.ipynb`

Additional reference comparisons during migration: 51.
