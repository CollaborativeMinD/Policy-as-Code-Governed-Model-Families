---
name: governed-model-console
description: Inspect currently admitted model families, publish model TOML as an admin, or execute a role-scoped model task over local MCP.
---

Read inventory first. Use the authenticated role and selected model to determine available actions. In viewer mode observe the active revision. In admin mode open the draft, retain both edit preconditions, edit TOML, apply, and verify the new revision. In agent mode select a named task, submit its permitted input keys and the active revision, and inspect the returned result and receipt.

A changed revision requires a new read. A rejected policy requires a corrected draft or a qualified runtime implementation. Use the three-session witness and local Forgejo release procedure in the [Runbook](Runbook.md).
