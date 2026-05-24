import re
from pathlib import Path

def find_matching_close(html, start_pos):
    """Find the closing </div> for the <div> tag starting at start_pos."""
    open_gt = html.find('>', start_pos)
    if open_gt < 0:
        print(f'find_matching_close: no > found after {start_pos}')
        return -1
    depth = 1
    pos = open_gt + 1
    print(f'Starting at pos {pos} after > at {open_gt}, char={repr(html[open_gt:open_gt+10])}')
    steps = 0
    while pos < len(html) and depth > 0:
        steps += 1
        if steps > 100:
            print('Breaking at 100 steps')
            break
        if html[pos:pos+5] == '<div ' or html[pos:pos+4] == '<div>':
            print(f'  Step {steps}: OPEN at {pos}, depth={depth+1}, tag={repr(html[pos:pos+20])}')
            depth += 1
            gt = html.find('>', pos)
            if gt < 0:
                print('  No > found for open div!')
                return -1
            pos = gt + 1
        elif html[pos:pos+6] == '</div>':
            print(f'  Step {steps}: CLOSE at {pos}, depth={depth-1}, char={repr(html[pos:pos+10])}')
            depth -= 1
            if depth == 0:
                print(f'  FOUND END at {pos}')
                return pos
            pos += 6
        else:
            pos += 1
    print(f'Loop ended, depth={depth}, steps={steps}')
    return -1

p = r'C:\Users\Administrator\github\novelpick-website'
fname = 'best-action-fantasy-web-novels-2026.html'
with open(Path(p) / fname, 'r', encoding='utf-8', errors='ignore') as f:
    c = f.read()

ab_match = re.search(r'<div[^>]*\bclass="article-body"[^>]*>', c)
if ab_match:
    print('Found at:', ab_match.start(), '->', repr(c[ab_match.start():ab_match.start()+40]))
    result = find_matching_close(c, ab_match.start())
    print('Final result:', result)
    if result > 0:
        print('Closing context:', repr(c[result:result+20]))