content = open(r'C:\Users\Administrator\github\novelpick-website\best-cultivation-novels-2026.html', 'r', encoding='utf-8', errors='replace').read()

ab = content.find('class="article-body"')
ab_open = content.find('>', ab)
print(f'article-body opens at: {ab_open}')
print(f'Context: {repr(content[ab_open:ab_open+50])}')

# Find the article-body closing div
ab_close = content.find('</div>', ab_open + 1)
print(f'First </div> after ab_open: {ab_close}')

# What div class is it?
prev_div = content.rfind('<div', ab_open, ab_close)
print(f'Opening div: {repr(content[prev_div:prev_div+50])}')

# Now find all divs between article-body open and footer
import re
footer = content.find('<footer')
segment = content[ab_open:footer]
opens = len(re.findall(r'<div', segment))
closes = len(re.findall(r'</div>', segment))
print(f'\nIn article-body to footer: {opens} opens, {closes} closes, net={opens-closes}')
