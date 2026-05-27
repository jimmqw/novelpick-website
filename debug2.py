import re
from pathlib import Path

print('=== FATANDMETHOD ===')
p = r'C:\Users\Administrator\github\fateandmethod-site'
for fname in ['bazi-ten-gods-guide.html', 'chinese-zodiac-compatibility-guide.html']:
    f = Path(p) / fname
    with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
        c = fh.read()
    ab_m = re.search(r'class="[^"]*article-body[^"]*"', c)
    print(fname, '-> ab:', bool(ab_m), ab_m.group() if ab_m else '')
    body_text = re.sub(r'<[^>]+>', ' ', c)
    body_text = re.sub(r'\s+', ' ', body_text).strip()
    print('  body text len:', len(body_text))

print('\n=== MORAI ===')
p2 = r'C:\Users\Administrator\github\morai-website'
for fname in ['best-ai-design-tools-2026.html', 'best-ai-research-assistants-2026.html', 'github-copilot-review-2026.html']:
    f = Path(p2) / fname
    with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
        c = fh.read()
    ab_m = re.search(r'class="[^"]*article-body[^"]*"', c)
    print(fname, '-> ab:', bool(ab_m))
    body_text = re.sub(r'<[^>]+>', ' ', c)
    body_text = re.sub(r'\s+', ' ', body_text).strip()
    print('  body text len:', len(body_text))
    has_baidu = bool(re.search(r'hm\.baidu', c))
    print('  baidu:', has_baidu)
    has_breadcrumb = bool(re.search(r'breadcrumb', c, re.I))
    print('  breadcrumb:', has_breadcrumb)
    has_sidebar = bool(re.search(r'<aside|sidebar', c, re.I))
    print('  sidebar:', has_sidebar)