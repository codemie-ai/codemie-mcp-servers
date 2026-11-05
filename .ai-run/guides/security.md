# Security Practices

Report vulnerabilities through a GitHub Security Advisory, not a public issue (`SECURITY.md`, "Reporting a Vulnerability").

## Secrets Management

| Bad | Best |
|---|---|
| Credential in code or an example | Read from the environment, see `Settings` in `mcp/assistants/src/codemie_mcp_assistants/model.py` |
| Print settings with secrets | `Settings.__str__` omits credentials, see the same class |
| Commit `.env` | Keep it out of source control (`SECURITY.md`, "Guidance for Users") |

Secret scanning rules are in `.gitleaks.toml`.

## Public repository content

CI scans the tree. Do not commit credentials, private hostnames, ticket keys or personal e-mail addresses (`CONTRIBUTING.md`). Use `https://codemie.example.com` in examples. The scans are the CI jobs `Internal references` and `Security` (see `quality-gates.md`). Ticket key and tracker details are in `project.md`, as placeholders only.

## TLS

Verification is on by default. Parsing is strict, so an unknown value stops the server (`_read_verify_ssl` in each package). `false` is for local testing only (`SECURITY.md`, "Guidance for Users").

| Bad | Best |
|---|---|
| `verify_ssl=False` in code | Pass the parsed setting, see `get_client` in `mcp/datasources/src/codemie_mcp_datasources/server.py` |
| Unknown value treated as false | Raise `ValueError`, see `_read_verify_ssl` in `mcp/assistants/src/codemie_mcp_assistants/model.py` |

## Startup Validation

The server exits with a non-zero code before any network call when a required setting is missing (`README.md`). CI enforces this in the smoke test (see `quality-gates.md`). Do not add a code path that creates a client before this check.

## Tool Input And Destructive Tools

`delete_datasource` runs with no confirmation step (`mcp/datasources/src/codemie_mcp_datasources/server.py`). The platform account decides what the call may do. Treat a new write or delete tool as a security-relevant change.

Assistant names and descriptions from the platform go into the tool description unfiltered (`mcp/assistants/src/codemie_mcp_assistants/server.py`, `chat_with_assistant` decorator). The AI tool reads this text, so platform data reaches the model. Keep this in mind when you change that text.

## CI And Release Permissions

| Control | Evidence |
|---|---|
| Default workflow permission is `contents: read` | `.github/workflows/ci.yml:10` |
| Only the `publish` job has `id-token: write` | `.github/workflows/publish.yml:169` |
| The `publish` job passes the secret `PYPI_API_TOKEN` to the reusable workflow. The token is temporary. Trusted publishing is the target (`docs/RELEASING.md`, "Admin prerequisites"). | `.github/workflows/publish.yml:171-172` |
| The `verify` job has no secrets. It downloads `check_version.py` from `codemie-ai/ci-workflows` at `CI_WORKFLOWS_REF: main`. | `.github/workflows/publish.yml:25`, `.github/workflows/publish.yml:107` |
| Actions in this repo are pinned by SHA | `.github/workflows/ci.yml:25` |
| Reusable workflows are pinned to `@main`, not a SHA. This is a known exposure: a change in `ci-workflows` reaches CI and publish without review here. | `.github/workflows/ci.yml:64`, `.github/workflows/publish.yml:170` |
| A `release` event publishes only a tagged commit on `main` | `.github/workflows/publish.yml:88-95` |
| A manual `workflow_dispatch` publish needs `main` as the ref and a tag on the run commit | `.github/workflows/publish.yml:97-102`, `.github/workflows/publish.yml:74-86` |
