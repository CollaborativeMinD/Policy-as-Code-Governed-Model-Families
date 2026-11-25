# Working on governed models

Start in TOML. For model behavior, edit the deployment draft for the selected model ID. For terminal and MCP scope, edit the console policy. Follow the role workflow and verification commands in the [Runbook](Runbook.md).

An agent reads its authorized inventory, selects an available task, and sends its declared inputs and observed revision to MCP. Record the returned receipt ID and effect. Refresh on a stale revision. Keep admin credentials and the service filesystem outside the agent environment.

For a new mathematical operation, demonstrate the missing binding, implement it in its model, check an independent reference and qualify its ordinary call. Add a reviewed task binding only when that operation should be available over MCP. Run the positive and denial witnesses before release. [Skill](SKILL.md)

## From policy change to release

Start with [console.toml](console.toml) for this component. Write down the requested effect and one case that must be denied. Change the TOML first.

1. Apply the candidate to disposable state. An unknown field or unbound operation must fail admission before an effect. Keep that denial.
2. For supported behavior, continue with the existing runtime. For new behavior, implement the missing typed field and the method that enforces it. Run the same candidate again.
3. Run `python -B verification/replay.py` in the project environment. Exercise the normal entry point and the denial. Review the ordinary model result, reference tolerance and admitted revision. Reconcile discrepancies and repeat.
4. Qualify the exact commit on local Forgejo. Review the package, image, security scan and receipt for each release target. Ship the reviewed artifacts and record their digests.
