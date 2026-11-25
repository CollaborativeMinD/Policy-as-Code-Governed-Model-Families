# Model policy engine

Each executable model declares one stable `model_id`. Its normal Python entry points resolve an authenticated TOML policy before evaluating their formulas. The shared engine and the model kernels run on Python 3.11 or later using the standard library. A copied model needs the engine, the configured keyring and its own admission. There are no imports between models.

## Start a local deployment

From the directory containing `model_families` and `model_policy_engine`, run these PowerShell commands.

```powershell
python -m pip install --no-index .\model_policy_engine-1.1.0-py3-none-any.whl
$env:MODEL_POLICY_HOME = Join-Path $PWD 'model-policy-state'
python -m model_policy_engine init "$env:MODEL_POLICY_HOME"
python -m model_policy_engine list
```

The release includes the engine wheel for offline installation. From a source checkout, use `python -m pip install .\\model_policy_engine`. Initialization creates a local keyring, one editable draft per model, signed active files and authenticated last-known-good records. Existing deployments keep their edits. For an existing external keyring, set `MODEL_POLICY_KEYRING_FILE` before initialization and in the model process. The keyring JSON contains `active_key_id` and a `keys` object mapping each key ID to its hex-encoded secret of at least 32 bytes. HMAC uses a shared secret for signing and verification. Restrict access to the deployment and keyring accordingly. Keep the installed engine and baseline templates under the same control as model source.

## Change one model

Open `$env:MODEL_POLICY_HOME\drafts\hardware_viability\recovery_time_inflation_policy.toml`. In `[calls."RecoveryTimeInflationConfig"]`, change the default of `rti_warning_threshold` from `1.25` to `1.5`. Keep the other fields and the declared model ID. Apply the edited draft.

```powershell
$draft = Join-Path $env:MODEL_POLICY_HOME 'drafts\hardware_viability\recovery_time_inflation_policy.toml'
python -m model_policy_engine apply "$draft"
```

For recovery time 1.3 s, baseline 1 s, time to violation 10 s and previous RTI 1.3, the ordinary `evaluate_recovery_state` call returns `GRACEFUL_DEGRADATION` at the shipped threshold and `NOMINAL_RECOVERY` at 1.5. The next top-level call in an existing process sees the admitted edit. Nested operations share that call’s snapshot. Existing objects keep their stored values. Reconstruct a configuration or a stateful search to adopt new defaults. Constraints on an explicitly supplied configuration still apply.

## Qualify a change

Start with one model ID and edit its deployment draft. Apply it, then call the same public function or alias the consumer uses. Record the expected result, observed result and disposition. A conflicting fixed value must fail before the formula runs. A rejected draft must leave the last admitted behavior available.

If a draft asks for an unknown operation or field, keep the rejection. Add its typed runtime binding in the model release and put the configurable value in TOML. Use an independent calculation or physical invariant to check the new math. Include a boundary case and an invalid input. Run the catalog audit, the model fixtures, and the offline wheel check before promoting that release. A signature establishes which policy was issued. Numerical qualification belongs to the release evidence.

Engine 1.0.1 checks supplied argument types at runtime, including nested items, records and enum identities. Ordinary integer measurements remain valid for float fields. JSON array pairs retain their supported tuple representation. The two thermal crossing templates now declare finite inputs. For an existing deployment, merge those field constraints into the two active models’ **drafts**, retain local tuning, and apply each draft with an admissible version.

The review directory includes the commands, tested scope and receipts. [Verification report](../verification/Review.md)

## Policy fields

| Declaration | Meaning |
| --- | --- |
| `model_id`, `version` | Family-qualified source identity and three-part policy version. The draft location, installed contract and signed content must agree. |
| `[calls."operation"]` | The operation’s fields and annotations. A field without a default is supplied by the caller. A policy may supply a default for a formerly required input. |
| `default`, `none = true` | An omitted argument takes its admitted value. TOML uses the explicit null marker for optional defaults. Nested record values use TOML tables. |
| `fixed = true` | Pin the field to its admitted default. An explicit, conflicting value raises an error before formula execution. |
| `allowed`, `gt`, `ge`, `lt`, `le`, `finite`, `min_items`, `max_items` | Define admissible values, numeric intervals and container lengths. |
| `records`, `enums` | Installed record field names, types and enum wire values preserve the model API. Changing its structure requires a corresponding model release. |
| `[settings]`, `relations` | Internal tuning values and relationships between fields. Sequence settings can constrain each numeric item with `items_ge` or `items_gt` and the total with `sum_eq`. Supported relations are `lt`, `le`, `same_length`, `member` and `disjoint`. |

For mappings with tuple or numeric keys, supply a TOML array of tables with `key` and `value` fields. A tuple key is written as an array. Callable arguments remain caller-supplied Python functions.

Measured inputs, solver iterates, return values and mathematical identities are computed by the model. Model-specific checks still evaluate properties that depend on the actual inputs, including geometry, units and dimensional compatibility. A policy signature attests to the issued settings. It does not establish scientific validity.

## Rejection and recovery

`apply` checks the edited bytes and recognized schema, verifies routing, signs the candidate, and runs the supplied loader’s version and rollback checks. A malformed draft can be corrected in place. A failed publication preserves the previous active pair. At runtime, an invalid active pair is quarantined. A model with a verified last-known-good record continues from that record, including after restart. With no valid admission it raises `PolicySecurityError`. Last-known-good records are bound to their absolute deployment paths. Initialize a deployment at its final location.

The loader retains the supplied key-rotation and single-use rollback-token protocols. Publish an authorized downgrade with `apply DRAFT --override TOKEN.json`. The signing epoch uses integer seconds and advances beyond the preceding admitted epoch when publishing multiple edits in one second. The distributed archive contains source and baseline templates. Deployment secrets and admission state are created locally.

## Verification

From the extracted bundle root run the engine tests and the full model tree.

```powershell
python -B -m unittest discover -s model_policy_engine/tests -v
python model_families/smoke_test.py --tree
```

The supplied loader tests cover key rotation, rollback, and single-use overrides. The integration tests cover ordinary calls, stale configuration records, per-model isolation, malformed and misrouted drafts, nested records, same-digest version binding, persisted fallback and first-use failure. Directory smoke tests create disposable deployments of the shipped policy defaults and compare the results to fixed reference fixtures. The family READMEs record the outputs.

The supplied archive’s loader filename began with a zero-width character. The integrated loader has a normal Python filename. Its wire schemas now live in `protocol.toml`. Standard-library records validate the declared wire types, reject unknown fields and preserve the signed JSON fields and canonical HMAC payloads. The public Pydantic object API and Pydantic’s implicit type coercions are outside this port.

