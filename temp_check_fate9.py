import re

fpath = r'C:\Users\Administrator\github\fateandmethod-site\chinese-zodiac-compatibility-guide.html'
content = open(fpath, 'r', encoding='utf-8', errors='replace').read()

# Find the meta description tag specifically
idx = content.find('name=description')
print('name=description at:', idx)
if idx >= 0:
    # Show the full tag
    tag_start = content.rfind('<meta', 0, idx)
    tag_end = content.find('>', idx) + 1
    tag = content[tag_start:tag_end]
    print('Full tag:', repr(tag))
    # Try to extract content
    m = re.search(r'content=["\']([^"\']+)["\']', tag)
    if m:
        print('Content value:', m.group(1))
        print('Content length:', len(m.group(1)))

# Check my regex
has_meta_desc = bool(re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'][^"\']{20,}', content, re.IGNORECASE))
print('\nMy regex says has_meta_desc:', has_meta_desc)

# Try a debug version
pattern = r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']{20,})["\']'
m2 = re.search(pattern, content, re.IGNORECASE)
print('Pattern match:', m2)
if m2:
    print('Groups:', m2.groups())