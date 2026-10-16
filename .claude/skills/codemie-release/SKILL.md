---
name: codemie-release
description: Release a package of codemie-mcp-servers to PyPI. Use when the user says "release", "publish a version", "cut a release" or "make an rc". Checks the repo, picks the next version from the registry, runs a dry run, writes release notes and creates the GitHub Release that starts the publish workflow.
---

# CodeMie release for codemie-mcp-servers

A release starts when a GitHub Release is published. The workflow builds, checks and publishes the package. The tag is the version. The manifest holds only the base line `MAJOR.MINOR.0` and is never changed by a release. Read `RELEASING.md` for the full rules.

**Never publish the GitHub Release without an explicit "yes" from the user.** It publishes the package to a public registry. This cannot be undone.

## Packages

| Package | Registry | Tag prefix | Directory | Manifest |
|---------|----------|------------|-----------|----------|
| `codemie-mcp-assistants` | PyPI | `mcp-assistants-v` | `mcp/assistants` | `pyproject.toml` |
| `codemie-mcp-datasources` | PyPI | `mcp-datasources-v` | `mcp/datasources` | `pyproject.toml` |
| `codemie-mcp-workflows` | PyPI | `mcp-workflows-v` | `mcp/workflows` | `pyproject.toml` |

All packages use the workflow `publish.yml`. One tag releases one package. To release all three, make three Releases, one by one.

## 1. Pre-flight

Stop and tell the user if a check fails.

```bash
git branch --show-current          # must be main
git status --porcelain             # must be empty
git fetch origin && git rev-list --left-right --count HEAD...origin/main   # must be "0 0"
gh run list --branch main --limit 3 --json conclusion,workflowName,headSha # CI on HEAD must be success
gh auth status
```

Ask which package to release if the user did not say.

## 2. Choose the version

1. Read the base line from the manifest.
   ```bash
   grep -m1 '^version' mcp/<name>/pyproject.toml
   ```
2. Read the latest published version.
   ```bash
   curl -s https://pypi.org/pypi/codemie-mcp-<name>/json | python3 -c "import sys,json; print(json.load(sys.stdin)['info']['version'])"
   ```
   A package that is not on PyPI yet gives HTTP 404. This is fine: it is the first release.
3. Propose the next version:
   - Same `MAJOR.MINOR` as the base line: latest + 1 patch.
   - Registry on an older line than the base line: `MAJOR.MINOR.0` of the base line.
   - Release candidate: `-rcN` on the next version, with N one higher than the last rc of that version.
4. A new minor or major line needs the base raised in the manifest first, and merged. Stop and say so.
5. Show: package, base line, latest on the registry, proposed tag. Ask the user to confirm or give another version.

The tag is `<prefix>X.Y.Z` or `<prefix>X.Y.Z-rcN`. The workflow fails closed if the version is not higher than the registry.

## 3. Dry run

There is no local dry run script. Run the workflow in dry-run mode from `main`. It builds and runs the version gate. It publishes nothing.

```bash
gh workflow run publish.yml --ref main -f tag=mcp-<name>-vX.Y.Z -f dry_run=true
gh run watch      # pick the run you just started
```

If the dry run fails, stop. Report the failing step. Do not continue.

## 4. Release notes

Find the previous tag of this package. For a stable release skip `-rc` tags. For an rc use the previous tag of any kind.

```bash
PREV=$(git tag -l '<prefix>*' --sort=-v:refname | grep -v -- '-rc' | head -1)   # stable
git log --pretty='%s' ${PREV:+$PREV..HEAD} -- mcp/<name>
```

Only list commits that touch the package. Group them by the commit prefix: `feat`, `fix`, `perf`, `refactor`, `docs`, `chore`. Put breaking changes first (`BREAKING CHANGE:` in a commit body). Keep PR numbers. Do not put internal URLs, ticket keys or customer names in the notes.

```markdown
## What's changed

### Features
- Description (#PR)

### Bug fixes
- Description (#PR)

**Full changelog**: https://github.com/codemie-ai/codemie-mcp-servers/compare/<PREV>...<TAG>
```

Show the notes to the user.

## 5. Publish the Release

After the user says "yes" to the tag and the notes:

```bash
gh release create <TAG> --target main --title "<TAG>" --notes "<NOTES>" [--prerelease for an rc]
```

Do not save a draft: a draft does not start the workflow. Skip this step if `gh release view <TAG>` shows the release already.

## 6. After the release

```bash
gh run list --workflow publish.yml --limit 3
gh run watch            # pick the run of the new tag
```

`publish` may wait for approval if the `release` environment has reviewers. Tell the user. When the run is green, check the registry:

```bash
pip index versions codemie-mcp-<name> | head -1
```

Report the tag, the run URL, the registry link and the install command.

## If something fails

- `verify` fails: read the log, fix on `main`, then use a **new** tag. Never re-use or move a tag of a published version.
- Tag is wrong and nothing is published yet: `gh release delete <TAG> --cleanup-tag --yes`, after the user agrees.
- A published version cannot be changed. Release a higher patch version instead.
