# QA Health

**Last assessed**: 2026-11-09
**Coverage**: low. No coverage data, qualitative assessment only. No package has a test file, so measured coverage would be 0% for each.

Method: test-to-source mapping. `mcp/` has 8 source files and 980 lines (`wc -l mcp/*/src/*/*.py`) and no test file. On 2026-11-09, `poetry run pytest -q` in a scratch copy of each package printed `no tests ran` (exit code 5). The only executed behaviour check is the CI smoke test (`.github/workflows/ci.yml:48-58`). Strategy and conventions are in `qa-strategy.md`.

## Coverage Summary

| Module / area | Coverage | Notes |
|---|---|---|
| `mcp/assistants/src/codemie_mcp_assistants/model.py` (135 lines) | 0% unit. Smoke test runs `_read_required_settings`. | Settings, auth method and TLS parsing. Only the "all three settings missing" path runs in CI. |
| `mcp/assistants/src/codemie_mcp_assistants/server.py` (231 lines) | 0% unit. Smoke test reaches only the import-time `Settings()` call. | `sanitize_tool_name`, `get_assistant_info`, `chat_with_assistant` never run in CI. |
| `mcp/datasources/src/codemie_mcp_datasources/server.py` (346 lines) | 0% unit. Smoke test runs `validate_settings` from `main()`. | Seven tools, including create, update and delete, never run in CI. |
| `mcp/workflows/src/codemie_mcp_workflows/model.py` (145 lines) | 0% unit. Smoke test runs `_read_required_settings`. | Request and response models are not checked against the SDK. |
| `mcp/workflows/src/codemie_mcp_workflows/server.py` (109 lines) | 0% unit. Smoke test reaches only the import-time `WorkflowSettings()` call. | `execute_workflow` never runs in CI. |
| `__init__.py` files (14 lines) | n/a | No logic |

## Risky Untested Areas

Modules with zero coverage that carry logic:

| Path | Coverage | Risk reason |
|---|---|---|
| `create_code_datasource`, `create_git_faq_datasource`, `update_code_datasource`, `get_datasource_processing_info` in `mcp/datasources/src/codemie_mcp_datasources/server.py` | 0% | Each tool fails on every call today (`architecture.md`, "Known Defects To Check Before You Copy A Pattern"). A test with an SDK-shaped stub would fail today. |
| `mcp/datasources/src/codemie_mcp_datasources/server.py:260-267` | 0% | `delete_datasource` deletes with no confirmation. Destructive tool with no test of its input or result. |
| `mcp/assistants/src/codemie_mcp_assistants/server.py:49-76` | 0% | `sanitize_tool_name` checks `> 60` and slices to 64, then `ask_` is added (`:119`). A long assistant name can make an invalid MCP tool name. Pure function, cheapest test to add. |
| `mcp/assistants/src/codemie_mcp_assistants/model.py:44`, `mcp/workflows/src/codemie_mcp_workflows/model.py:30` | 0% | `validate_auth_method` decides between username and password and client credentials. Only the "nothing set" path is exercised. |
| `_read_verify_ssl` (`mcp/assistants/src/codemie_mcp_assistants/model.py:85`, `mcp/datasources/src/codemie_mcp_datasources/server.py:37`, `mcp/workflows/src/codemie_mcp_workflows/model.py:63`) | 0% | Security-relevant: an unknown value must raise, not turn TLS off (`security.md`, "TLS"). Three copies, no test keeps them equal. |
| `mcp/workflows/src/codemie_mcp_workflows/server.py:52` | 0% | `execute_workflow` validates the SDK response with an aliased Pydantic model. No lockfile, so a new SDK release can break it with no failing check (`architecture.md`, "SDK Client And Settings"). |

## Known Test Debt

- No unit, integration or end-to-end tests in any package (`quality-gates.md`, "Gates that do not exist").
- `pytest` is a declared dev dependency in each package but has no tests and no configuration (`mcp/assistants/pyproject.toml:32`).
- `make test` is declared in `.PHONY` but has no recipe (`mcp/assistants/Makefile:1`). It prints `Nothing to be done`.
- CI has no test step and no coverage step (`.github/workflows/ci.yml:23-58`).
- No test guards the known defects in `architecture.md`, "Known Defects To Check Before You Copy A Pattern".
- Tool behaviour needs a live CodeMie installation. No mock client or fixture exists.

## Recent Test Activity

No test file exists in the current tree. `git log --diff-filter=AM -n 5 --name-only --pretty='' -- '*test*' '*spec*'` lists only three files under `scripts/tests/`. All three were later deleted when the scripts moved to the reusable workflows in `codemie-ai/ci-workflows`. They did not test the MCP packages.
