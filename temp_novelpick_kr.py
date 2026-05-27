content = open(r'C:\Users\Administrator\github\novelpick-website\best-progression-fantasy-novels.html', 'r', encoding='utf-8', errors='replace').read()

import re

# Find the related-articles div
m = re.search(r'<div class=.related-articles.>', content)
if m:
    footer = content.find('<footer')
    ra_start = m.start()
    ra_end = content.find('</div>', m.start()) + 6
    print(f'related-articles: {ra_start} to {ra_end}')
    print(f'Footer at: {footer}')
    print(f'Gap between ra end and footer: {footer - ra_end} chars')
    # Find next tag after </div>
    next_tag = content.find('<', ra_end)
    print(f'Next tag after ra </div>: {next_tag}: {repr(content[next_tag:next_tag+30])}')
