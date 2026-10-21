# Scenaro plugin

Connect your AI coding agent to Scenaro voice experiences using the hosted MCP service.

**MCP endpoint:** https://mcp.scenaro.io/mcp

An existing Scenaro account is required. Your browser opens for OAuth authorization: choose one company and the permissions you want to grant. Read access is required; draft edits, publication, synchronization and analytics refresh each require separate permissions. You can revoke access from the Scenaro Cockpit at https://app.scenaro.io/oauth/connections.

## Cursor

Install this plugin from its repository or add the following to your Cursor MCP configuration, then use the connection button:

```json
{"mcpServers":{"scenaro":{"url":"https://mcp.scenaro.io/mcp"}}}
```

## Claude Code

```sh
claude mcp add --transport http --scope user scenaro https://mcp.scenaro.io/mcp
```

Open `/mcp` to authenticate.

## Codex

```sh
codex mcp add scenaro --url https://mcp.scenaro.io/mcp
codex mcp login scenaro
```

## Available capabilities

Browse applications and scenarios, inspect conversations, collections, analytics and evaluation results. Separately authorized actions can edit drafts, create versions, publish a selected version, synchronize a connector or refresh analytics. No scenario is automatically published after editing.

[Documentation](https://mcp.scenaro.io/docs) · [Support](https://mcp.scenaro.io/support) · [Privacy](https://mcp.scenaro.io/privacy) · [Terms](https://mcp.scenaro.io/terms)

This repository contains plugin metadata and static assets only. It contains no credentials, user data or server implementation. Marketplace listings remain subject to each vendor’s review.

## Packaging and releases

GitHub Actions validates all three plugin manifests on every push and pull request, then uploads the ZIPs as workflow artifacts. To prepare a version, keep `server.json` and all three `plugin.json` versions aligned, commit the changes, then push a matching `v<version>` tag. The workflow creates a draft GitHub release containing the three ZIPs. Directory submission and publisher terms remain separate manual steps.

The private server repository owns the runtime and Terraform deployment. This public repository only packages metadata; it does not deploy AWS resources or publish to vendor directories.
