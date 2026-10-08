import hashlib
import json
import os
from pathlib import Path
from datetime import datetime, timezone

repo = Path('/home/ubuntu/lchr_v2')
root = repo / 'HYPERGRAPH_RESEARCH/TOPOLOGY_V28'
reports = repo / 'result/innovation2/TOPOLOGY_V28'
files = {}
for p in sorted(reports.iterdir()):
    if p.is_file() and p.name != 'V28_FINAL_RESEARCH_REVIEW.md':
        content = p.read_bytes()
        record = {'bytes': len(content), 'sha256': hashlib.sha256(content).hexdigest()}
        if p.suffix == '.json':
            try:
                obj = json.loads(content)
                if isinstance(obj, dict):
                    record['state'] = obj.get('state')
                    record['test_flags'] = {k: obj[k] for k in ('test_opened', 'test_accessed') if k in obj}
            except Exception as e:
                record['parse_error'] = str(e)
        files[p.name] = record

def flag_values(obj):
    found = []
    if isinstance(obj, dict):
        for key, val in obj.items():
            if key in ('test_opened', 'test_accessed'):
                found.append([key, val])
            elif isinstance(val, (dict, list)):
                found.extend(flag_values(val))
    elif isinstance(obj, list):
        for val in obj:
            found.extend(flag_values(val))
    return found

cells = []
for kind in ('training', 'backbones'):
    for p in sorted((root / kind).rglob('result.json')):
        obj = json.loads(p.read_text())
        cells.append({'path': str(p.relative_to(root)), 'test_flags': flag_values(obj)})
logs = []
for p in sorted((root / 'logs').glob('*.log')):
    content = p.read_text(errors='replace')
    errors = [line.strip() for line in content.splitlines() if 'Error:' in line or 'No space left' in line]
    logs.append({'path': p.name, 'bytes': p.stat().st_size, 'errors': errors})
processes = []
for p in Path('/proc').iterdir():
    if not p.name.isdigit() or int(p.name) == os.getpid():
        continue
    try:
        comm = (p / 'comm').read_text().strip()
        cmd = (p / 'cmdline').read_bytes().replace(b'\0', b' ').decode(errors='replace')
        if comm.startswith('python') or comm in ('torchrun', 'accelerate'):
            processes.append({'pid': int(p.name), 'comm': comm, 'command': cmd})
    except (PermissionError, FileNotFoundError, ProcessLookupError):
        pass
stat = os.statvfs(repo)
out = {
    'checked_at_utc': datetime.now(timezone.utc).isoformat(),
    'workspace': 'DCDLP-main', 'workspace_info_tool': 'NOT_AVAILABLE',
    'server_checkout': str(repo), 'report_files': files,
    'raw_result_records': cells, 'logs': logs,
    'inner_training_result_count': sum(x['path'].startswith('training/inner/') for x in cells),
    'inner_backbone_result_count': sum(x['path'].startswith('backbones/inner/') for x in cells),
    'live_python_trainers': processes,
    'historical_run_status': json.loads((root / 'RUN_STATUS.json').read_text()),
    'disk_available_bytes': stat.f_bavail * stat.f_frsize,
    'latest_experiment_directory_exists': root.is_dir(),
    'raw_dataset_exists': (repo / 'data/raw').is_dir(),
}
print(json.dumps(out, ensure_ascii=False))
