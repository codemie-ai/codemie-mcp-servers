# Architecture Guide

**Project**: CodeMie MCP Servers
**Style**: three independent Python packages in one repository. No workspace manifest and no shared code.
**Language**: Python 3.12 (`mcp/assistants/pyproject.toml`, `[tool.poetry.dependencies]`) | **Framework**: `mcp` FastMCP (`mcp/assistants/src/codemie_mcp_assistants/server.py`, `FastMCP("codemie-assistants")`)

## Overview

```
AI tool (stdio) -> codemie-mcp-<package> (FastMCP) -> codemie-sdk-python (CodeMieClient) -> CodeMie API
```

Each server is a client of the CodeMie API. It is not related to `codemie-mcp-connect-service`, which works in the other direction (`README.md`). The public API of this repository is the set of MCP tools. The transport is stdio (`main()` in each `server.py`, `mcp.run(transport="stdio")`). There are no HTTP routes.

## Component Structure

| Path | Purpose | Entry point |
|---|---|---|
| `mcp/assistants` | One chat tool for one configured assistant | `mcp/assistants/pyproject.toml`, `[tool.poetry.scripts]`; `main` in `server.py` |
| `mcp/datasources` | Datasource list, read, create, update, delete tools | `main` in `mcp/datasources/src/codemie_mcp_datasources/server.py` |
| `mcp/workflows` | One tool that starts a workflow | `main` in `mcp/workflows/src/codemie_mcp_workflows/server.py` |
| `.github/workflows` | CI, CodeQL, PR title check, PyPI publish | `.github/workflows/ci.yml` |
| `docs/RELEASING.md` | Release procedure. Source of truth for releases. | `docs/RELEASING.md` |

Each package has `Makefile`, `README.md`, `pyproject.toml` and `src/codemie_mcp_<package>/`. The three Makefiles are identical. The `model.py` file exists only in assistants and workflows.

## Package Differences

This table is the single home of the differences. Commands are in `quality-gates.md`.

| Package | Settings read | Network at import | Auth | Dependencies that differ |
|---|---|---|---|---|
| assistants | At import (`Settings()` in `server.py`) | Yes. `get_assistant_info` fetches the assistant to name the tool. | Username and password, or client credentials (`AuthConfig.validate_auth_method` in `model.py`) | `httpx ^0.28.1`, `pydantic ^2.11.2` |
| datasources | In `main()` and on each `get_client()` (`validate_settings` in `server.py`) | No | Username and password only. `CODEMIE_AUTH_CLIENT_SECRET` is not read (`get_client`). | `httpx ^0.27.0`, no `pydantic` |
| workflows | At import (`WorkflowSettings()` in `server.py`) | No | Username and password, or client credentials (`WorkflowAuthConfig.validate_auth_method` in `model.py`) | `httpx ^0.27.0`, `pydantic ^2.11.2` |

All three use `codemie-sdk-python >=0.1.620,<0.2`, `mcp ^1.6.0` and `certifi`.

## Dependency Rules

| Rule | Evidence |
|---|---|
| Packages do not import each other. A change in shared behaviour is three edits. | `REQUIRED_SETTINGS` in `mcp/assistants/src/codemie_mcp_assistants/model.py`, `mcp/datasources/src/codemie_mcp_datasources/server.py` and `mcp/workflows/src/codemie_mcp_workflows/model.py` |
| Platform calls go through `CodeMieClient`, not direct HTTP | `get_client` in `mcp/datasources/src/codemie_mcp_datasources/server.py` |
| Dependency versions differ per package. Check before you assume they match. | `[tool.poetry.dependencies]` in each `pyproject.toml` |

## Adding A Tool Or Package

| Change | Steps |
|---|---|
| New tool | Add a `@mcp.tool()` function in the package `server.py`. Document it in the package `README.md`. Follow "Tool Patterns" below. |
| New package | Add `mcp/<name>`. Add it to the CI matrix (`.github/workflows/ci.yml`, `matrix.package`), the tag mapping (`.github/workflows/publish.yml`, step "Map the tag prefix to a package"), the table in `docs/RELEASING.md`, and the package lists in `README.md` and `CONTRIBUTING.md`. |

## Boundaries

| Do | Do not |
|---|---|
| Keep each package installable alone | Add a shared module that one package imports from another path |
| Keep the settings check before any network call (`README.md`) | Add built-in server addresses |
| Change the three packages together when the rule is shared | Fix a shared rule in one package only |

## Tool Inventory

| Package | Tool | Definition (`server.py` of the package) |
|---|---|---|
| assistants | `ask_<assistant name>` (dynamic) | `chat_with_assistant` |
| datasources | `list_datasources` | `list_datasources` |
| datasources | `get_datasource` | `get_datasource` |
| datasources | `create_code_datasource` | `create_code_datasource` |
| datasources | `create_git_faq_datasource` | `create_git_faq_datasource` |
| datasources | `delete_datasource` | `delete_datasource` |
| datasources | `update_code_datasource` | `update_code_datasource` |
| datasources | `get_datasource_processing_info` | `get_datasource_processing_info` |
| workflows | `execute_workflow` | `execute_workflow` |

## Tool Patterns

Write an `async def` with `@mcp.tool()`. The type hints and the docstring are the schema that the AI tool reads.

| Bad | Best |
|---|---|
| Free-form string for a closed set | `Literal` type, see `list_datasources` in the datasources `server.py` |
| No `Args:` section | One line per parameter, see `list_datasources` |
| Return an SDK object | Return a plain dict, see `get_datasource` |
| New tool without README entry | Add it to the package `README.md`, section "API" |

Validation differs by package:

| Package | Approach | Evidence |
|---|---|---|
| workflows | Pydantic request and response models | `WorkflowExecutionRequest`, `WorkflowExecutionResponse` in `mcp/workflows/src/codemie_mcp_workflows/model.py` |
| assistants | Manual checks with `ValueError` | `chat_with_assistant` in the assistants `server.py` |
| datasources | SDK request models | `create_code_datasource` in the datasources `server.py` |

`list_datasources` takes `page` and `per_page`, with defaults 0 and 10.

### Dynamic Tool Name

The assistants tool name comes from platform data. `sanitize_tool_name` must produce a name that matches `^[a-zA-Z0-9_-]{1,64}$` (`mcp/assistants/src/codemie_mcp_assistants/server.py`). See the known defect below.

## SDK Client And Settings

Each package has its own `get_client()`. It creates a new `CodeMieClient` per call. No package caches a client, although datasources declares an unused `_client` variable.

| Bad | Best |
|---|---|
| Direct `httpx` call to the API | SDK call through `get_client()` |
| Hardcoded address | Required environment setting (`REQUIRED_SETTINGS`) |
| Assume all packages accept client credentials | Check the Package Differences table |

| Variable | Required | Default |
|---|---|---|
| `CODEMIE_AUTH_SERVER_URL`, `CODEMIE_AUTH_REALM_NAME`, `CODEMIE_API_DOMAIN` | Yes, an empty value counts as missing | none |
| `CODEMIE_ASSISTANT_ID` | Assistants only, per the README | none. The code does not validate it (`Settings` in `model.py`). |
| `CODEMIE_AUTH_CLIENT_ID` | No | `codemie-sdk` |
| `CODEMIE_VERIFY_SSL` | No | `true`. An unknown value is an error (`_read_verify_ssl`). |

The servers have no retry, rate-limit or timeout logic of their own. They log to stderr and raise. Details are in `development.md`.

Imports from `codemie_sdk.models.*` tie the servers to SDK models. The workflows response model reads aliased SDK fields (`WorkflowExecutionResponse`). Check these when you change the lower bound of the SDK range. No lockfile exists, so CI resolves the newest allowed SDK on each run.

External services: the CodeMie API (through the SDK), PyPI (publication) and `codemie-ai/ci-workflows` (reusable workflows). Token, pinning and permissions are in `security.md`. Release steps are in `docs/RELEASING.md`.

## Known Defects To Check Before You Copy A Pattern

| Location | Finding |
|---|---|
| `create_code_datasource`, `create_git_faq_datasource`, `update_code_datasource` in the datasources `server.py` | Each returns `get_datasource(...)` with no `await`, and `get_datasource` is `async def`. The caller gets a coroutine. |
| `update_code_datasource` in the datasources `server.py` | `branch or current.code.branch if current.code else None` drops a supplied `branch` when `current.code` is empty, because of operator precedence. |
| `sanitize_tool_name` in the assistants `server.py` | The length check uses 60 and the slice uses 64. The `ask_` prefix is added after that, where `chat_tool_name` is set. A long name can pass 64 characters. |
| `mcp/workflows/README.md`, section "API" | The README documents a tool `execute` with `parameters`. The code has `execute_workflow` with `user_input`. Trust the code. |
| `mcp/datasources/README.md`, section "Environment Variables" | The README offers client credentials. The code requires username and password. Trust the code. |
| `pyproject.toml` of each package | The base version sits in two places. Poetry uses only `[project].version` and ignores the `[tool.poetry]` copy. See "Versioning" in `development.md`. |

These come from reading the code. No test or live run confirmed them.
