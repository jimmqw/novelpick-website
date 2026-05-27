import re

content = open(r'C:\Users\Administrator\github\morai-website\best-ai-coding-assistants-2026.html', 'r', encoding='utf-8', errors='replace').read()

# Find article-body
ab_class = content.find('class="article-body"')
ab_open = content.find('>', ab_class)

# Find </main>
main_close = content.find('</main>')

# Count divs in each segment
header_seg = content[:ab_class]  # before article-body CSS
article_seg = content[ab_class:main_close]  # article-body CSS + <main>...</main>
sidebar_seg = content[main_close:]  # after </main>

for name, seg in [('header', header_seg), ('article+main', article_seg), ('sidebar', sidebar_seg)]:
    opens = seg.count('<div ')
    closes = seg.count('</div>')
    print(f'{name}: opens={opens}, closes={closes}, net={opens-closes}')

# Now look at what </main> is followed by
print(f'\nAfter </main>: {repr(content[main_close:main_close+100])}')

# Check for the extra </div> in sidebar - find where it is
footer = content.find('<footer')
sidebar_only = content[main_close:footer]
print(f'\nSidebar: opens={sidebar_only.count("<div ")}, closes={sidebar_only.count("</div>")}, net={sidebar_only.count("<div ") - sidebar_only.count("</div>")}')

# Find the last </div> before </footer>
last_div = content.rfind('</div>', 0, footer)
print(f'\nLast </div> before footer: {last_div}')
print(f'Context: {repr(content[last_div-30:last_div+50])}')
print(f'After last div: {repr(content[last_div+6:last_div+50])}')
