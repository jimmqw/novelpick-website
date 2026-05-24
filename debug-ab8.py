import re
from pathlib import Path

p = r'C:\Users\Administrator\github\novelpick-website'
fname = 'best-action-fantasy-web-novels-2026.html'
with open(Path(p) / fname, 'r', encoding='utf-8', errors='ignore') as f:
    c = f.read()

# Try different regex patterns
patterns = [
    r'<div[^>]*\bclass="article-body"[^>]*>',
    r'<div[^>]*class="article-body"[^>]*>',
    r'class="article-body"',
    r'article-body',
]

for pat in patterns:
    m = re.search(pat, c)
    print('Pattern %r: %s' % (pat, 'FOUND at %d' % m.start() if m else 'NOT FOUND'))

# Check what's at position 10369
print('\nContext at 10369:', repr(c[10360:10400]))
# Check if maybe there's a self-closing issue or something
print('\nChar codes around pos 10369:')
for i in range(10365, 10380):
    print('  pos %d: char=%r ord=%d' % (i, c[i], ord(c[i])))