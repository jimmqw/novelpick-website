with open(r'C:\Users\Administrator\github\novelpick-website\scifi.html', 'r', encoding='utf-8') as f:
    content = f.read()
body_start = content.find('<div class="article-body">')
body_end = content.find('<aside class="sidebar">')
body = content[body_start:body_end]
# Find the last </div> in body
last_close = body.rfind('</div>')
print('Last closing div at:', last_close)
print('Around last div:')
print(repr(body[last_close-100:last_close+100]))
