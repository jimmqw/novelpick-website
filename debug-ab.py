import re
from pathlib import Path

p = r'C:\Users\Administrator\github\novelpick-website'
fname = 'best-action-fantasy-web-novels-2026.html'
f = Path(p) / fname
with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
    c = fh.read()

body_start = c.find('class="article-body"')
print('body_start:', body_start)
# Count depth from article-body start tag to find matching close
inner = c[body_start:]
depth = 0
article_body_end = -1
i = 0
while i < len(inner):
    if inner[i:i+5] == '<div ' or inner[i:i+4] == '<div>':
        depth += 1
        # find the end of this tag
        gt = inner.find('>', i)
        i = gt + 1
    elif inner[i:i+6] == '</div>':
        depth -= 1
        if depth == 0:
            article_body_end = body_start + i
            break
        i += 6
    else:
        i += 1

print('article-body end pos:', article_body_end)
if article_body_end > 0:
    content = c[body_start:article_body_end + 6]
    # remove tags
    text = re.sub(r'<[^>]+>', '', content)
    print('text len:', len(text.strip()))
    print('first 200 chars:', repr(text.strip()[:200]))
    # Check what's around the container div
    container_start = content.find('class="container"')
    if container_start >= 0:
        print('container found at offset:', container_start, 'in content')