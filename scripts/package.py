"""Validate and package public plugin metadata. No server implementation or credentials."""
from pathlib import Path
import json
import zipfile

root = Path(__file__).resolve().parents[1]
version = json.loads((root / 'server.json').read_text())['version']
endpoint = 'https://mcp.scenaro.io/mcp'
schema = 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'
mcp_schema = 'https://agent-plugins.org/schemas/1.0.0/mcp.schema.json'
description = 'Inspect and manage Scenaro voice experiences from a coding agent.'


def load(path):
    return json.loads((root / path).read_text())


def require(condition, message):
    if not condition:
        raise SystemExit(message)


portable = load('plugin.json')
require(portable['$schema'] == schema, 'plugin.json schema')
require(set(portable) <= {
    '$schema', 'name', 'version', 'description', 'author', 'homepage',
    'repository', 'license', 'keywords', 'extensions',
}, 'plugin.json has a field Mistral rejects')
require(portable['name'] == 'scenaro' and portable['version'] == version, 'plugin.json identity')
require(portable['description'] == description, 'plugin.json description')
vibe = portable['extensions']['ai.mistral.vibe']
require(vibe['schemaVersion'] == 1 and vibe['toolNamespace'] == 'scenaro', 'Mistral extension')
listing = portable['extensions']['com.openai']['interface']
require(len(listing['displayName']) <= 30 and len(listing['shortDescription']) <= 30, 'listing length')
require(len(listing['defaultPrompt']) == 3, 'starter prompts')
cases = portable['extensions']['com.openai']['review']['test_cases']
require(len(cases['positive']) == 5 and len(cases['negative']) == 3, 'review cases')

shared = load('mcp.json')
require(shared['$schema'] == mcp_schema and set(shared) == {'$schema', 'mcpServers'}, 'mcp.json schema')
server = shared['mcpServers']['scenaro']
require(server == {'type': 'streamable-http', 'url': endpoint}, 'mcp.json server')

claude_mcp = load('.mcp.json')['mcpServers']['scenaro']
require(claude_mcp == {'type': 'http', 'url': endpoint}, 'Claude MCP config')
gravity = load('mcp_config.json')
require(gravity == {'mcpServers': {'scenaro': {'serverUrl': endpoint}}}, 'Antigravity MCP config')
require('headers' not in claude_mcp and 'headers' not in server, 'Credentials must never be embedded')

for client, mcp in (('cursor', 'mcp.json'), ('claude', '.mcp.json'), ('codex', '.mcp.json')):
    manifest = load(f'.{client}-plugin/plugin.json')
    require(manifest['name'] == 'scenaro' and manifest['version'] == version, client)
    require(manifest['description'] == description, client + ' description')
    require(load(mcp)['mcpServers']['scenaro']['url'] == endpoint, client + ' endpoint')
    for key in ('logo', 'composerIcon', 'composerIconDark', 'logoDark'):
        if key in manifest:
            require((root / manifest[key]).is_file(), key)
        if key in listing:
            require((root / listing[key]).is_file(), 'listing ' + key)

codex = load('.codex-plugin/plugin.json')
require(codex['interface'] == listing, 'Codex and ChatGPT listings diverged')
require(codex['extensions']['com.openai']['review'] == portable['extensions']['com.openai']['review'], 'review cases diverged')

market = load('.claude-plugin/marketplace.json')
require(market['name'] == 'scenaro' and market['plugins'][0]['source'] == './', 'Claude marketplace')
require(market['plugins'][0]['version'] == version, 'Claude marketplace version')
codex_market = load('.agents/plugins/marketplace.json')
require(codex_market['plugins'][0]['source']['path'] == './', 'Codex marketplace')

skill = (root / 'skills/voice-experiences/SKILL.md').read_text()
require(skill.startswith('---\nname: voice-experiences\n'), 'skill name')

assets = sorted((root / 'assets').glob('*.svg'))
skills = sorted(path for path in (root / 'skills').rglob('*') if path.is_file())
out = root / '.artifacts'
out.mkdir(exist_ok=True)


def pack(name, files):
    with zipfile.ZipFile(out / f'scenaro-{name}-{version}.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, str(path.relative_to(root)))
    print(f'Validated and packaged {name} {version}')


for client, mcp in (('cursor', 'mcp.json'), ('claude', '.mcp.json'), ('codex', '.mcp.json')):
    files = [root / f'.{client}-plugin/plugin.json', root / mcp, root / 'README.md', *assets, *skills]
    if client == 'claude':
        files.append(root / '.claude-plugin/marketplace.json')
    if client == 'codex':
        files.extend([root / 'plugin.json', root / 'mcp.json', root / '.agents/plugins/marketplace.json'])
    pack(client, files)

pack('agent', [
    root / 'plugin.json', root / 'mcp.json', root / 'mcp_config.json',
    root / 'README.md', *assets, *skills,
])
