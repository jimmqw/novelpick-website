with open(r'C:\Users\Administrator\github\novelpick-website\scifi.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the orphaned </div> between article-body close and <div class="related">
article_body_close = content.find('</div>', content.find('<div class="article-body">'))
related = content.find('<div class="related">')

# The orphaned div is the </div> between article_body_close and related
# article_body_close is the first </div> after article-body opens
# We need to find the </div> that comes after that (article-body close) but before related
second_div = content.find('</div>', article_body_close + 5)

print('article-body closes at:', article_body_close)
print('second div at:', second_div)
print('related div at:', related)

# Check content between second_div and related
print('Between second_div and related:')
print(repr(content[second_div:related]))

# Remove the orphaned </div>
old = '''        </div>
    </div>
    <div class="related">'''

new = '''    </div>
    <div class="related">'''

if old in content:
    content = content.replace(old, new, 1)
    with open(r'C:\Users\Administrator\github\novelpick-website\scifi.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('SUCCESS: removed orphaned </div>')
else:
    print('ERROR: orphaned div not found')
    print('Looking for:')
    print(repr(old))