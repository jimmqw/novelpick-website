with open(r'C:\Users\Administrator\github\novelpick-website\scifi.html', 'r', encoding='utf-8') as f:
    content = f.read()

body_start = content.find('<div class="article-body">')
related_pos = content.find('<div class="related">')
body_close = content.rfind('</div>', 0, related_pos)
body_content = content[body_start:body_close+6]
lines = body_content.split('\n')
for i in range(40, 55):
    if i < len(lines):
        print(f'{i+1}: {lines[i]}')