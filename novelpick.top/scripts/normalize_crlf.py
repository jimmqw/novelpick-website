#!/usr/bin/env python3
"""Force-normalize line endings in all HTML files."""
import glob, os

def _rf(p):
    with open(p, 'rb') as f:
        raw = f.read()
    if raw.startswith(b'\xff\xfe') or raw.startswith(b'\xfe\xff'):
        return raw.decode('utf-16').encode('utf-8').decode('utf-8')
    for enc in ['utf-8-sig', 'utf-8', 'cp1252']:
        try: return raw.decode(enc)
        except: continue
    return raw.decode('utf-8', errors='replace')

def _norm(c):
    return c.replace('\r\n', '\n').replace('\r', '\n')

count = 0
for site_dir in [
    r'C:\Users\Administrator\.openclaw\workspace\morai-website',
    r'C:\Users\Administrator\.openclaw\workspace\novelpick-website',
]:
    for fpath in glob.glob(site_dir + r'\*.html'):
        content = _rf(fpath)
        if '\r' in content:
            norm = _norm(content)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(norm)
            count += 1
            print(f'Normalized: {os.path.basename(fpath)}')

print(f'Total normalized: {count}')
