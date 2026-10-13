# Contributing

Contributions are welcome. Please read the [Code of Conduct](CODE_OF_CONDUCT.md) before you start.

This repository contains three packages, each in its own folder under `mcp/`:

- `mcp/assistants`: `codemie-mcp-assistants`
- `mcp/datasources`: `codemie-mcp-datasources`
- `mcp/workflows`: `codemie-mcp-workflows`

## How to Contribute

1. Fork `codemie-ai/codemie-mcp-servers` on GitHub.
2. Clone your fork and create a branch: `git checkout -b my-feature-branch`.
3. Make your change.
4. Run the checks (see below).
5. Push the branch to your fork and open a pull request against `main`.

## Pull Requests

- The PR title must follow [Conventional Commits](https://www.conventionalcommits.org/): `<type>(<optional scope>): <description>`, for example `feat(workflows): add run status tool` or `fix(datasources): handle empty response`.
- Allowed types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
- Keep a PR focused on one change. Describe what changed and why.
- Individual commit messages are not checked.

## Review Rule

Every PR needs one approval from any collaborator with write access before it can be merged. All CI checks must pass.

## Local Checks

Run the checks in the folder of the package you changed. The packages have no lockfile, so install the dependencies fresh:

```bash
cd mcp/assistants
poetry install
poetry run ruff check .
poetry build
```

CI runs the same steps for each package. It also starts the installed command with the three platform settings unset and expects a non-zero exit code with the message `Missing required settings`.

## Internal References and Secrets

CI scans the tree for internal references and for secrets. Do not commit credentials, private hostnames, ticket keys, or personal e-mail addresses. Use placeholders such as `https://codemie.example.com` in examples.

## Reporting Issues

Use GitHub Issues for bugs and feature requests. For security problems, follow [SECURITY.md](SECURITY.md).
