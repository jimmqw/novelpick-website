import re

fpath = r'C:\Users\Administrator\github\fateandmethod-site\chinese-zodiac-compatibility-guide.html'
content = open(fpath, 'r', encoding='utf-8', errors='replace').read()

# Check for meta description
idx = content.find('name="description"')
print('meta desc at:', idx)
if idx >= 0:
    print(repr(content[idx:idx+200]))

# Also check og tags
og = content.find('og:description')
print('og:description at:', og)
if og >= 0:
    print(repr(content[og:og+200]))

# Check if there is a meta description at all
meta_desc = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']{20,})["\']', content, re.IGNORECASE)
print('Meta desc match:', meta_desc)
if meta_desc:
    print('Content:', meta_desc.group(1))

# Check what meta tags are in the head
head = content[content.find('<head>'):content.find('</head>')]
meta_tags = re.findall(r'<meta[^>]*>', head)
print(f'\nMeta tags in head: {len(meta_tags)}')
for tag in meta_tags:
    print(' ', tag[:100])