# Model families 1.0.1 verification

The public model call is the admission boundary. The release audit matched 133 installed TOML contracts to their source files, including 323 operation and record tables and 70 internal settings. Each cataloged model declares its ID and binds its module. The audit found no literal defaults on the governed call signatures, no record fields declared in Python, and no direct module-level reads of tunable settings. Physical constants, unit conversions, wire identifiers, and arithmetic identities stay with the formulas.

## What changed

| Finding in the supplied archive | Correction and witness |
| --- | --- |
| A fractional count, boolean count or wrong sequence element could reach a kernel with a declared input type. A look-alike Python object could stand in for a governed record. | The common binder validates supplied values, nested containers, enums and registered record types before evaluation. JSON array pairs still work at tuple boundaries. Runtime binding also rejects missing public operations, mismatched signatures and Python-side call defaults. |
| A one-shot edge iterator gave a different connectivity result from the same triangle supplied as a list. | The binder retains validated iterable values for the call. Both inputs now produce two independent paths. A declared item ceiling stops a stream at the first excess item. |
| For a reachable temperature step of 10⁻¹⁶ °C toward a 100 °C equilibrium with a 50 s time constant, the heating function raised an error and its returned evaluator gave zero. Cooling had the same loss of precision. | The two crossing kernels evaluate the logarithm with the small change preserved. Both call paths now return approximately 5 × 10⁻¹⁷ s. The updated TOMLs declare finite inputs. |
| Scalar Kalman fusion with prior variance 10¹⁸ and measurement variance 1 returned zero posterior variance. | The Joseph covariance update retains the measurement-noise term. It agrees with the independent scalar precision calculation and a coupled two-state observation. |
| A caller could overwrite a recovery phase label through a mutable module dictionary. | The phase codes and labels are read-only wire identifiers. Recovery thresholds resolve from TOML. |

## Evidence from the original 1.0.1 review

The repository replay and wheel links below now point to the corresponding 1.1.0 receipts. Its wheel contains 132 catalog entries and checks 142 source and policy files.

| Check | Observation |
| --- | --- |
| Cold, admitted, and live-revision fixture replay | 131 catalog entries, including the base metadata module. Each fixture was denied in an empty deployment, passed under its signed template, then passed again on the same loaded module after a signed version-only edit. The observed runtime version changed in every case. The receipt includes source and policy SHA-256 values and the test revision digests. [Fixture results](fixture-results.json) |
| Real tuning change through the installed wheel | The same copied stale-evidence function returned 0.5, then 0.125 after the TOML decay exponent changed from 1 to 3. An explicit exponent of 2 was rejected. The check installed offline in an isolated environment and compared 143 runtime and policy files with the reviewed source. [Wheel receipt](wheel-result.json) |
| Engine, catalog, and independent mathematical tests | 27 tests passed on each of CPython 3.14.3 and 3.13.17. The numerical checks include all 1,099 simple labeled undirected graphs on one through five vertices, rational queue and speedup references, decimal thermal thresholds, heat balance, scalar and coupled covariance, and a radio power budget in linear units. [3.14 results](engine-tests.txt) · [3.13 results](engine-tests-py313.txt) |
| Shipped model regression suites | 23 suites ran on CPython 3.14.3. Of 63 tests discovered, 61 passed and two recorded their existing skips. [Suite results](fixture-results.json) |
| Original archive | Four targeted regression methods reproduced the original type, iterator, thermal and covariance failures against the supplied bytes. [Baseline comparison](baseline-comparison.txt) |

The communications/radar module received a separate check of radio received power. Its radar-range function and the wargame harness received static contract review only. The archived PCC-13 turret is outside the governed catalog. The source-claim ceiling gate has no implementation in the supplied archive. Model fixture parity covers the tested inputs. Independent mathematical checks have the scope listed above. Historical solver parity counts in the family READMEs remain historical.

## Reproduce locally

From the folder containing the engine and model families, run the following commands. The replay and wheel check create disposable policy deployments.

```powershell
python -B -m unittest discover -s model_policy_engine/tests -v
python -B verification/replay.py
python -B verification/verify_wheel.py
```

For a tuning change, edit one model draft, apply it and observe the public call. For a new model requirement, first capture the failed admission, then bind the operation and add an independent mathematical reference. Check the expected effect, a boundary and a rejection before promoting the implementation. Production policy publication verifies the installed contract and signed policy. The numerical tests run during release qualification.

Source archive SHA-256 is `de820daab60326441f7560bb4d2e46999f30b67bdc0e8507c24967f54732539d`. The counts above describe the original workstation review.
