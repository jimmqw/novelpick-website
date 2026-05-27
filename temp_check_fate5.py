import re

fpath = r'C:\Users\Administrator\github\fateandmethod-site\chinese-zodiac-compatibility-guide.html'
content = open(fpath, 'r', encoding='utf-8', errors='replace').read()

# The article-body class is only in CSS. Find the main tag
main_pos = content.find('<main')
footer_pos = content.find('<footer')
print(f'<main at: {main_pos}')
print(f'<footer at: {footer_pos}')

# Show the main tag
main_end = content.find('>', main_pos)
print(f'<main> closing > at: {main_end}')
print(f'Main tag: {repr(content[main_pos:main_end+1])}')

# Extract content from main to footer
segment = content[main_pos:footer_pos]
text = re.sub(r'<[^>]+>', '', segment).strip()
print(f'Text length: {len(text)}')
print(f'First 200: {text[:200]}')
print(f'Last 200: {text[-200:]}')

# Count divs in segment
div_opens = len(re.findall(r'<div[^/>][^>]*>', segment))
div_closes = segment.count('</div>')
print(f'Div opens in segment: {div_opens}, closes: {div_closes}, diff: {div_opens - div_closes}')