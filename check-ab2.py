import re
from pathlib import Path

p = r'C:\Users\Administrator\github\novelpick-website'
f = list(Path(p).rglob('*.html'))[0]
with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
    c = fh.read()

idx = c.find('class="article-body"')
print('pos:', idx)
if idx >= 0:
    segment = c[idx:idx+1000]
    print('segment around article-body:')
    print(repr(segment[:500]))
    print('---')
    # find the closing tag
    close_idx = segment.find('</div>')
    print('first </div> after article-body:', close_idx)
    if close_idx > 0:
        print(repr(segment[close_idx:close_idx+50]))