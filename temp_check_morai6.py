import re

content = open(r'C:\Users\Administrator\github\morai-website\best-ai-coding-assistants-2026.html', 'r', encoding='utf-8', errors='replace').read()

# Find article-body opening
ab = content.find('class="article-body"')
# Find its closing >
ab_open = content.find('>', ab)

# Track nesting: every <div increments depth, every </div decrements
# We start with depth=1 because we're INSIDE the article-body div
depth = 1
search_start = ab_open + 1

matches = list(re.finditer(r'<div|</div>', content[search_start:]))
for m in matches:
    if m.group() == '<div':
        depth += 1
    else:  # </div>
        depth -= 1
        if depth < 0:
            close_pos = search_start + m.start()
            print(f'article-body closes at: {close_pos}')
            print(f'Context: {repr(content[close_pos-30:close_pos+20])}')
            # Check what's after
            print(f'After: {repr(content[close_pos+6:close_pos+100])}')
            break

# Count how many divs are properly nested inside article-body
total_divs_in_article = sum(1 for m in matches if m.group() == '<div')
total_closes_in_article = sum(1 for m in matches if m.group() == '</div')
print(f'\nInside article-body: {total_divs_in_article} opens, {total_closes_in_article} closes')
print(f'Net: {total_divs_in_article - total_closes_in_article} (should be 0 for proper nesting)')
print(f'Actual closing depth: {depth}')