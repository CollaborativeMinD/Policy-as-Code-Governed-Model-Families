---
name: governed-model-console
description: Inspect currently admitted model families, publish model TOML as an admin, or execute a role-scoped model task over local MCP.
---

Read inventory first. Use the authenticated role and selected model to determine available actions. In viewer mode observe the active revision. In admin mode open the draft, retain both edit preconditions, edit TOML, apply, and verify the new revision. In agent mode select a named task, submit its permitted input keys and the active revision, and inspect the returned result and receipt.

A changed revision requires a new read. A rejected policy requires a corrected draft or a qualified runtime implementation. Use the three-session witness and local Forgejo release procedure in the [Runbook](Runbook.md).

## From policy change to release

Start with [console.toml](console.toml) for this component. Write down the requested effect and one case that must be denied. Change the TOML first.

1. Apply the candidate to disposable state. An unknown field or unbound operation must fail admission before an effect. Keep that denial.
2. For supported behavior, continue with the existing runtime. For new behavior, implement the missing typed field and the method that enforces it. Run the same candidate again.
3. Run `python -B verification/replay.py` in the project environment. Exercise the normal entry point and the denial. Review the ordinary model result, reference tolerance and admitted revision. Reconcile discrepancies and repeat.
4. Qualify the exact commit on local Forgejo. Review the package, image, security scan and receipt for each release target. Ship the reviewed artifacts and record their digests.
