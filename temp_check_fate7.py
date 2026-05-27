import re

fpath = r'C:\Users\Administrator\github\fateandmethod-site\chinese-zodiac-personality-traits.html'
content = open(fpath, 'r', encoding='utf-8', errors='replace').read()

# Find article-body class or id or the article section
for kw in ['article-body', 'article-layout', '<article', '<main', 'class="content"']:
    idx = content.find(kw)
    if idx >= 0:
        print(f'{kw}: at {idx}')
        print(repr(content[idx:idx+80]))
        print()

# Find all div classes
divs = re.findall(r'<div[^>]*class="([^"]*)"[^>]*>', content)
print(f'Total divs with class: {len(divs)}')
for d in divs[:20]:
    print('  div class:', d)

# Show lines around a specific position to understand structure
# Find the article content area
h2_count = len(re.findall(r'<h2', content))
print(f'H2 count: {h2_count}')

# Show the last 100 lines before footer
footer = content.find('<footer')
lines = content[footer-2000:footer].split('\n')
print('\nLast 30 lines before footer:')
for i, line in enumerate(lines[-30:]):
    print(f'  {i}: {repr(line.strip())}')