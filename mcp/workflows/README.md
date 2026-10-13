# CodeMie Workflows MCP Server

Python server implementing Model Context Protocol (MCP) for CodeMie Workflows operations.

## Features
- Execute CodeMie workflows
- Manage workflow executions
- Integration with CodeMie Workflow API

Note: The server requires authentication credentials via environment variables.

## API

### Tools

#### execute
Execute a specific workflow
Inputs:
- `workflow_id (string)`: Workflow identifier to execute
- `parameters (object, optional)`: Workflow execution parameters
- `execution_id (string, optional)`: Custom execution identifier

Returns workflow execution details and status

## Breaking changes in 0.2.0

- The server no longer has built-in server addresses. `CODEMIE_AUTH_SERVER_URL`, `CODEMIE_AUTH_REALM_NAME` and `CODEMIE_API_DOMAIN` are required. Without them the server exits with an error.

## Installation

Ensure you have `Python 3.12` or later installed.

**Important:** Before running the MCP server, you must configure the required environment variables (see [Environment Variables](#environment-variables) section below).

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *codemie-mcp-workflows*.

```bash
uvx codemie-mcp-workflows
```

### Using Poetry

Alternatively you can install via Poetry:

```bash
poetry install codemie-mcp-workflows
```

After installation, you can run it as a script using:

```bash
poetry run codemie-mcp-workflows
```

## Configuration 

### Configure for Claude.app

Add to your Claude settings:

<details>
<summary>Using uvx</summary>

**Required variables:**
```json
"mcpServers": {
  "codemie-workflows": {
    "command": "uvx",
    "args": ["codemie-mcp-workflows"],
    "env": {
      "CODEMIE_AUTH_SERVER_URL": "https://auth.example.com/auth",
      "CODEMIE_AUTH_REALM_NAME": "your-realm",
      "CODEMIE_API_DOMAIN": "https://codemie.example.com/code-assistant-api",
      "CODEMIE_USERNAME": "your-username",
      "CODEMIE_PASSWORD": "your-password"
    }
  }
}
```

**Optional variables:**
```json
"env": {
  "CODEMIE_AUTH_CLIENT_ID": "codemie-sdk",
  "CODEMIE_VERIFY_SSL": "true"
}
```
</details>

<details>
<summary>Using poetry installation</summary>

**Required variables:**
```json
"mcpServers": {
  "codemie-workflows": {
    "command": "poetry",
    "args": ["run", "codemie-mcp-workflows"],
    "env": {
      "CODEMIE_AUTH_SERVER_URL": "https://auth.example.com/auth",
      "CODEMIE_AUTH_REALM_NAME": "your-realm",
      "CODEMIE_API_DOMAIN": "https://codemie.example.com/code-assistant-api",
      "CODEMIE_USERNAME": "your-username",
      "CODEMIE_PASSWORD": "your-password"
    }
  }
}
```

**Optional variables:**
```json
"env": {
  "CODEMIE_AUTH_CLIENT_ID": "codemie-sdk",
  "CODEMIE_VERIFY_SSL": "true"
}
```
</details>

### Environment Variables

#### Mandatory Variables

The following environment variables **must** be configured before running the MCP server:

**Platform settings (all three are required, an empty value counts as missing):**
- `CODEMIE_AUTH_SERVER_URL`: URL of your authentication server, for example `https://auth.example.com/auth`
- `CODEMIE_AUTH_REALM_NAME`: authentication realm name
- `CODEMIE_API_DOMAIN`: URL of your CodeMie API, for example `https://codemie.example.com/code-assistant-api`

The server has no built-in addresses. If any of the three is missing it prints `Missing required settings: <names>` and exits with a non-zero code, before any network call.

**Authentication (choose one method):**

*Option 1: Username/Password*
- `CODEMIE_USERNAME`: Your CodeMie username
- `CODEMIE_PASSWORD`: Your CodeMie password

*Option 2: Client Credentials*
- `CODEMIE_AUTH_CLIENT_SECRET`: Auth client secret

#### Optional Variables

- `CODEMIE_AUTH_CLIENT_ID`: authentication client ID (default: `codemie-sdk`)

- `CODEMIE_VERIFY_SSL`: TLS certificate verification flag (default: `true`). Set `false` only for local testing.
