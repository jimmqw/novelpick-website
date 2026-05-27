# -*- coding: utf-8 -*-
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

f = Path(r'C:\Users\Administrator\github\novelpick-website\best-reincarnation-web-novels-2026.html')
c = f.read_text(encoding='utf-8', errors='ignore')

idx = c.find('<header')
if idx >= 0:
    chunk = c[idx:idx+500]
    # Replace problematic chars
    chunk = chunk.encode('ascii', errors='replace').decode('ascii')
    print('HEADER ELEM:')
    print(chunk)

print('\n--- Gradient patterns ---')
for m in re.finditer(r'gradient', c, re.I):
    start = max(0, m.start()-50)
    end = min(len(c), m.end()+50)
    snippet = c[start:end].encode('ascii', errors='replace').decode('ascii')
    print(f'...{snippet}...')
