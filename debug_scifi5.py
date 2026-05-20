with open(r'C:\Users\Administrator\github\novelpick-website\scifi.html', 'r', encoding='utf-8') as f:
    content = f.read()

body_open = content.find('<div class="article-body">')
sidebar = content.find('<aside class="sidebar">')

body_section = content[body_open:sidebar]
open_divs = body_section.count('<div ')
close_divs = body_section.count('</div>')
print('Body section length:', len(body_section))
print('Open divs:', open_divs, 'Close divs:', close_divs)
print('Balance:', open_divs == close_divs)

# Show the last 400 chars
print()
print('Last 400 chars of body:')
print(body_section[-400:])