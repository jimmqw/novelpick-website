import re
content = open(r'C:\Users\Administrator\github\novelpick-website\best-apocalypse-and-survival-novels.html', 'r', encoding='utf-8').read()

# Find exact div opening
idx = content.find('<div class="article-body">')
print('exact match at:', idx)
if idx >= 0:
    print(content[idx:idx+200])

# Find all article-body occurrences
for i, ch in enumerate(content):
    if content[i:i+16] == 'class="article-body':
        print('found at pos', i, ':', repr(content[i-5:i+80]))
        break

# Try class= with different quote
idx2 = content.find("class='article-body'")
print('single quote at:', idx2)

# Try just the class attribute
idx3 = content.find('article-body')
print('anywhere at:', idx3)
# show surrounding
if idx3 >= 0:
    print(repr(content[idx3-20:idx3+60]))