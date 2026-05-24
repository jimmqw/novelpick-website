content = open(r'C:\Users\Administrator\github\novelpick-website\best-progression-fantasy-novels.html', 'r', encoding='utf-8', errors='replace').read()

import re

# Find the related-articles div and extract everything
m = re.search(r'<div class="related-articles">(.*?)</div>\s*$', content, re.DOTALL)
if m:
    print(m.group(0))
else:
    # Try to find it differently
    ra_start = content.find('<div class="related-articles">')
    ra_end = content.find('</div>', ra_start) + 6
    print(content[ra_start:ra_end])
