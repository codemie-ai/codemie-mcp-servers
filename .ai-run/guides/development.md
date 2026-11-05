# Development Practices

Tooling is Poetry with Python 3.12 (`mcp/assistants/pyproject.toml`, `[tool.poetry.dependencies]`). Exact commands are in `quality-gates.md`. Package differences are in `architecture.md`.

## Error Handling

Tool functions log the failure to stderr and raise again. `main()` catches startup failures and exits with code 1.

| Bad | Best |
|---|---|
| Swallow the exception and return text | Print to stderr and `raise`, see `execute_workflow` in `mcp/workflows/src/codemie_mcp_workflows/server.py` |
| Empty SDK result passed on | Raise `ValueError`, see `chat_with_assistant` in `mcp/assistants/src/codemie_mcp_assistants/server.py` |
| Stack trace at startup for bad settings | Message and `sys.exit(1)`, see `main` in `mcp/datasources/src/codemie_mcp_datasources/server.py` |

## Logging

Use `print(..., file=sys.stderr)`. No package uses a logging framework.

| Bad | Best |
|---|---|
| `print()` to stdout | stdout carries the stdio MCP transport, so write to stderr, see `main` in the assistants `server.py` |
| Log message text or credentials | Log identifiers only, see the "Starting chat" line in `chat_with_assistant` |

Existing exception: an invalid history entry is printed whole in `chat_with_assistant` ("Invalid history format").

## Configuration

| Bad | Best |
|---|---|
| Read a required value with a built-in fallback | Report every missing setting in one error, see `_read_required_settings` in `mcp/assistants/src/codemie_mcp_assistants/model.py` |
| Copy one package's settings shape into another without checking | assistants and workflows use a settings class, datasources uses functions (`validate_settings` in the datasources `server.py`) |

The error text `Missing required settings: <names>` is a contract. CI checks it (`quality-gates.md`, smoke test) and the package READMEs state it. Variables and defaults are in `architecture.md`.

## Async

Tools are `async def`, but they call the SDK synchronously, see `list_datasources` in the datasources `server.py`. Await any call to another `async def`. See the known defects in `architecture.md`.

## Dependencies

| Rule | Evidence |
|---|---|
| Declare dependencies per package | `[tool.poetry.dependencies]` in each `pyproject.toml` |
| Do not commit a lockfile | `CONTRIBUTING.md`, Local Checks |
| Keep the SDK range in step with the root README | `README.md`, `mcp/assistants/pyproject.toml` |
| Do not run `make publish`. Release through `publish.yml`. | `Makefile` target `publish`, `docs/RELEASING.md` |

## Versioning

Each `mcp/*/pyproject.toml` holds the base version twice: `[project] version` (line 3) and `[tool.poetry] version` (line 12). The publish workflow reads and stamps the version with `poetry version` (`.github/workflows/publish.yml`, lines 125 and 133). The tag names the release version. Release rules are in `docs/RELEASING.md`.

When you raise the base line, change both copies.

Check on 2026-11-05 in a scratch copy: with Poetry 2.5.1, `poetry version 0.9.9` in `mcp/assistants` changed both copies. CI installs Poetry with `pipx install poetry`, so its version can differ. That Poetry version is the only one checked; any other version is an assumption.

## Documentation

Each package README is the user reference for its tools and settings. Update it in the same PR as the tool. Keep placeholder values in examples (`mcp/assistants/README.md`). Write public text without internal references (`CONTRIBUTING.md`; rules in `security.md`).
