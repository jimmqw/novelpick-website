content = open(r'C:\Users\Administrator\github\fateandmethod-site\five-elements-complete-guide.html', 'r', encoding='utf-8', errors='replace').read()
footer = content.find('<footer')
segment = content[footer-3000:footer]

import re
sections = list(re.finditer(r'<section|</section>', segment))
print('Sections in segment:')
for s in sections:
    print(f'  {s.start()}: {repr(s.group())}')

divs = list(re.finditer(r'<div|</div>', segment))
print(f'\nTotal opens: {segment.count("<div")}, closes: {segment.count("</div>")}, net: {segment.count("<div") - segment.count("</div>")}')

print('\nLast divs:')
for d in divs[-15:]:
    print(f'  {d.start()}: {repr(d.group())}')

# Check if there's a related-section wrapper
has_related_section = 'related-section' in segment
print(f'\nHas related-section: {has_related_section}')
has_related_grid = 'related-grid' in segment
print(f'Has related-grid: {has_related_grid}')
