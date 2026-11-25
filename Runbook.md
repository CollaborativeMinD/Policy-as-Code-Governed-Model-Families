# Runbook

## Prepare the local service

Use Python 3.13 from the repository root. The service account owns its checkout, deployment and credentials. Give each TUI user read access to only their own token file. Keep the signer, other tokens and deployment directory accessible only to the service operator. On Windows, use a service-account directory with a private NTFS ACL. The generated tokens inherit its ACL. The existing local model CLI is a trusted operator interface.

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-console.txt
$env:MODEL_POLICY_HOME = Join-Path $PWD '.local/deployment'
python -m model_policy_engine init $env:MODEL_POLICY_HOME
python -m console_app.server credentials .local/credentials
$pin = (Get-FileHash console.toml -Algorithm SHA256).Hash.ToLower()
python -m console_app.server serve --credentials .local/credentials --policy console.toml --sha256 $pin
```

Review the console policy before approving its digest. For a managed deployment, supply that approved digest through the service launcher. Credential provisioning creates a new directory and refuses to overwrite an existing one. Rotate a token by atomically replacing its protected file with a fresh URL-safe secret of at least 43 characters. The server authenticates each request.

## Open the terminal

In another terminal, use the same virtual environment. For a local single-operator demonstration, launch one of these commands. For separate operators, point each client to its own protected copy of the assigned credential. The client needs the loopback port and its token. Only the server process needs MODEL_POLICY_HOME.

```powershell
python -m console_app.tui --token .local/credentials/viewer.token
python -m console_app.tui --token .local/credentials/admin.token
python -m console_app.tui --token .local/credentials/agent.token
```

Filter to `stale_evidence_decay`. The viewer shows admission, version, policy digest and MCP activity. Ctrl+R refreshes immediately. An unavailable observation clears the table. Ctrl+Q exits.

In admin mode, open the selected draft. Change the default decay exponent from 1 to 3. Apply the TOML. A successful publication returns the new revision. An invalid edit leaves the active policy intact. If another operator publishes first, reopen the draft and reapply your change. Ordinary refreshes preserve the editor buffer while that model remains selected.

In agent mode, select `evidence_decay`. With age 5 and freshness margin 10, the baseline result is 0.5. With the admitted exponent 3, the result is 0.125. Read the receipt ID in the terminal. Full receipts are JSON files under the service deployment’s `receipts` directory. Each records the task, inputs, model source digest, signed policy revision, time and result.

## Manage scope

Edit `console.toml` to select registered tasks, sample inputs, grants, port and polling interval. Task input keys define the arguments an agent can supply. The model contract governs the values. Validate and restart the service with the approved console digest for scope changes. Model-policy publications take effect live.

An external MCP client uses stateless Streamable HTTP at `http://127.0.0.1:8766/mcp` by default, protocol `2026-07-28`, and the role bearer credential. Discover tools through MCP, then read inventory to obtain the task name, input shape and current revision. Agent requests carry those three values. The server checks them again under the publication lock. Changed or unverifiable revisions require a fresh inventory read. Role grants are enforced by the server for every client.

## Qualify a candidate

```powershell
python -B -m unittest discover -s model_policy_engine/tests -v
python -B verification/replay.py
python -B verification/verify_wheel.py
python -B tests/verify_console.py
```

The console witness uses a disposable deployment, ephemeral port and fresh role credentials. Check the local Forgejo run and its revision artifact before promoting that same Git revision to GitHub.

## From policy change to release

Start with [console.toml](console.toml) for this component. Write down the requested effect and one case that must be denied. Change the TOML first.

1. Apply the candidate to disposable state. An unknown field or unbound operation must fail admission before an effect. Keep that denial.
2. For supported behavior, continue with the existing runtime. For new behavior, implement the missing typed field and the method that enforces it. Run the same candidate again.
3. Run `python -B verification/replay.py` in the project environment. Exercise the normal entry point and the denial. Review the ordinary model result, reference tolerance and admitted revision. Reconcile discrepancies and repeat.
4. Qualify the exact commit on local Forgejo. Review the package, image, security scan and receipt for each release target. Ship the reviewed artifacts and record their digests.

The version 2 `[runtime]` table in `console.toml` sets request size, concurrency and client deadlines. Version 1 files inherit the shipped budget. Reissue them as version 2 to pin these choices in the admitted document.

## Build and ship this revision

Review [release/policy.toml](release/policy.toml) and the hash-locked dependency closure. Local Forgejo builds the Linux wheel, source distribution and exact-source ZIP. On the trusted Windows workstation set `PAC_CHECKOUT` to the clean checkout, `PAC_OUTPUT` to a fresh release directory, `PAC_BUILD_PYTHON` to a Python 3.13 environment with `release/build.lock`, and `PAC_SCANNER` to the pinned Trivy executable. Run this from the checkout.

```powershell
forgejo-runner exec --workflows release/workstation.yml --job workstation --image=-self-hosted --detect-event --env "PAC_CHECKOUT=$env:PAC_CHECKOUT" --env "PAC_OUTPUT=$env:PAC_OUTPUT" --env "PAC_BUILD_PYTHON=$env:PAC_BUILD_PYTHON" --env "PAC_SCANNER=$env:PAC_SCANNER"
```

The job builds and reinstalls the Windows wheel, checks the target machine and UID, exercises the native console effect in hardened Compose, scans the image, exports it and checks the restored image ID. For a package installation, install the release lock followed by the wheel with `--no-deps`. Use the command named by the release policy with `unpack NEW_DIRECTORY` to install the exact component tree. Follow its native runbook from there.

For a container installation, load the matching `.image.tar.gz` and use its accompanying `compose.json`. Provision the service's credential directory with `docker compose -f compose.json run --rm console credentials /state/credentials`. Apply the component's native setup before starting the console. The server binds loopback inside its own network namespace. Supply upstream files as read-only mounts and place a dependent local service or client in that same namespace. Review the policy digest, package hashes, image identity, scan report and effect before promoting the revision.
