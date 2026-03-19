import json
from pathlib import Path

path = Path(r'C:\Projects\pharmacy-accessibility-ch\notebooks\03_isochrones_ors.ipynb')
with open(path, encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    src = cell['source'] if isinstance(cell['source'], str) else ''.join(cell['source'])
    ctype = cell['cell_type']
    preview = src[:100].replace('\n', ' ')
    print(f'Zelle {i} [{ctype}]: {preview}')
