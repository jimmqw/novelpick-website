# Debug find_matching_close for main tag
import re
from pathlib import Path

def find_matching_close(html, start_pos, tag_name='div'):
    open_tag = '<main' if tag_name == 'main' else '<div'
    open_pos = start_pos
    if html[open_pos:open_pos+len(open_tag)] != open_tag:
        print('[DEBUG] open_tag mismatch: %r != %r' % (html[open_pos:open_pos+len(open_tag)], open_tag))
        return -1
    open_gt = html.find('>', open_pos)
    if open_gt < 0:
        print('[DEBUG] no > found')
        return -1
    print('[DEBUG] open tag ends at %d, char=%r' % (open_gt, html[open_gt:open_gt+5]))
    depth = 1
    pos = open_gt + 1
    open_pattern = '<%s ' % tag_name if tag_name != 'main' else '<main'
    open_pattern2 = '<%s>' % tag_name
    close_pattern = '</%s>' % tag_name
    print('[DEBUG] open_pattern=%r close_pattern=%r' % (open_pattern, close_pattern))
    print('[DEBUG] starting at pos %d, html[pos:pos+10]=%r' % (pos, html[pos:pos+10]))
    steps = 0
    while pos < len(html) and depth > 0:
        steps += 1
        if steps > 5:
            print('[DEBUG] stopping after 5 steps')
            break
        if html[pos:pos+len(open_pattern)] == open_pattern:
            print('  step%d: OPEN at %d, depth->%d, tag=%r' % (steps, pos, depth+1, html[pos:pos+20]))
            depth += 1
            gt = html.find('>', pos)
            pos = gt + 1
        elif html[pos:pos+len(open_pattern2)] == open_pattern2:
            print('  step%d: OPEN2 at %d, depth->%d, tag=%r' % (steps, pos, depth+1, html[pos:pos+15]))
            depth += 1
            pos = html.find('>', pos) + 1
        elif html[pos:pos+len(close_pattern)] == close_pattern:
            print('  step%d: CLOSE at %d, depth->%d, tag=%r' % (steps, pos, depth-1, html[pos:pos+len(close_pattern)+3]))
            depth -= 1
            if depth == 0:
                return pos
            pos += len(close_pattern)
        else:
            pos += 1
    print('[DEBUG] loop end, depth=%d steps=%d' % (depth, steps))
    return -1

p2 = r'C:\Users\Administrator\github\novelpick-website'
fname = 'best-action-fantasy-web-novels-2026.html'
with open(Path(p2) / fname, 'r', encoding='utf-8', errors='ignore') as f:
    c = f.read()

m = re.search(r'<main[^>]*\bclass="article-body"[^>]*>', c)
print('Found main tag at:', m.start() if m else None)
if m:
    print('Tag:', repr(c[m.start():m.start()+40]))
    result = find_matching_close(c, m.start(), 'main')
    print('Result:', result)
    if result > 0:
        print('Closing context:', repr(c[result:result+20]))