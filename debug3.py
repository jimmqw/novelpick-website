import re
from pathlib import Path

def get_article_body_text(html):
    m = re.search(r'<main[^>]*\bclass="article-body"[^>]*>', html)
    tag = 'main'
    if not m:
        m = re.search(r'<div[^>]*\bclass="article-body"[^>]*>', html)
        tag = 'div'
    if not m:
        m = re.search(r'<div[^>]*\bclass="article-content article-body"[^>]*>', html)
        tag = 'div'
    if not m:
        return ''
    depth = 1
    start = m.start()
    open_end = html.find('>', start)
    if open_end < 0:
        return ''
    scan_from = open_end + 1
    for m2 in re.finditer(r'<' + tag + r'\b|</' + tag + r'>', html[scan_from:]):
        rel_pos = scan_from + m2.start()
        if html[rel_pos:rel_pos+2] == '</':
            depth -= 1
            if depth == 0:
                content = html[start:rel_pos + len('</%s>' % tag)]
                text = re.sub(r'<[^>]+>', '', content)
                return text.strip()
        else:
            depth += 1
    return ''

# Test fateandmethod
p = r'C:\Users\Administrator\github\fateandmethod-site'
fname = 'bazi-ten-gods-guide.html'
with open(Path(p) / fname, 'r', encoding='utf-8', errors='ignore') as f:
    c = f.read()

ab_m = re.search(r'<div[^>]*\bclass="article-body"[^>]*>', c)
print('ab match:', ab_m)
if ab_m:
    print('context:', repr(c[ab_m.start():ab_m.start()+50]))
    t = get_article_body_text(c)
    print('text len:', len(t))

# Now check the actual article-content article-body issue from earlier
fname2 = 'chinese-zodiac-compatibility-guide.html'
with open(Path(p) / fname2, 'r', encoding='utf-8', errors='ignore') as f:
    c2 = f.read()
ab_m2 = re.search(r'class="article-content article-body"', c2)
print('\n' + fname2, 'article-content article-body:', bool(ab_m2))
if ab_m2:
    print('context:', repr(c2[ab_m2.start()-20:ab_m2.start()+60]))