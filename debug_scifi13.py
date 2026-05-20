with open(r'C:\Users\Administrator\github\novelpick-website\scifi.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the verdict-box section
vb_start = content.find('<div class="verdict-box">')
vb_end = content.find('</div>', vb_start) + 6
vb_content = content[vb_start:vb_end]
print('verdict-box section length:', len(vb_content))
print('verdict-box div count - open:', vb_content.count('<div '), 'close:', vb_content.count('</div>'))

# Now show what comes after verdict-box and before related
print()
# Find article-body close
body_start = content.find('<div class="article-body">')
related_pos = content.find('<div class="related">')
body_close = content.rfind('</div>', 0, related_pos)

after_vb = content[vb_end:related_pos]
print('After verdict-box to related:')
print('Length:', len(after_vb))
# Count divs
print('Open divs:', after_vb.count('<div '))
print('Close divs:', after_vb.count('</div>'))
# Show first 200 chars
print('First 100 chars:', after_vb[:100])