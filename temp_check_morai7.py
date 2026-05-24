import re

content = open(r'C:\Users\Administrator\github\morai-website\chatgpt-vs-claude.html', 'r', encoding='utf-8', errors='replace').read()

ab = content.find('class="article-body"')
ab_open = content.find('>', ab)

depth = 1
matches = list(re.finditer(r'<div|</div>', content[ab_open+1:]))
for m in matches:
    if m.group() == '<div':
        depth += 1
    else:
        depth -= 1
    if depth == 0:
        close_pos = ab_open + 1 + m.start()
        print(f'article-body closes at: {close_pos}')
        print(repr(content[close_pos-50:close_pos+50]))
        print('After:', repr(content[close_pos+6:close_pos+200]))
        break