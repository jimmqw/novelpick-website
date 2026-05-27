import re
from pathlib import Path

p = r'C:\Users\Administrator\github\fateandmethod-site'
f = list(Path(p).rglob('*.html'))[0]
with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
    c = fh.read()

print('File:', f.name)
# Count total text
body_m = re.search(r'<body[^>]*>(.*)</body>', c, re.DOTALL)
if body_m:
    text = re.sub(r'<[^>]+>', ' ', body_m.group(1))
    text = re.sub(r'\s+', ' ', text).strip()
    print('Body text len:', len(text))
    print('First 200:', repr(text[:200]))
else:
    print('No body found')

# Check article-body-like patterns
print('article-body patterns:', re.findall(r'class="[^"]*article[^"]*"', c)[:5])
print('main patterns:', re.findall(r'<main[^>]*>', c)[:3])
print('article patterns:', re.findall(r'<article[^>]*>', c)[:3])