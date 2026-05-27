# Test get_article_body_text
import re
from pathlib import Path

def get_article_body_text(html):
    m = re.search(r'<main[^>]*\bclass="article-body"[^>]*>', html)
    tag = 'main'
    if not m:
        m = re.search(r'<div[^>]*\bclass="article-body"[^>]*>', html)
        tag = 'div'
    if not m:
        return ''

    depth = 1
    start = m.start()
    open_end = html.find('>', start)
    if open_end < 0:
        return ''
    scan_from = open_end + 1

    open_pat = re.compile(r'<' + tag + r'\b')
    close_pat = re.compile(r'</' + tag + r'>')

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

# Test all three sites
tests = [
    (r'C:\Users\Administrator\github\morai-website', 'ai-agent-tools-2026.html'),
    (r'C:\Users\Administrator\github\novelpick-website', 'best-action-fantasy-web-novels-2026.html'),
    (r'C:\Users\Administrator\github\fateandmethod-site', None),
]
for base, fname in tests:
    if fname is None:
        f = list(Path(base).rglob('*.html'))[0]
    else:
        f = Path(base) / fname
    with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
        c = fh.read()
    t = get_article_body_text(c)
    print('%s: text_len=%d first_100=%r' % (f.name, len(t), t[:100]))