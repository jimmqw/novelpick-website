with open(r'C:\Users\Administrator\github\novelpick-website\scifi.html', 'r', encoding='utf-8') as f:
    c = f.read()
b = c[c.find('<div class="article-body">'):c.find('<aside class="sidebar">')]
print('Body chars:', len(b))
# Check for Chinese quotes
if '\u201c' in b or '\u201d' in b:
    print('WARN: Chinese quotes found')
else:
    print('No Chinese quotes OK')
# Check for em dashes
if '\u2014' in b:
    print('WARN: em dashes found')
else:
    print('No em dashes OK')
# Check for double title duplication
title_count = c.count('<h1>Best Sci-Fi Novels')
print('h1 title count:', title_count)