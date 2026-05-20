with open(r'C:\Users\Administrator\github\novelpick-website\scifi.html', 'r', encoding='utf-8') as f:
    content = f.read()

vb_idx = content.find('<div class="verdict-box">')
related_idx = content.find('<div class="related">')

print('verdict-box at byte:', vb_idx)
print('related at byte:', related_idx)
print('Space between verdict-box start and related:', related_idx - vb_idx)

# Find ALL </div> positions between vb_idx and related_idx
import re
divs_between = [(vb_idx + m.start(), m.group()) for m in re.finditer(r'</div>', content[vb_idx:related_idx])]
print('</div> positions (absolute):', [pos for pos, _ in divs_between])
print('Count of </div> between verdict-box and related:', len(divs_between))

# The first </div> after vb_idx
first_close = vb_idx + content[vb_idx:].find('</div>')
print()
print('First </div> after verdict-box (absolute):', first_close)
print('Content:')
print(repr(content[first_close-30:first_close+50]))