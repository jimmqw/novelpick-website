import re

content = open(r'C:\Users\Administrator\github\morai-website\best-ai-coding-assistants-2026.html', 'r', encoding='utf-8', errors='replace').read()
footer = content.find('<footer')
rec = content.find('class="recommended"')
end_pos = min(footer if footer > 0 else 999999, rec if rec > 0 else 999999)
print(f'footer at {footer}, rec at {rec}, end_pos={end_pos}')

ab = content.find('class="article-body"')
print(f'article-body at {ab}')

# Find the div that should close article-body
# Look for </div> in the last 400 chars before footer
last_400 = content[footer-400:footer]
print('Last 400 chars before footer:')
print(last_400)

# Find all </div> in last 400
divs = [(m.start(), content[footer-400+m.start():footer-400+m.start()+20]) for m in re.finditer(r'</div>', last_400)]
print('Div closes in last 400:', divs)

# Show what the div structure looks like near the closing
# Find the </aside> that might be closing the main layout
aside_close = content.rfind('</aside>', 0, footer)
print(f'</aside> at {aside_close}')
print('After </aside>:', repr(content[aside_close+8:footer]))