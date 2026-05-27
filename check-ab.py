# check what class names look like for article-body
import re
from pathlib import Path

p = r'C:\Users\Administrator\github\morai-website'
for f in list(Path(p).rglob('*.html'))[:5]:
    with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
        c = fh.read()
    matches = re.findall(r'class="[^"]*article-body[^"]*"', c)
    if matches:
        print(f.name, '->', matches[:3])
    else:
        # try finding article body differently
        id_match = re.findall(r'id="article-body"', c)
        print(f.name, 'id matches:', id_match, '-> body divs:', len(re.findall(r'<div[^>]*>', c[:500])))