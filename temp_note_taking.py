content = open(r'C:\Users\Administrator\github\morai-website\best-ai-note-taking-tools-2026.html', 'rb').read()

# Find the main layout div
layout = content.find(b'<div class="layout">')
print('layout at:', layout, repr(content[layout:layout+30]))

# Find where article-body div content ends
ab_class = content.find(b'<div class="article-body">')
ab_open = content.find(b'>', ab_class)
print('article-body div opens at:', ab_open)

# Count depth to find closing
import re
depth = 1
pos = ab_open + 1
for m in re.finditer(b'<div|</div>', content[pos:]):
    if m.group() == b'<div':
        depth += 1
    else:
        depth -= 1
    if depth == 0:
        close_pos = pos + m.start()
        print('article-body closes at:', close_pos)
        print('Context:', content[close_pos-30:close_pos+50])
        break

# What's after the article-body close?
print('\nAfter article-body:')
print(repr(content[close_pos:close_pos+200]))
