<div align="center">

<img src="assets/codemie-logo.svg" alt="CodeMie" width="96" />

# CodeMie MCP Servers

**Model Context Protocol servers for the CodeMie platform.**

[![PyPI](https://img.shields.io/pypi/v/codemie-mcp-assistants.svg?style=flat-square&label=PyPI)](https://pypi.org/project/codemie-mcp-assistants/)
[![CI](https://img.shields.io/github/actions/workflow/status/codemie-ai/codemie-mcp-servers/ci.yml?branch=main&style=flat-square&label=CI)](https://github.com/codemie-ai/codemie-mcp-servers/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg?style=flat-square)](#requirements)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=flat-square)](LICENSE)

</div>

## What is it

[MCP](https://modelcontextprotocol.io) servers that let AI tools such as Claude Desktop work with your [CodeMie](https://www.codemie.ai/) installation. Each server is a separate Python package with its own README, usage and examples.

| Package | Path | Command | Registry |
|---------|------|---------|----------|
| [`codemie-mcp-assistants`](mcp/assistants/README.md) | `mcp/assistants` | `codemie-mcp-assistants` | PyPI |
| [`codemie-mcp-datasources`](mcp/datasources/README.md) | `mcp/datasources` | `codemie-mcp-datasources` | PyPI |
| [`codemie-mcp-workflows`](mcp/workflows/README.md) | `mcp/workflows` | `codemie-mcp-workflows` | not published yet |

```bash
uvx codemie-mcp-assistants
```

## Related repository

These servers are clients of the CodeMie API: an AI tool connects to the servers, and the servers call your CodeMie installation. They are not the same as [codemie-mcp-connect-service](https://github.com/codemie-ai/codemie-mcp-connect-service). That service works the other way round: it lets CodeMie call local stdio MCP servers over HTTP. The two projects share no code and do not depend on each other.

The client SDKs and the infrastructure-as-code tools live in [codemie-sdk](https://github.com/codemie-ai/codemie-sdk) and [codemie-cdk](https://github.com/codemie-ai/codemie-cdk).

## Requirements

- Python 3.12 or later
- `codemie-sdk-python` `>=0.1.620 <0.2` (installed as a dependency)
- A CodeMie installation. You must set `CODEMIE_AUTH_SERVER_URL`, `CODEMIE_AUTH_REALM_NAME` and `CODEMIE_API_DOMAIN`. The servers have no built-in addresses and exit with an error when one of them is missing.

## Documentation

- [What is CodeMie](https://docs.codemie.ai/user-guide/getting-started/what-is-codemie/): an introduction to the platform.
- [CodeMie documentation](https://docs.codemie.ai/): user guides and platform reference.

## Contributing

Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md) first.

## Security

Do not report vulnerabilities in public issues. Follow [SECURITY.md](SECURITY.md).

For bugs and feature requests, use [GitHub Issues](https://github.com/codemie-ai/codemie-mcp-servers/issues).

## Releasing

See [docs/RELEASING.md](docs/RELEASING.md).

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE).
