import re

fname = r'C:\Users\Administrator\github\fateandmethod-site\bazi.html'
content = open(fname, 'r', encoding='utf-8', errors='replace').read()

print('File length:', len(content))

# Find all divs with article-body in class
idx = 0
count = 0
while True:
    idx = content.find('article-body', idx)
    if idx < 0:
        break
    # Show context around each occurrence
    snippet = content[max(0, idx-30):idx+60]
    print(f'pos {idx}: ...{repr(snippet)}...')
    count += 1
    idx += 1
    if count > 5:
        break

print('\n--- Looking for div with article-body class ---')
# Find div with class="article-body"
pattern = r'<div[^>]*class=["\']([^"\']*article-body[^"\']*)["\'][^>]*>'
matches = list(re.finditer(pattern, content))
print('found', len(matches))
for m in matches:
    print('pos', m.start(), ':', content[m.start():m.start()+80])

# Check what's around the article-body div opening
ab_idx = content.find('class="article-body"')
print('\nclass="article-body" at:', ab_idx)
if ab_idx >= 0:
    # Find the opening >
    open_pos = content.find('>', ab_idx)
    print('opening > at:', open_pos)
    print('snippet:', repr(content[ab_idx-20:open_pos+1]))
    print('after:', repr(content[open_pos+1:open_pos+100]))