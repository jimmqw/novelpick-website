import re
from pathlib import Path

def find_matching_close(html, start_pos):
    open_gt = html.find('>', start_pos)
    if open_gt < 0:
        return -1
    depth = 1
    pos = open_gt + 1
    while pos < len(html) and depth > 0:
        if html[pos:pos+5] == '<div ' or html[pos:pos+4] == '<div>':
            depth += 1
            gt = html.find('>', pos)
            if gt < 0:
                return -1
            pos = gt + 1
        elif html[pos:pos+6] == '</div>':
            depth -= 1
            if depth == 0:
                return pos
            pos += 6
        else:
            pos += 1
    return -1

def get_article_body_text(html):
    ab_pattern = re.search(r'<div[^>]*\bclass="article-body"[^>]*>', html)
    if not ab_pattern:
        return ''
    start = ab_pattern.start()
    end = find_matching_close(html, start)
    if end < 0:
        return ''
    content = html[start:end+6]
    text = re.sub(r'<[^>]+>', '', content)
    return text.strip()

# Test on novelpick
p = r'C:\Users\Administrator\github\novelpick-website'
fname = 'best-action-fantasy-web-novels-2026.html'
with open(Path(p) / fname, 'r', encoding='utf-8', errors='ignore') as f:
    c = f.read()
text = get_article_body_text(c)
print('novelpick article-body text len:', len(text))
print('First 200 chars:', repr(text[:200]))

# Test on morai
p2 = r'C:\Users\Administrator\github\morai-website'
fname2 = 'ai-agent-tools-2026.html'
with open(Path(p2) / fname2, 'r', encoding='utf-8', errors='ignore') as f:
    c2 = f.read()
text2 = get_article_body_text(c2)
print('\nmorai article-body text len:', len(text2))
print('First 200 chars:', repr(text2[:200]))