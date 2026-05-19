import os
import re

webroot = r"C:\Users\Administrator\github\novelpick-website"
results = []

for fname in os.listdir(webroot):
    if not fname.endswith('.html'):
        continue
    fpath = os.path.join(webroot, fname)
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    
    # Find article-body content
    m = re.search(r'<div class="article-body"(?:[^>]*)>(.*?)</div>\s*<(?:aside|main|div class="related")', html, re.DOTALL)
    if m:
        body = m.group(1)
        text = re.sub(r'<[^>]+>', ' ', body)
        text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        text = ' '.join(text.split())
        results.append((fname, len(text), text[:120]))

results.sort(key=lambda x: x[1])
for r in results:
    print(f"{r[0]}|{r[1]} chars: {r[2][:80]}...")