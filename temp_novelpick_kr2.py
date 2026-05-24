content = open(r'C:\Users\Administrator\github\novelpick-website\best-progression-fantasy-novels.html', 'r', encoding='utf-8', errors='replace').read()

import re

# Find the related-articles div
m = re.search(r'<div class="related-articles">', content)
if m:
    ra_start = m.start()
    # Find the closing </div>
    ra_end = content.find('</div>', m.start()) + 6
    print(f'related-articles: {ra_start} to {ra_end}')
    # Extract just the inner content
    inner_start = content.find('>', m.start()) + 1
    inner_end = ra_end - 6
    inner = content[inner_start:inner_end].strip()
    print('Inner content:')
    print(inner)
