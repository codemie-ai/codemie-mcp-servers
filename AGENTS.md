# AGENTS.md

Primary AI entrypoint for `codemie-mcp-servers`. Load the relevant `.ai-run/guides/` file before changing code.

## Guide Imports

AGENTS.md has no native import directive. Open the paths below as plain files.

| Category | Guide Path | Purpose |
|---|---|---|
| Project | .ai-run/guides/project.md | Identity, tracker, ticket and PR adapters |
| Architecture | .ai-run/guides/architecture.md | Package layout, startup differences, tool inventory, SDK client, settings, known defects |
| Security | .ai-run/guides/security.md | Secrets, public repository content, TLS, CI permissions |
| Development | .ai-run/guides/development.md | Errors, logging, configuration, dependencies, versioning |
| Safety | .ai-run/guides/safety-no-go.md | Files, commands and actions that are off limits; same list as `.claude/settings.json` |
| Quality gates | .ai-run/guides/quality-gates.md | Exact checks per package, and gates that do not exist |
| QA strategy | .ai-run/guides/testing/qa-strategy.md | Test frameworks, test types, conventions, where new tests go |
| QA health | .ai-run/guides/testing/qa-health.md | Coverage state, risky untested areas, test debt |
| Code quality | .ai-run/guides/standards/code-quality.md | Lint and format state, type hints, naming |
| Git | .ai-run/guides/standards/git-workflow.md | Branches, commits, PR titles, merge strategy |
| Release | docs/RELEASING.md | Tags, versions, publish workflow |

## Task Classifier

| Category | User Intent | Example Requests | P0 Guide | P1 Guide |
|---|---|---|---|---|
| Tool | Add or change an MCP tool | "add a datasource tool" | .ai-run/guides/architecture.md | .ai-run/guides/development.md, .ai-run/guides/security.md |
| Package | Add a package or change the layout | "add a new MCP server" | .ai-run/guides/architecture.md | docs/RELEASING.md |
| Platform | Change SDK use, authentication or settings | "support client credentials" | .ai-run/guides/architecture.md | .ai-run/guides/development.md, .ai-run/guides/security.md |
| Security | Secrets, TLS, CI permissions | "review the token handling" | .ai-run/guides/security.md | .ai-run/guides/quality-gates.md |
| Verification | Run or add checks | "run the checks" | .ai-run/guides/quality-gates.md | .ai-run/guides/standards/code-quality.md |
| Testing | Write tests or assess test gaps | "add tests for datasources" | .ai-run/guides/testing/qa-strategy.md | .ai-run/guides/testing/qa-health.md, .ai-run/guides/quality-gates.md |
| Git | Commit, branch, PR | "open a PR" | .ai-run/guides/standards/git-workflow.md | .ai-run/guides/project.md |
| Release | Publish a package | "release assistants" | docs/RELEASING.md | .ai-run/guides/quality-gates.md |

## Critical Rules

| Rule | Trigger | Action |
|---|---|---|
| Check Guides First | ANY task | Match request to category and load the P0 guide before searching broadly |
| Safety | ANY file read, shell command or release step | Never do what `.ai-run/guides/safety-no-go.md` lists. Ask a person instead. |
| Testing | "write tests" / "run tests" | Only write or run tests when requested or when needed for verification. Load `.ai-run/guides/quality-gates.md` and `.ai-run/guides/testing/qa-strategy.md` first. |
| Git Operations | "commit" / "push" / "PR" | Only then; load `.ai-run/guides/standards/git-workflow.md` |
| Shell | ANY shell command | Use bash/Linux-compatible syntax |
| Public Content | ANY change to a tracked file | Load the "Public repository content" section of `.ai-run/guides/security.md` |
| Release | "release" / "publish" | Only when asked; load `docs/RELEASING.md` |

## Commands

| Need | Source Guide | Source Evidence | Notes |
|---|---|---|---|
| Lint / format | .ai-run/guides/quality-gates.md | .github/workflows/ci.yml, package Makefile | Run per package |
| Build / smoke test | .ai-run/guides/quality-gates.md | .github/workflows/ci.yml | Run per package |
| Tests | .ai-run/guides/quality-gates.md, .ai-run/guides/testing/qa-strategy.md | none | The repository has no tests |
| Git / review workflow | .ai-run/guides/standards/git-workflow.md | CONTRIBUTING.md, git history | Load guide before git operations |
