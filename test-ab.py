# Test get_article_body_text for both sites
import re, sys
sys.path.insert(0, r'C:\Users\Administrator\.openclaw\workspace')
# Inline the function
def find_matching_close(html, start_pos, tag_name='div'):
    open_tag = '<main' if tag_name == 'main' else '<div'
    open_pos = start_pos
    if html[open_pos:open_pos+len(open_tag)] != open_tag:
        return -1
    open_gt = html.find('>', open_pos)
    if open_gt < 0:
        return -1
    depth = 1
    pos = open_gt + 1
    open_pattern = '<%s ' % tag_name if tag_name != 'main' else '<main'
    open_pattern2 = '<%s>' % tag_name
    while pos < len(html) and depth > 0:
        if html[pos:pos+len(open_pattern)] == open_pattern or html[pos:pos+len(open_pattern2)] == open_pattern2:
            depth += 1
            gt = html.find('>', pos)
            if gt < 0:
                return -1
            pos = gt + 1
        elif html[pos:pos+6] == '</%s>' % tag_name:
            depth -= 1
            if depth == 0:
                return pos
            pos += len('</%s>' % tag_name)
        else:
            pos += 1
    return -1

def get_article_body_text(html):
    m = re.search(r'<main[^>]*\bclass="article-body"[^>]*>', html)
    tag = 'main'
    if not m:
        m = re.search(r'<div[^>]*\bclass="article-body"[^>]*>', html)
        tag = 'div'
    if not m:
        return ''
    end = find_matching_close(html, m.start(), tag)
    if end < 0:
        return ''
    content = html[m.start():end+len('</%s>' % tag)]
    text = re.sub(r'<[^>]+>', '', content)
    return text.strip()

from pathlib import Path

# Test morai
p1 = r'C:\Users\Administrator\github\morai-website'
f1 = Path(p1) / 'ai-agent-tools-2026.html'
with open(f1, 'r', encoding='utf-8', errors='ignore') as fh:
    c1 = fh.read()
t1 = get_article_body_text(c1)
print('morai text len:', len(t1))

# Test novelpick
p2 = r'C:\Users\Administrator\github\novelpick-website'
f2 = Path(p2) / 'best-action-fantasy-web-novels-2026.html'
with open(f2, 'r', encoding='utf-8', errors='ignore') as fh:
    c2 = fh.read()
t2 = get_article_body_text(c2)
print('novelpick text len:', len(t2))

# Test fateandmethod
p3 = r'C:\Users\Administrator\github\fateandmethod-site'
f3 = list(Path(p3).rglob('*.html'))[0]
with open(f3, 'r', encoding='utf-8', errors='ignore') as fh:
    c3 = fh.read()
t3 = get_article_body_text(c3)
print('fateandmethod text len:', len(t3), 'first 100:', repr(t3[:100]))