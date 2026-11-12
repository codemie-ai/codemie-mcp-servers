# Quality Gates

Run each gate inside the folder of the package you changed: `mcp/assistants`, `mcp/datasources` or `mcp/workflows`. There is no root manifest and no root command. CI runs the same steps for all three packages (`.github/workflows/ci.yml`, matrix at line 19). The package differences are in `architecture.md`.

The "Ran" column records what was executed on 2026-11-05, in a scratch copy of the repository, with Poetry 2.5.1 and Python 3.12. "not run" means nobody ran the command for this guide.

## Commands per package

| Command | assistants | datasources | workflows | Pass means |
|---|---|---|---|---|
| `poetry install --no-interaction` | yes, exit 0 | yes, exit 0 | yes, exit 0 | exit code 0 |
| `poetry run ruff check .` | yes, exit 0 | yes, exit 0 | yes, exit 0 | `All checks passed!` |
| `poetry build` | yes, exit 0 | yes, exit 0 | yes, exit 0 | wheel and sdist in `dist/` |
| Missing-settings smoke test (below) | yes, exit 1 with expected message | yes, exit 1 with expected message | yes, exit 1 with expected message | non-zero exit and message below |
| `make ruff-fix` | yes, exit 0 | yes, exit 0 | yes, exit 0 | exit code 0 (rewrites files) |
| `make verify` (runs `make ruff`) | yes, exit 0, rewrote files | yes, exit 0, rewrote files | yes, exit 0, rewrote files | exit code 0 (rewrites files) |
| `make build` | yes, exit 0 | yes, exit 0 | yes, exit 0 | same as `poetry build` |
| `make test` | yes, exit 0, no recipe | yes, exit 0, no recipe | yes, exit 0, no recipe | nothing ran: `Nothing to be done` |
| `make install` | not run | not run | not run | same as `poetry install` without the flag |
| `make publish` | not run (publishes to PyPI, never run it) | not run | not run | not a check |

The three `Makefile` files are identical in content (checked with `diff`).

### Missing-settings smoke test

Copy of the CI step (`.github/workflows/ci.yml`, step "Smoke test without settings"). Replace `<package>` with `assistants`, `datasources` or `workflows`:

```bash
env -u CODEMIE_AUTH_SERVER_URL -u CODEMIE_AUTH_REALM_NAME -u CODEMIE_API_DOMAIN poetry run codemie-mcp-<package> </dev/null
```

Pass: non-zero exit code, and the output has `Missing required settings: CODEMIE_AUTH_SERVER_URL, CODEMIE_AUTH_REALM_NAME, CODEMIE_API_DOMAIN`. Fail: exit code 0, or another message. Startup validation is broken. The text before that message differs by package (`Error initializing settings:` or `Error starting MCP server:`).

### Notes on the local commands

- The packages have no lockfile, so dependencies resolve fresh against PyPI (comment above the install step in `ci.yml`; `CONTRIBUTING.md`, Local Checks).
- `poetry install` can create `poetry.lock`, and `poetry build` creates `dist/`. Both show as untracked. Do not commit them. Delete them after the check.
- `make verify` and `make ruff` run `ruff check --fix` and `ruff format` (`Makefile`, targets `ruff` and `verify`). They change source files, so they are not checks. In the scratch run they rewrote files in all three packages.
- Stage named files only. Never use `git add -A`.

## CI jobs

| Job name | Definition | Fail means |
|---|---|---|
| `Package assistants`, `Package datasources`, `Package workflows` | `.github/workflows/ci.yml`, job `package`, matrix at line 19 | install, lint, build or smoke test failed in that package |
| `Internal references` | `.github/workflows/ci.yml`, line 60 | private host, ticket key or personal e-mail in the tree |
| `Security` | `.github/workflows/ci.yml`, line 66; rules in `.gitleaks.toml` | a secret is in the change |
| `PR Title` | `.github/workflows/pr-title-lint.yml`, line 17 | the title is not Conventional Commits |
| `CodeQL (actions)`, `CodeQL (python)` | `.github/workflows/codeql.yml`, line 25 | finding in `actions` or `python` |

The last four have no local command in this repository. CI permissions and pinning are in `development/security-patterns.md`.

## Gates that do not exist

| Gate | State | Evidence |
|---|---|---|
| Unit tests | No test files. CI has no test step. `pytest` is a dev dependency but nothing uses it. `make test` has no recipe. | `mcp/assistants/pyproject.toml`, `[tool.poetry.group.dev.dependencies]`; `mcp/assistants/Makefile`, `.PHONY` |
| Type check | No mypy or pyright configuration | `mcp/assistants/pyproject.toml` |
| Format check | CI runs `ruff check` only, not `ruff format`, `black` or `isort` | `.github/workflows/ci.yml`, step "Lint" |

Test strategy and the list of risky untested code are in `testing/qa-strategy.md` and `testing/qa-health.md`. Do not report a package as tested because lint and build pass. To verify tool behaviour, say what you ran. The servers need a live CodeMie installation.
