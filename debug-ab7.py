import re
from pathlib import Path

def find_matching_close(html, start_pos, log):
    open_gt = html.find('>', start_pos)
    if open_gt < 0:
        log.write('no > found\n')
        return -1
    depth = 1
    pos = open_gt + 1
    log.write('start pos=%d after_gt=%d\n' % (pos, open_gt))
    steps = 0
    while pos < len(html) and depth > 0:
        steps += 1
        if steps > 200:
            log.write('break at 200 steps\n')
            break
        if html[pos:pos+5] == '<div ' or html[pos:pos+4] == '<div>':
            depth += 1
            log.write('  step%d open depth=%d at %d: %r\n' % (steps, depth, pos, html[pos:pos+20]))
            gt = html.find('>', pos)
            if gt < 0:
                return -1
            pos = gt + 1
        elif html[pos:pos+6] == '</div>':
            depth -= 1
            log.write('  step%d close depth=%d at %d: %r\n' % (steps, depth, pos, html[pos:pos+10]))
            if depth == 0:
                log.write('found end at %d\n' % pos)
                return pos
            pos += 6
        else:
            pos += 1
    log.write('loop end depth=%d steps=%d\n' % (depth, steps))
    return -1

log_lines = []
with open(r'C:\Users\Administrator\.openclaw\workspace\debug-log.txt', 'w') as log:

    p = r'C:\Users\Administrator\github\novelpick-website'
    fname = 'best-action-fantasy-web-novels-2026.html'
    with open(Path(p) / fname, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()

    ab_match = re.search(r'<div[^>]*\bclass="article-body"[^>]*>', c)
    log.write('Found at: %d -> %r\n' % (ab_match.start() if ab_match else -1, c[ab_match.start():ab_match.start()+40] if ab_match else ''))
    
    if ab_match:
        result = find_matching_close(c, ab_match.start(), log)
        log.write('Final result: %d\n' % result)
        if result > 0:
            log.write('Closing context: %r\n' % c[result:result+20])