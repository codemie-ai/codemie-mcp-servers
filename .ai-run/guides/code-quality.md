# Code Quality

Exact commands are in `quality-gates.md`.

## Enforced Rules

| Tool | State | Evidence |
|---|---|---|
| ruff lint | Enforced in CI with default rules. No `[tool.ruff]` section exists. | `.github/workflows/ci.yml`, step "Lint"; `mcp/assistants/pyproject.toml`, dev dependencies |
| ruff format | Only through `make ruff`. CI does not check it. | `mcp/assistants/Makefile`, target `ruff` |
| black, isort | Declared. No Makefile target or CI step runs them. | `mcp/assistants/pyproject.toml`, dev dependencies |
| CodeQL | Runs for `actions` and `python` | `.github/workflows/codeql.yml` |

## Formatting Scope

| Bad | Best |
|---|---|
| Run `make ruff` and commit unrelated reformatting | Run the check, then fix only the files in your change. `make ruff` rewrites the whole package. |
| Add a new formatter or a ruff config in a feature PR | Propose tooling changes in a separate `chore` or `build` PR |

The code does not have one uniform format. Compare the import blocks of `mcp/workflows/src/codemie_mcp_workflows/server.py` and `mcp/datasources/src/codemie_mcp_datasources/server.py`.

## Type Hints

Public tool functions have full hints, because FastMCP builds the schema from them (`list_datasources` in the datasources `server.py`). No type checker runs.

| Bad | Best |
|---|---|
| `history: List[...] = None` in new code | `Optional[List[...]] = None`, see `create_code_datasource` |
| Untyped tool parameter | Typed parameter with an `Args:` line, see `create_code_datasource` |

## Naming

| Item | Convention | Evidence |
|---|---|---|
| Distribution and command | `codemie-mcp-<package>` | `[tool.poetry.scripts]` in each `pyproject.toml` |
| Python module | `codemie_mcp_<package>` | `packages` in each `pyproject.toml` |
| Release tag | `mcp-<package>-vX.Y.Z` | `docs/RELEASING.md` |
| FastMCP server name | `codemie-<package>` | `FastMCP("codemie-workflows")` in the workflows `server.py` |
