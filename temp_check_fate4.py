import re

fpath = r'C:\Users\Administrator\github\fateandmethod-site\chinese-zodiac-compatibility-guide.html'
content = open(fpath, 'r', encoding='utf-8', errors='replace').read()

# Find all occurrences of 'article-body'
idx = 0
count = 0
while True:
    idx = content.find('article-body', idx)
    if idx < 0:
        break
    snippet = content[max(0,idx-50):idx+80]
    print(f'{count}: pos={idx}: {repr(snippet)}')
    count += 1
    idx += 1
    if count > 5:
        break

# Check if there's an article-body div at all (class or id)
ab_class = content.find('class="article-body"')
ab_id = content.find('id="article-body"')
ab_main = content.find('<main')

print(f'\nclass="article-body": {ab_class}')
print(f'id="article-body": {ab_id}')
print(f'<main: {ab_main}')

# Show content around the article-body class occurrence
if ab_class >= 0:
    print(f'\nAround class="article-body":')
    print(repr(content[ab_class-100:ab_class+150]))