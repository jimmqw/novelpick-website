import re

content = open(r'C:\Users\Administrator\github\morai-website\best-ai-coding-assistants-2026.html', 'r', encoding='utf-8', errors='replace').read()

# Find article-body content start and end
ab_class = content.find('class="article-body"')
ab_open = content.find('>', ab_class)

# Find where article-body actually opens (after the CSS)
# The CSS is in <style>, the article-body div is in body
style_end = content.find('</style>', ab_class)
body_start = content.find('<body')
main_open = content.find('<main')
main_close = content.find('</main>')

# The article-body content div starts after <main>
# Let's find <div class="article-body"> in the body
in_body = content[body_start:]
ab_div = in_body.find('class="article-body"')
ab_div_open = in_body.find('>', ab_div)
print(f'Article-body div opens at: {body_start + ab_div_open}')
print(f'Context: {repr(in_body[ab_div_open:ab_div_open+50])}')

# Find closing
depth = 1
for m in re.finditer(r'<div|</div>', in_body[ab_div_open+1:]):
    if m.group() == '<div':
        depth += 1
    else:
        depth -= 1
    if depth == 0:
        close_pos = ab_div_open + 1 + m.start()
        print(f'Article-body closes at: {body_start + close_pos}')
        print(f'Context: {repr(in_body[close_pos-50:close_pos+50])}')
        break

# What's after the article-body close?
after_ab = in_body[close_pos:close_pos+200]
print(f'\nAfter article-body close:')
print(f'opens: {after_ab.count("<div ")}, closes: {after_ab.count("</div>")}')
print(repr(after_ab[:200]))
