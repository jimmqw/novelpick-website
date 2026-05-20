with open(r'C:\Users\Administrator\github\novelpick-website\scifi.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all major structural elements
article_body_open = content.find('<div class="article-body">')
article_body_close = content.rfind('</div>')
related_open = content.find('<div class="related">')
sidebar_open = content.find('<aside class="sidebar">')

print('article-body open at:', article_body_open)
print('article-body closes at:', article_body_close)
print('related div at:', related_open)
print('sidebar at:', sidebar_open)

print()
print('Content between article-body close and related open:')
print(repr(content[article_body_close-50:related_open+50]))

print()
print('Content around end of body section:')
# Find the last div before sidebar
last_div_before_aside = content.rfind('</div>', 0, sidebar_open)
print(repr(content[last_div_before_aside-100:last_div_before_aside+50]))