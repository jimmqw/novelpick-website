with open(r'C:\Users\Administrator\github\novelpick-website\scifi.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find verdict-box and related
vb_idx = content.find('<div class="verdict-box">')
related_idx = content.find('<div class="related">')

print('verdict-box starts at:', vb_idx)
print('related div at:', related_idx)

# Find ALL </div> positions between verdict-box and related
import re
divs_between = [(m.start(), m.group()) for m in re.finditer(r'</div>', content[vb_idx:related_idx])]
print('</div> positions between verdict-box and related:', [pos for pos, _ in divs_between])
print('Count:', len(divs_between))

# Also - the first </div> after verdict-box open
first_close_after_vb = content.find('</div>', vb_idx)
print()
print('First </div> after verdict-box open at:', first_close_after_vb)
print('Content around it:')
print(repr(content[first_close_after_vb-50:first_close_after_vb+30]))