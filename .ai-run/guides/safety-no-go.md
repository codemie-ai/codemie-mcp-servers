# Safety No-Go List

Things an AI agent must never do in this repository. The list applies to every agent: Claude Code, Codex, Copilot, Gemini and others. `.claude/settings.json` (`permissions.deny`) enforces the same list for Claude Code. Other tools do not read that file, so follow this guide. If you change one, change the other.

If a task needs an item on this list, stop and ask a person. Secrets handling, TLS and CI permissions are in `security.md`. This guide only lists refusals.

## Files never read or changed

| Path | Why |
|---|---|
| `.env`, `.env.*` (any folder) | They hold real platform credentials (`CODEMIE_PASSWORD`, `CODEMIE_AUTH_CLIENT_SECRET`). The repository has no committed `.env` template, so no `.env*` file is safe to read. Use the variable names in `architecture.md`, "SDK Client And Settings". |
| `*.pem`, `*.key`, `*.p12`, `*.pfx` | Private keys and certificates. A value read into the context can leak into a log, a commit or a PR. |
| `~/.ssh/**` | SSH keys give push access to repositories. |
| `~/.aws/**` | Cloud credentials. Not needed for any task here. |
| `~/.pypirc`, `~/.config/pypoetry/auth.toml` | PyPI upload tokens. Releases go only through `publish.yml` (`docs/RELEASING.md`). |
| `~/.npmrc`, `~/.docker/config.json` | Registry tokens. Not needed for any task here. |
| `poetry.lock` (change) | No lockfile is committed. `poetry install` creates one locally. Never edit it by hand and never commit it (`quality-gates.md`, "Notes on the local commands"). |

## Commands never run

| Command | Why |
|---|---|
| `git push --force`, `git push -f`, `git push <remote> --force…`, `git push <remote> -f…` | Rewrites shared history and can delete work of other people. Push a new commit instead. |
| `git reset --hard` | Deletes uncommitted work with no undo. |
| `git clean -fd` | Deletes untracked files with no undo. |
| `rm -rf <anything>` | Deletes with no undo. Delete named files one at a time. |
| `git commit --no-verify`, any command with `--no-verify` | Skips hooks that exist to stop bad commits. Fix the cause. |

## Actions that always need a person

| Action | Why |
|---|---|
| `poetry publish`, `make publish` | Uploads a version to PyPI. PyPI never accepts the same version twice, so a wrong upload cannot be undone. Releases go only through `publish.yml` (`docs/RELEASING.md`). |
| `gh release create` | A published release starts `publish.yml` and releases to PyPI (`docs/RELEASING.md`). |
| `gh workflow run` | `publish.yml` accepts a manual run that can publish. A person decides every manual run. |
| Push to `main`, or merge a PR | Every PR needs one approval and green CI (`CONTRIBUTING.md`, "Review Rule"). |
| Add a write or delete MCP tool | It is a security-relevant change (`security.md`, "Tool Input And Destructive Tools"). |
| Call `delete_datasource` against a live CodeMie installation | It deletes with no confirmation (`mcp/datasources/src/codemie_mcp_datasources/server.py:260`). |

The last three rows have no rule in `.claude/settings.json`, because a command pattern cannot express them.
