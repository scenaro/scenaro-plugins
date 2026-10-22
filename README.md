# Scenaro plugin

Connect your AI coding agent to Scenaro voice experiences using the hosted MCP service.

**MCP endpoint:** https://mcp.scenaro.io/mcp

An existing Scenaro account is required. Your browser opens for OAuth authorization: choose one company and the permissions you want to grant. Read access is required; draft edits, publication, synchronization and analytics refresh each require separate permissions. You can revoke access from the Scenaro Cockpit at https://app.scenaro.io/oauth/connections.

## Cursor

Install this plugin from its repository, or add the MCP server directly:

```json
{"mcpServers":{"scenaro":{"url":"https://mcp.scenaro.io/mcp"}}}
```

The public listing is submitted from this repository at [cursor.com/marketplace/publish](https://cursor.com/marketplace/publish). Cursor reviews the plugin before it appears in the marketplace.

## Claude Code

This repository is its own marketplace:

```sh
claude plugin marketplace add scenaro/scenaro-plugins
claude plugin install scenaro@scenaro
```

Open `/mcp` to authenticate. A listing in Anthropic's official directory is a separate review on claude.ai. Anyone who can clone this repository can install the plugin without that review.

## Codex and ChatGPT

```sh
codex plugin marketplace add scenaro/scenaro-plugins
```

The same package is the ChatGPT submission. Upload `.artifacts/scenaro-agent-0.3.0.zip` in the OpenAI plugin submission portal. Before the directory accepts it, Scenaro still has to verify the business identity, verify `mcp.scenaro.io`, and provide a demo recording. The live server already publishes the read-only, destructive, and open-world hints used by that review.

## Google Antigravity

Antigravity has a marketplace, but installation from it only accepts the curated catalog `antigravity-plugins-official`. A third-party listing goes through Google. Until then, install this repository directly:

```sh
agy plugin install https://github.com/scenaro/scenaro-plugins
```

The app reads `mcp_config.json` and connects to the same MCP server. Authentication uses dynamic client registration, then the Authenticate button in Customizations. You can also drop the folder in `~/.gemini/config/plugins/scenaro`.

## Mistral Vibe

Vibe reads the Agent Plugins manifest at `plugin.json`. There is no public Mistral marketplace to submit to. Install the `scenaro-agent` archive, or this repository, as `~/.vibe/plugins/scenaro`, then run `/reload-plugins` and `/mcp login scenaro`. Vibe also loads the Claude Code and Codex manifests, but the root manifest takes precedence.

## Available capabilities

Browse applications and scenarios, inspect conversations, collections, analytics and evaluation results. Separately authorized actions can edit drafts, create versions, publish a selected version, synchronize a connector or refresh analytics. No scenario is automatically published after editing.

[Documentation](https://mcp.scenaro.io/docs) · [Support](https://mcp.scenaro.io/support) · [Privacy](https://mcp.scenaro.io/privacy) · [Terms](https://mcp.scenaro.io/terms)

This repository contains plugin metadata and static assets only. It contains no credentials, user data or server implementation. Marketplace listings remain subject to each vendor’s review.

## Packaging and releases

GitHub Actions validates the manifests and uploads the ZIPs as workflow artifacts. To prepare a version, keep `server.json`, the root `plugin.json`, the three client manifests, and the Claude marketplace entry on the same version. Commit the changes, then push a matching `v<version>` tag. The workflow creates a draft GitHub release containing the ZIPs. `scenaro-agent` is the package for Mistral and the ChatGPT upload. Directory submission and publisher terms remain separate manual steps.

The private server repository owns the runtime and Terraform deployment. This public repository only packages metadata; it does not deploy AWS resources or publish to vendor directories.
