with open(r'C:\Users\Administrator\github\novelpick-website\scifi.html', 'r', encoding='utf-8') as f:
    content = f.read()
body_start = content.find('<div class="article-body">')
body_end = content.find('<aside class="sidebar">')
print('article-body starts at:', body_start)
print('sidebar starts at:', body_end)
# Look at what is right before </aside
print('Before sidebar:')
print(repr(content[body_end-200:body_end]))