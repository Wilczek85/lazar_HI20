"""Build dashboard using actual entity registry IDs (Python standard library only)."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def bind(value, mapping):
    if isinstance(value, dict):
        return {key: bind(item, mapping) for key, item in value.items()}
    if isinstance(value, list):
        return [bind(item, mapping) for item in value]
    return mapping.get(value, value) if isinstance(value, str) else value

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('registry', help='Local copy of /config/.storage/core.entity_registry')
    parser.add_argument('--entry-id', help='Choose one config_entry_id if several integrations exist')
    parser.add_argument('--output', default='lazar_home.yaml')
    args = parser.parse_args()
    registry = json.loads(Path(args.registry).read_text())['data']['entities']
    expected = json.loads((ROOT / 'entity_map.json').read_text())
    mapping = {}
    errors = []
    for default_id, unique_id in expected.items():
        domain = default_id.split('.')[0]
        matches = [e for e in registry if e.get('platform') == 'lazar_hi20'
                   and e.get('unique_id') == unique_id
                   and e['entity_id'].split('.')[0] == domain
                   and (not args.entry_id or e.get('config_entry_id') == args.entry_id)]
        if len(matches) != 1 or matches[0].get('disabled_by'):
            errors.append(f'{unique_id}: missing, disabled or ambiguous')
        else:
            mapping[default_id] = matches[0]['entity_id']
    if errors:
        raise SystemExit('\n'.join(errors))
    dashboard = json.loads((ROOT / 'dashboard.json').read_text())
    # JSON is valid YAML, accepted by the HA raw dashboard editor.
    Path(args.output).write_text(json.dumps(bind(dashboard, mapping), ensure_ascii=False, indent=2)+'\n')
    print(f'Created: {args.output}')

if __name__ == '__main__':
    main()
