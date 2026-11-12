# QA Strategy

**Last assessed**: 2026-11-12

The repository has three Python packages under `mcp/`: `assistants`, `datasources` and `workflows`. All three use the same stack: Python 3.12, Poetry, FastMCP over stdio and `codemie-sdk-python` (`architecture.md`). There is no second stack, so one strategy covers all three. Run every command in the folder of the package (`quality-gates.md`).

## Test Frameworks

| Framework | Type | Config file | Test directories |
|---|---|---|---|
| pytest (declared, not used) | unit | none. No `pytest.ini`, `setup.cfg`, `tox.ini`, `conftest.py` or `[tool.pytest.ini_options]`. | none |
| Missing-settings smoke test (shell) | startup check of the installed command | `.github/workflows/ci.yml:48-58` | none (inline CI step) |

`pytest = "^8.0.0"` is in `[tool.poetry.group.dev.dependencies]` of each package (`mcp/assistants/pyproject.toml:32`, `mcp/datasources/pyproject.toml`, `mcp/workflows/pyproject.toml`). On 2026-11-09, `poetry run pytest -q` in a scratch copy of each package (Poetry 2.5.1, pytest 8.4.2) printed `no tests ran` and exited with code 5.

## Test Types in Use

### Unit Tests
- **Location**: none detected. No `tests/` folder and no `test_*.py` file in `mcp/`.
- **Pattern**: n/a. If you add tests, use `mcp/<package>/tests/test_*.py`, so each package stays installable and testable alone (`architecture.md`, "Boundaries").
- **Run command**: n/a. CI has no test step (`.github/workflows/ci.yml:23-58`). `make test` has no recipe (`mcp/assistants/Makefile:1`).
- **Example**: none in the tree. The only executed check of code behaviour is the smoke test: `.github/workflows/ci.yml:53`.

### Integration Tests
- **Location**: none detected
- **Pattern**: n/a
- **Run command**: n/a. The servers need a live CodeMie installation (`quality-gates.md`, last line).

### End-to-End Tests
- **Location**: none detected
- **Tool**: none detected
- **Run command**: n/a

### Startup smoke test (CI)
- **Location**: `.github/workflows/ci.yml:48-58`, step "Smoke test without settings", one run per package in the matrix (`.github/workflows/ci.yml:19`)
- **Run command**: `env -u CODEMIE_AUTH_SERVER_URL -u CODEMIE_AUTH_REALM_NAME -u CODEMIE_API_DOMAIN poetry run codemie-mcp-<package> </dev/null` (same as `quality-gates.md`)
- **Pass means**: non-zero exit code and the text `Missing required settings: CODEMIE_AUTH_SERVER_URL, CODEMIE_AUTH_REALM_NAME, CODEMIE_API_DOMAIN`
- **What it proves**: startup validation only. It does not call any tool.

## Coverage Targets

- **Line coverage target**: not configured
- **Branch coverage target**: not configured
- **Coverage command**: not configured. `pytest-cov` and `coverage` are not dependencies, and there is no `[tool.coverage]` section.

## Conventions

- **Test file naming**: none in the tree. Use `test_*.py`, the pytest default, because pytest is the declared runner.
- **Test file location**: none in the tree. Use `mcp/<package>/tests/`.
- **Test style**: none in the tree.
- **Source docs scanned**: `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, `CLAUDE.md`, `SECURITY.md`, `docs/RELEASING.md`, `mcp/*/README.md`, `.ai-run/guides/*.md`, `.ai-run/guides/standards/*.md`. No `skills/`, `.claude/rules/`, `.cursorrules` or `.github/copilot-instructions.md`.
- **Naming / selector conventions (from docs)**:
  - No UI, so no selector conventions.
  - The MCP tool name and docstring are the schema the AI tool reads (`architecture.md`, "Tool Patterns"). A test of a tool should check the name and the `Args:` section too.
  - Dynamic tool names must match `^[a-zA-Z0-9_-]{1,64}$` (`mcp/assistants/src/codemie_mcp_assistants/server.py:53`).
- **Architecture notes (from docs)**:
  - assistants and workflows read settings at import and call `sys.exit(1)` on failure (`mcp/assistants/src/codemie_mcp_assistants/server.py:17-21`, `mcp/workflows/src/codemie_mcp_workflows/server.py:16-20`). A test must set the environment before it imports `server`.
  - assistants fetches the assistant from the platform at import (`mcp/assistants/src/codemie_mcp_assistants/server.py:117`). A test must stub `CodeMieClient` before import.
  - datasources reads settings on each `get_client()` call (`mcp/datasources/src/codemie_mcp_datasources/server.py:54-56`). It is the easiest package to unit-test.
  - The packages share no code. A shared rule needs the same test in each package (`architecture.md`, "Dependency Rules").
- **Testing guidance (from docs)**:
  - Write or run tests only when asked or when you need them to verify a change (`AGENTS.md`, "Critical Rules").
  - Do not report a package as tested because lint and build pass. Say what you ran (`quality-gates.md`, "Gates that do not exist").
  - `poetry install` can create `poetry.lock`. Do not commit it (`quality-gates.md`, "Notes on the local commands").
  - A new test step must also go into `.github/workflows/ci.yml`, or CI does not run it.

## Anti-Patterns (observed in this codebase)

| Bad | Better | Why |
|---|---|---|
| A datasources test with a `MagicMock` client, so `create(...)` returns an object with `.id` and any method name exists | Stub the SDK at its HTTP layer and keep the SDK types: for example stub `DatasourceService._api.post` to return `{"message": "..."}`, and build `UpdateCodeDataSourceRequest` for real. Check the tool result is a `dict`. | A loose mock makes a test pass on a tool that fails on every call. The real failures are in `architecture.md`, "Known Defects To Check Before You Copy A Pattern": `create()` and `update()` return a `dict`, the update request needs `link`, and `get_processing_info` does not exist. |
| `branch=branch or current.code.branch if current.code else None` in `update_code_datasource` | Parenthesise, and test with `current.code` empty and a supplied `branch` | Operator precedence drops the supplied value. This test can pass only after the missing `link` is fixed (`architecture.md`, "Known Defects"). |
| Length check `> 60` and slice `[:64]`, then `ask_` added later (`mcp/assistants/src/codemie_mcp_assistants/server.py:74-75`, `:119`) | Test `sanitize_tool_name` with a long name and check the final tool name against the 64-character pattern | A long name can exceed the limit. A pure function is cheap to test. |
| Settings and a network call at import (`mcp/assistants/src/codemie_mcp_assistants/server.py:18`, `:117`) | Set the environment and stub `CodeMieClient` in a fixture before the import | Import fails or calls the network in a test run. |
| `delete_datasource` with no confirmation (`mcp/datasources/src/codemie_mcp_datasources/server.py:260-267`) | Run only against a mock client in tests | A test against a live platform deletes real data. |

## Code Repositories

Application source repositories that are tested. Recorded so `qa-e2e-generator` can search pull requests and commits. Not scanned for conventions.

- **codemie-mcp-servers**: https://github.com/codemie-ai/codemie-mcp-servers

## External Sources

### Test Case Management
- **System**: none. Bugs and test gaps are tracked as GitHub Issues (`CONTRIBUTING.md`, "Reporting Issues").
- **Adapter**: not available

> **No MCP adapter configured** for test case management. The project uses GitHub Issues only and keeps no separate test cases. To enable automated test case creation, configure a test case system and an adapter, then re-run qa-foundation.

### QA Documentation
- **System**: within repo
- **Adapter**: not configured
- **Paths**: `.ai-run/guides/quality-gates.md`, `.ai-run/guides/testing/qa-health.md`

### External Test Repositories
none
