# Project Context

## Project Identity

| Field | Value | Source |
|---|---|---|
| Project name | CodeMie MCP Servers | `README.md` |
| Repository/package | codemie-ai/codemie-mcp-servers; packages codemie-mcp-assistants, codemie-mcp-datasources, codemie-mcp-workflows | `CONTRIBUTING.md`, `[project] name` in each `mcp/*/pyproject.toml` |
| Project code/key | `EPMCDME-NNNNN` (placeholder form) | user decision |

## Work Item Tracker

| Field | Value |
|---|---|
| Provider | Jira |
| Key/prefix | `EPMCDME-NNNNN` (placeholder) |

> Adapter configuration belongs exclusively in `## Ticket Adapter`. Do not duplicate adapter status or instructions in the Work Item Tracker table.

Public content rules: `.ai-run/guides/development/security-patterns.md`, section "Public repository content".

## Ticket Adapter

**Status**: configured
**Adapter**: Invoke the `codemie-jira-assistant` skill via the Skill tool. The skill is for maintainers only and this repository does not ship it. If the skill is not loaded in your session, treat this adapter as not configured and skip the ticket steps.
**Lookup**: Invoke the `codemie-jira-assistant` skill with the ticket key and a request for summary, description, acceptance criteria, and links.
**Create**: Invoke the `codemie-jira-assistant` skill with the complete ticket payload or approved story file as the argument.
**Output**: Ticket key and URL returned by the skill.
**Comment**: Invoke the `codemie-jira-assistant` skill with a request to add a comment to the ticket, passing the comment body as the argument.

## Source Control And Review

| Field | Value |
|---|---|
| Provider | GitHub |
| Repository remote | `https://github.com/codemie-ai/codemie-mcp-servers.git` |
| Default target branch | main |
| Review artifact type | PR |

## MR Adapter

**Status**: configured
**Adapter**: `gh` CLI
**Instructions**: In a clone of a fork, run `gh repo set-default codemie-ai/codemie-mcp-servers` once, or export `GH_REPO=codemie-ai/codemie-mcp-servers`. Otherwise bare `gh` commands resolve against the fork and do not find the PR. Create the PR with `gh pr create --repo codemie-ai/codemie-mcp-servers --base main`. Read the status with `gh pr view <number>` and `gh pr checks <number>`. Load `.ai-run/guides/standards/git-workflow.md` for the title format and the rule on ticket keys.

## Complexity Scoring

**Status**: not configured
**Field**: not configured
**Format**: not configured
