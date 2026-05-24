import re
content = open(r'C:\Users\Administrator\github\novelpick-website\best-apocalypse-and-survival-novels.html', 'r', encoding='utf-8').read()

# The article-body div uses class attribute
# Find: <div class="article-body">
pattern = r'<div[^>]*class=["\'][^"\']*article-body[^"\']*["\'][^>]*>'
matches = list(re.finditer(pattern, content))
print('found', len(matches), 'article-body divs')
for m in matches:
    end_tag = content.index('>', m.start())
    snippet = content[m.start():end_tag+1]
    print('pos', m.start(), ':', snippet)
    # Find matching </div>
    inner = content[end_tag+1:]
    # Find where this div closes - but we need to track nesting
    # For now just show 200 chars after opening
    print('  content after:', inner[:200])
    break

# Simpler: find article-body div and grab content until next sibling div or footer
ab_pos = content.find('class="article-body"')
print('\narticle-body class pos:', ab_pos)
# Find the opening >
ab_open = content.find('>', ab_pos)
print('opening > at:', ab_open)
print('snippet:', content[ab_open-50:ab_open+50])

# Look for the content - what comes after the opening tag?
after = content[ab_open+1:]
# Find the next </div> that closes this div
# First find the class name
ab_class_start = content.rfind('<div', 0, ab_pos)
ab_class_end = content.index('>', ab_class_start)
print('div tag at:', ab_class_start, '-', ab_class_end)
print('div:', content[ab_class_start:ab_class_end+1])

# Try to extract between this div and footer
# Find the article-body container: the div with class=article-body
# and grab everything until the next major section (footer or recommended)
footer_pos = content.find('<footer')
recommended_pos = content.find('<div class="recommended"')
print('footer at:', footer_pos, ', recommended at:', recommended_pos)

# What's between ab_class_end+1 and footer?
segment = content[ab_class_end+1:footer_pos]
text = re.sub(r'<[^>]+>', '', segment)
print('text length:', len(text.strip()))
print('first 200:', text[:200])
print('last 200:', text[-200:])