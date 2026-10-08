import hashlib
from pathlib import Path
wheelhouse = Path(r'E:\Z\qths_v71_wheelhouse')
out = Path(r'E:\我的资料库\Documents\Downloads\DCDLP-main\HYPERGRAPH_RESEARCH\QTHS_V7_1\wheelhouse_sha256.txt')
lines = []
for path in sorted(wheelhouse.glob('*.whl')):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    lines.append(f'{digest}  {path.name}')
out.write_bytes(('\n'.join(lines) + '\n').encode('ascii'))
print(len(lines), out.stat().st_size)
