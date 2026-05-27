import re

content = open(r'C:\Users\Administrator\github\fateandmethod-site\chinese-zodiac-personality-traits.html', 'r', encoding='utf-8', errors='replace').read()

print('div opens:', content.count('<div '))
print('div closes:', content.count('</div>'))
print('diff:', content.count('<div ') - content.count('</div>'))

# Check if there's a main wrapper div
# Look for unclosed divs - list all opening divs
opens = [(m.start(), content[m.start():m.start()+50]) for m in re.finditer(r'<div[^/>][^>]*>', content)]
print(f'opens: {len(opens)}, closes: {content.count("</div>")}')

# Find article-body
ab = content.find('article-body')
print(f'article-body at: {ab}')
if ab > 0:
    print(repr(content[ab-50:ab+100]))

# Look at the last 500 chars before footer
footer = content.find('<footer')
if footer > 0:
    print('Last 500 before footer:')
    print(repr(content[footer-500:footer]))