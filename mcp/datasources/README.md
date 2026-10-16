# CodeMie Datasources MCP Server

Python server implementing Model Context Protocol (MCP) for CodeMie Datasources operations.

## Features
- List and filter datasources
- Get datasource details
- Create code datasources
- Update datasources
- Delete datasources
- Monitor datasource processing status

Note: The server requires authentication credentials via environment variables.

## API

### Tools

#### list_datasources
Get list of available datasources with filtering and pagination
Inputs:
- `page (integer, optional)`: Page number (default: 0)
- `per_page (integer, optional)`: Items per page (default: 10)
- `sort_key (string, optional)`: Sort by 'date' or 'update_date' (default: 'update_date')
- `sort_order (string, optional)`: Sort order 'asc' or 'desc' (default: 'desc')
- `datasource_types (array, optional)`: Filter by datasource types
- `projects (array, optional)`: Filter by project names
- `owner (string, optional)`: Filter by owner
- `status (string, optional)`: Filter by status

Returns list of datasources with their details

#### get_datasource
Get detailed information about a specific datasource
Inputs:
- `datasource_id (string)`: ID of the datasource to retrieve

Returns complete datasource details including configuration

#### create_code_datasource
Create a new code datasource
Inputs:
- `name (string)`: Datasource name (lowercase letters and underscores only)
- `description (string)`: Datasource description
- `project_name (string)`: Project name
- `repository_link (string)`: Git repository URL
- `branch (string)`: Git branch name
- `index_type (string, optional)`: Type of indexing - 'code', 'summary', or 'chunk-summary' (default: 'code')
- `files_filter (string, optional)`: File patterns to include/exclude
- `embeddings_model (string, optional)`: Model for embeddings generation
- `shared_with_project (boolean, optional)`: Whether datasource is shared with project (default: false)

Returns created datasource details

#### update_code_datasource
Update an existing code datasource
Inputs:
- `datasource_id (string)`: ID of the datasource to update
- `name (string, optional)`: New name
- `description (string, optional)`: New description
- `branch (string, optional)`: New branch
- `files_filter (string, optional)`: New files filter
- `full_reindex (boolean, optional)`: Whether to perform full reindex
- `skip_reindex (boolean, optional)`: Whether to skip reindex
- `resume_indexing (boolean, optional)`: Whether to resume indexing

Returns updated datasource details

#### delete_datasource
Delete a datasource
Inputs:
- `datasource_id (string)`: ID of the datasource to delete

Returns deletion confirmation

#### get_datasource_processing_info
Get datasource processing status and progress
Inputs:
- `datasource_id (string)`: ID of the datasource to get info for

Returns processing information including status, progress, and file counts

## Breaking changes in 0.2.0

- The Python package is now `codemie_mcp_datasources`. The command `codemie-mcp-datasources` is unchanged.
- The server no longer has built-in server addresses. `CODEMIE_AUTH_SERVER_URL`, `CODEMIE_AUTH_REALM_NAME` and `CODEMIE_API_DOMAIN` are required. Without them the server exits with an error.
- TLS certificate verification is now on by default. Earlier versions turned it off in this server. Set `CODEMIE_VERIFY_SSL=false` to keep the old behavior for local testing only.

## Installation

Ensure you have `Python 3.12` or later installed.

**Important:** Before running the MCP server, you must configure the required environment variables (see [Environment Variables](#environment-variables) section below).

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *codemie-mcp-datasources*.

```bash
uvx codemie-mcp-datasources
```
#### create_git_faq_datasource

Creates a Git FAQ datasource (`knowledge_base_git_faq`). Every `.md` file in the repository
(narrowed only by the optional gitignore-style `files_filter`) is parsed as an FAQ article, split
into embedded H1-H3 section chunks, and searched through the standard hybrid knowledge-base
retrieval flow.

```
create_git_faq_datasource(
  name="team_faq",
  description="Team FAQ articles",
  project_name="my_project",
  repository_link="https://github.com/org/docs",
  branch="main",
  files_filter="docs/**/*.md\n!docs/internal/**",
)
```


### Using pip

Alternatively you can install the package with pip:

```bash
pip install codemie-mcp-datasources
```

After installation, you can run it as a script using:

```bash
codemie-mcp-datasources
```

## Configuration

### Configure for Claude.app

Add to your Claude settings:

<details>
<summary>Using uvx</summary>

**Required variables:**
```json
"mcpServers": {
  "codemie-datasources": {
    "command": "uvx",
    "args": ["codemie-mcp-datasources"],
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
<summary>Using pip installation</summary>

**Required variables:**
```json
"mcpServers": {
  "codemie-datasources": {
    "command": "codemie-mcp-datasources",
    "args": [],
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

## Build

### Make build:
```bash
make build
```
