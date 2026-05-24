import re
from pathlib import Path

p = r'C:\Users\Administrator\github\fateandmethod-site'
fname = 'bazi-ten-gods-guide.html'
with open(Path(p) / fname, 'r', encoding='utf-8', errors='ignore') as f:
    c = f.read()

# Try to find article-body
patterns = [
    r'<div[^>]*\bclass="article-body"[^>]*>',
    r'<main[^>]*\bclass="article-body"[^>]*>',
    r'class="article-body"',
]
for pat in patterns:
    m = re.search(pat, c)
    print('Pattern %r: %s at %d' % (pat, 'FOUND' if m else 'NOT FOUND', m.start() if m else -1))
    if m:
        print('  Context:', repr(c[m.start():m.start()+60]))

# The bug: maybe the article-body div has nested divs that break the depth counting?
# Let's trace what happens in get_article_body_text
def trace_get_article_body_text(html):
    m = re.search(r'<div[^>]*\bclass="article-body"[^>]*>', html)
    if not m:
        return 'no match'
    tag = 'div'
    depth = 1
    start = m.start()
    open_end = html.find('>', start)
    if open_end < 0:
        return 'no open >'
    scan_from = open_end + 1
    count = 0
    for m2 in re.finditer(r'<' + tag + r'\b|</' + tag + r'>', html[scan_from:]):
        rel_pos = scan_from + m2.start()
        if html[rel_pos:rel_pos+2] == '</':
            depth -= 1
            if depth == 0:
                return 'found end at %d, content len=%d' % (rel_pos, rel_pos - start)
        else:
            depth += 1
        count += 1
        if count > 100:
            return 'too many iterations'
    return 'loop ended, depth=%d' % depth

result = trace_get_article_body_text(c)
print('trace result:', result)