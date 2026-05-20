with open(r'C:\Users\Administrator\github\novelpick-website\scifi.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Parse divs manually
body_start = content.find('<div class="article-body">')
related_pos = content.find('<div class="related">')
body_close = content.rfind('</div>', 0, related_pos)

body_content = content[body_start:body_close+6]

# Find all divs with context
import re
for m in re.finditer(r'<div |</div>', body_content):
    pos = m.start()
    line_num = body_content[:pos].count('\n') + 1
    print(f'Line {line_num}: {m.group()!r}')