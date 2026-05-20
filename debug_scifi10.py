with open(r'C:\Users\Administrator\github\novelpick-website\scifi.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find article-body open and related div
body_start = content.find('<div class="article-body">')
related_pos = content.find('<div class="related">')
body_close = content.rfind('</div>', 0, related_pos)

body_content = content[body_start:body_close+6]

# Find all closing tags and show what line they're on
lines = body_content.split('\n')
close_lines = []
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped == '</div>':
        close_lines.append(i+1)
        
print('Closing div lines in body:', close_lines)
print('Count:', len(close_lines))

open_lines = []
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped.startswith('<div '):
        open_lines.append(i+1)
        
print('Opening div lines in body:', open_lines)
print('Count:', len(open_lines))