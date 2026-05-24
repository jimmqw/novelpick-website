content = open(r'C:\Users\Administrator\github\fateandmethod-site\five-elements-complete-guide.html', 'r', encoding='utf-8', errors='replace').read()

import re
sections = re.findall(r'<section[^>]*class="([^"]+)"', content)
print('Section classes:', sections)

# Find all div classes in body
body_start = content.find('<body')
footer = content.find('<footer')
body_seg = content[body_start:footer]
div_classes = re.findall(r'<div[^>]*class="([^"]+)"', body_seg)
print(f'\nDiv classes in body ({len(div_classes)} total):')
for d in div_classes:
    print(' ', d)

# Check for related-articles or keep-reading
has_kr = bool(re.search(r'class="[^"]*(?:keep-reading|related-articles|related-posts)[^"]*"', content, re.IGNORECASE))
print(f'\nHas keep-reading/related-articles class: {has_kr}')

# Check for related-section
has_rs = 'related-section' in content
print(f'Has related-section: {has_rs}')
