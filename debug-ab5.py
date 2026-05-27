import re
from pathlib import Path

def find_matching_close(html, start_pos):
    open_gt = html.find('>', start_pos)
    if open_gt < 0:
        return -1
    depth = 1
    pos = open_gt + 1
    ops = []
    while pos < len(html) and depth > 0:
        if html[pos:pos+5] == '<div ' or html[pos:pos+4] == '<div>':
            depth += 1
            ops.append(('open', pos, depth, repr(html[pos:pos+30])))
            gt = html.find('>', pos)
            if gt < 0:
                return -1
            pos = gt + 1
        elif html[pos:pos+6] == '</div>':
            depth -= 1
            ops.append(('close', pos, depth, repr(html[pos:pos+20])))
            if depth == 0:
                return pos
            pos += 6
        else:
            pos += 1
    return -1

p = r'C:\Users\Administrator\github\novelpick-website'
fname = 'best-action-fantasy-web-novels-2026.html'
with open(Path(p) / fname, 'r', encoding='utf-8', errors='ignore') as f:
    c = f.read()

ab_match = re.search(r'<div[^>]*\bclass="article-body"[^>]*>', c)
print('Found article-body at:', ab_match.start() if ab_match else None)
if ab_match:
    print('Context:', repr(c[ab_match.start():ab_match.start()+50]))
    result = find_matching_close(c, ab_match.start())
    print('END result:', result)
    for op in ops:
        print(' ', op)