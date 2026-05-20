with open(r'C:\Users\Administrator\github\novelpick-website\scifi.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find article-body open tag
body_open_idx = content.find('<div class="article-body">')
print('article-body open at byte:', body_open_idx)

# Show the content at and around body_open_idx
print('Content at body_open_idx:')
print(repr(content[body_open_idx:body_open_idx+200]))

# Also find where article-body closes (the </div> right before related div)
related_pos = content.find('<div class="related">')
body_close_idx = content.rfind('</div>', 0, related_pos)
print()
print('article-body close at byte:', body_close_idx)
print('Content at body_close_idx:')
print(repr(content[body_close_idx-20:body_close_idx+30]))