import re

content = open(r'C:\Users\Administrator\github\morai-website\best-ai-coding-assistants-2026.html', 'r', encoding='utf-8', errors='replace').read()

print('Whole file div counts:')
print('  <div  (with space):', content.count('<div '))
print('  <div> (with close):', content.count('<div>'))
print('  </div>:', content.count('</div>'))

# Count self-closing divs
self_closing = len(re.findall(r'<div[^/>]*/>', content))
print('  self-closing:', self_closing)

# The issue: overall file has opens=47, closes=46. But article-body segment has opens=36, closes=38
# This means the article-body segment has 2 more closes than opens
# But overall file has 1 more open than close
# So the BEFORE article-body part has more opens than closes?

# Let's check the before segment
ab_pos = content.find('class="article-body"')
before = content[:ab_pos]
print('\nBefore article-body:')
print('  <div :', before.count('<div '))
print('  <div>:', before.count('<div>'))
print('  </div>:', before.count('</div>'))
print('  diff:', before.count('<div ') + before.count('<div>') - before.count('</div>'))

# After article-body
footer_pos = content.find('<footer')
rec_pos = content.find('class="recommended"')
end_pos = min(footer_pos if footer_pos > 0 else 999999, rec_pos if rec_pos > 0 else 999999)
after = content[end_pos:]
print('\nAfter article-body:')
print('  <div :', after.count('<div '))
print('  <div>:', after.count('<div>'))
print('  </div>:', after.count('</div>'))
print('  diff:', after.count('<div ') + after.count('<div>') - after.count('</div>'))

# Let's look at the article-body closing
# Find the </div> that closes the article-body container
# Search backwards from footer to find the div that should close the main article-body wrapper
# The article-body div contains content, so we need to find the </div> that matches its opening

# Find the article-body div opening
ab_start = content.find('<div class="article-body"')
ab_open_end = content.find('>', ab_start)
ab_content = content[ab_open_end+1:]

# Find how many nested divs are inside article-body
# The article-body div should close at the </div> that has the same nesting depth
# This is the </div> right before <footer> or <div class="recommended"

# Find the </aside> or </section> that closes the article-body wrapper
search = content[ab_start:]
# Find position of last </div> in article-body section
last_div_in_article = content.rfind('</div>', 0, footer_pos)
print(f'\nLast </div> before footer at: {last_div_in_article}')
print(f'Context: {repr(content[last_div_in_article-50:last_div_in_article+20])}')
print(f'Next 100 chars after last div: {repr(content[last_div_in_article+6:last_div_in_article+106])}')