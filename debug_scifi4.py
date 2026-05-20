with open(r'C:\Users\Administrator\github\novelpick-website\scifi.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find structure
body_open = content.find('<div class="article-body">')
related = content.find('<div class="related">')
sidebar = content.find('<aside class="sidebar">')
body_close_idx = content.find('</div>', body_open + 30)
print('article-body open:', body_open)
print('article-body closes at:', body_close_idx)
print('related div at:', related)
print('sidebar at:', sidebar)
print()
print('Is related inside article-body?', related < body_close_idx)
print('Is sidebar inside article-body?', sidebar < body_close_idx)
print()
# Show what's between article-body close and sidebar
print('Between article-body close and sidebar:')
print(repr(content[body_close_idx:sidebar]))