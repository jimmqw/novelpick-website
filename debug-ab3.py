import re
from pathlib import Path

p = r'C:\Users\Administrator\github\novelpick-website'
fname = 'best-action-fantasy-web-novels-2026.html'
f = Path(p) / fname
with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
    c = fh.read()

# Find article-body class
body_start = c.find('class="article-body"')
print('First occurrence pos:', body_start)
print('Context:', repr(c[body_start:body_start+50]))

# Try using regex to find the actual article-body div with depth counting
# Use a simpler approach - find all <div and </div> positions from the article-body start
matches = list(re.finditer(r'<div\b|</div>', c[body_start:body_start+50000]))
print('Total div tags found from article-body start:', len(matches))
depth = 0
for m in matches:
    tag = m.group()
    pos_in_doc = body_start + m.start()
    if tag == '<div' or tag.startswith('<div '):
        depth += 1
        if depth == 1:
            print(f'  div open at +{m.start()} -> depth={depth} (article-body itself)')
    else:
        depth -= 1
        if depth == 0:
            print(f'  div close at +{m.start()} -> depth={depth} (END of article-body)')
            print('Context:', repr(c[pos_in_doc:pos_in_doc+30]))
            break