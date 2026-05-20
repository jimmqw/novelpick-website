with open(r'C:\Users\Administrator\github\novelpick-website\scifi.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find article-body and what's inside
body_open = content.find('<div class="article-body">')
# Find where the article-body closes (the </div> right before <aside)
sidebar = content.find('<aside class="sidebar">')

# The article-body closes at the </div> that comes before <aside>
# Let's find all </div> positions and see which one is the closing one
import re
all_divs = [(m.start(), m.group()) for m in re.finditer(r'</div>', content)]
print('All </div> positions near sidebar:')
for pos, _ in all_divs:
    if pos > 10000 and pos < sidebar:
        print(pos)

# The article-body proper ends before related div
# Find the position of </div> that closes article-body
# That's the last </div> before the related div
related_pos = content.find('<div class="related">')
last_div_before_related = content.rfind('</div>', 0, related_pos)
print()
print('Related div at:', related_pos)
print('Last div before related at:', last_div_before_related)

# Now body ends at last_div_before_related
body_section = content[body_open:last_div_before_related + 6]  # +6 for </div>
open_divs = body_section.count('<div ')
close_divs = body_section.count('</div>')
print()
print('Body section length:', len(body_section))
print('Open divs:', open_divs, 'Close divs:', close_divs)
print('Balance:', open_divs == close_divs)