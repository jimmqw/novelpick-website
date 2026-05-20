with open(r'C:\Users\Administrator\github\novelpick-website\scifi.html', 'r', encoding='utf-8') as f:
    content = f.read()
body_start = content.find('<div class="article-body">')
body_end = content.find('<aside class="sidebar">')
body = content[body_start:body_end]
print('Body length:', len(body))
open_divs = body.count('<div ')
close_divs = body.count('</div>')
print('Open divs:', open_divs, 'Close divs:', close_divs)
print('Balance OK:', open_divs == close_divs)
