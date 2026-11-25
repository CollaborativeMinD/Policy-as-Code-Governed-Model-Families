# Policy-as-Code Governed Model Families

Browse deployed models in a live terminal, publish a model policy, or run a scoped task. Each terminal connects to the same stateless MCP service. The credential you present selects your tools.

| Mode | What you see and can do |
| --- | --- |
| Viewer | Filter the full inventory by family, model ID or admission state. Watch current MCP executions and the latest completed task per model. |
| Admin | Select a model, open its deployment draft, edit TOML and apply it. Publication verifies the model contract and signs the exact candidate. A stale edit requires a reload. |
| Agent | Select a scoped model and a named task, edit its TOML inputs, then run it. The service returns a result and receipt for the selected active revision. |

**Active** means the installed policy bytes, signed manifest and durable admission agree. **Inactive** means no admission exists. **Unverified** means the service cannot establish the active revision. Running counts and latest execution refer to this MCP process. Standalone library calls run independently.

The default task policy exposes evidence decay and Little’s Law queue length. Both call the ordinary governed Python functions. Changing an admitted model policy changes their behavior on the next call. An administrator can narrow role grants, remove a task, or bind another task to an implemented operation in the console TOML. [Console policy](console.toml)

Start with the local setup and three-mode walkthrough. [Runbook](Runbook.md) · [Agent workflow](AGENTS.md) · [Skill](SKILL.md)

The publication contains 131 computational models plus the base metadata contract. The original review covered a larger archive. The archived turret implementation and wargame harness are outside this release. [Model families](model_families/README.md) · [Policy engine](model_policy_engine/README.md) · [Original numerical review](verification/Review.md)

Local Forgejo qualifies the exact candidate on a repository-scoped Linux runner. It runs the catalog and admission tests, replays the reviewed fixtures, installs the release wheel offline, and drives three headless Textual sessions against a real MCP server. [Workflow](.forgejo/workflows/qualification.yml) · [Workstation console receipt](verification/console-witness.json)
