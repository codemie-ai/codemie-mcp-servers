# Releasing

Each package is released on its own by the GitHub Actions workflow `publish.yml`. A release starts when someone with write access publishes a GitHub Release whose tag names the package and the version.

| Package | Directory | Registry | Tag |
|---------|-----------|----------|-----|
| `codemie-mcp-assistants` | `mcp/assistants` | PyPI | `mcp-assistants-vX.Y.Z` or `mcp-assistants-vX.Y.Z-rcN` |
| `codemie-mcp-datasources` | `mcp/datasources` | PyPI | `mcp-datasources-vX.Y.Z` or `mcp-datasources-vX.Y.Z-rcN` |
| `codemie-mcp-workflows` | `mcp/workflows` | PyPI | `mcp-workflows-vX.Y.Z` or `mcp-workflows-vX.Y.Z-rcN` |

A merge to `main` never releases a package. A tag with another prefix does not publish anything: the `resolve` job fails.

## How to release

1. Merge the changes you want to release to `main`. Wait for CI to pass.
2. Choose the version. It must be higher than the highest version of that package on PyPI and on the line in its `pyproject.toml` (see below).
3. Create the Release. Use **Publish release**: **Save draft** does not start a workflow.
   - UI: Releases > Draft a new release > choose a new tag such as `mcp-assistants-v0.2.1`, target `main` > Publish release.
   - CLI: `gh release create mcp-assistants-v0.2.1 --target main --generate-notes`
4. Open the run in the Actions tab. `verify` builds and checks. `publish` waits for approval if the `release` environment has reviewers.

One tag releases one package. To release all three, create three Releases.

## How versions work

The tag is the version: `mcp-assistants-v0.2.1` releases `0.2.1` of `codemie-mcp-assistants`. Each `pyproject.toml` holds only the base line, `MAJOR.MINOR.0`. It is `0.2.0` for all three packages today.

- The tag must be `MAJOR.MINOR.PATCH` on the same `MAJOR.MINOR` line as the package `pyproject.toml`. The only pre-release form is `-rcN`, for example `mcp-assistants-v0.2.1-rc1`. A missing part or a leading zero fails.
- The tag prefix must belong to the package of the job. A tag `mcp-workflows-v0.2.1` never releases `codemie-mcp-assistants`.
- The workflow stamps the version into the build only (`poetry version`). It does not commit a version change.
- To start a new line, raise the base in `pyproject.toml`, for example to `0.3.0`, and merge it. Then tag `mcp-assistants-v0.3.0`.
- Runs are grouped by tag and package, so a release is never cancelled by a newer one.

## Checks before anything is published

The `verify` job has no secrets. It fails, and nothing is published, when:

- the tagged commit is not on `main`;
- for a manual publish, the tag does not exist or does not point to the dispatched commit;
- the tag prefix, format or line does not match;
- the version is equal to or lower than the highest published version (`scripts/release/check_version.py`);
- lint or the build fail.

The `publish` job runs the version check again right before the upload, because it can wait for approval and another release may land in between.

`scripts/release/check_version.py` compares the version with the live PyPI registry.

- A package that is not on PyPI yet (HTTP 404) has no latest version. The check passes.
- A timeout, network error, malformed registry response or a published version that cannot be parsed stops the release. The gate fails closed.

Print the version a tag names (no network):

```bash
python3 scripts/release/check_version.py --ecosystem pypi --name codemie-mcp-assistants --tag mcp-assistants-v0.2.1 --base 0.2.0 --tag-prefix mcp-assistants-v
```

## Admin prerequisites

An administrator does these steps once. This document only lists them.

- **Repository.** Create the public repository `codemie-ai/codemie-mcp-servers`.
- **GitHub environment `release`.** Create it in Settings > Environments. Restrict deployments to the tags `mcp-assistants-v*`, `mcp-datasources-v*` and `mcp-workflows-v*` (and `main` for a manual publish). Add required reviewers if a second approval is wanted.
- **Who can release.** Only people with write access can create a Release. Keep that group small.
- **PyPI token (temporary).** For now the workflow publishes with the repository secret `PYPI_API_TOKEN`, set in Settings > Secrets and variables > Actions. This is a temporary setup for tests.
- **PyPI trusted publishers (target).** The target is OpenID Connect with no stored token. For each package, add a trusted publisher in the PyPI project settings: repository `codemie-ai/codemie-mcp-servers`, workflow `publish.yml`, environment `release`. `codemie-mcp-assistants` and `codemie-mcp-datasources` already exist on PyPI. `codemie-mcp-workflows` may not: add a pending publisher for it on PyPI (Account > Publishing) with the same values, before the first release. Only the `publish` job has the `id-token: write` permission.
- **First commit.** Push the first exported snapshot to the new repository as a single commit. The export carries no history.
