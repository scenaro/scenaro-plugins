"""Validate and package public plugin metadata. No server implementation or credentials."""
from pathlib import Path
import json
import zipfile

root = Path(__file__).resolve().parents[1]
version = json.loads((root / 'server.json').read_text())['version']
out = root / '.artifacts'
out.mkdir(exist_ok=True)
for client in ('codex', 'claude', 'cursor'):
    meta = f'.{client}-plugin/plugin.json'
    manifest = json.loads((root / meta).read_text())
    assert manifest['name'] == 'scenaro' and manifest['version'] == version
    mcp = 'mcp.json' if client == 'cursor' else '.mcp.json'
    config = json.loads((root / mcp).read_text())['mcpServers']['scenaro']
    assert config['url'] == 'https://mcp.scenaro.io/mcp'
    assert 'headers' not in config, 'Credentials must never be embedded in a plugin'
    for key in ('logo',):
        if key in manifest:
            assert (root / manifest[key]).is_file()
    files = [root / meta, root / mcp, root / 'README.md', *sorted((root / 'assets').glob('*.svg'))]
    with zipfile.ZipFile(out / f'scenaro-{client}-{version}.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, str(path.relative_to(root)))
    print(f'Validated and packaged {client} {version}')
