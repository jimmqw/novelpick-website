import re
html = open(r'C:\Users\Administrator\github\morai-website\ai-agent-tools-2026.html', 'r', encoding='utf-8').read()

# Find article-body
ab_match = re.search(r'<div[^>]*class=["\'][^"\']*article-body["\'][^>]*>', html, re.IGNORECASE)
print(f'article-body tag: {html[ab_match.start():ab_match.end()]}')
print(f'article-body start: {ab_match.start()}, end: {ab_match.end()}')

# Find what comes after article-body
start = ab_match.end()
# Find the FIRST </div> after article-body start
close = html.find('</div>', start)
print(f'\nFirst </div> after article-body at pos: {close}')
print(f'Context around close: ...{html[close-50:close+20]}...')

# But article-body might contain nested divs that we should look past
# Let me find ALL </div> occurrences in article-body region
# and see the structure
content_start = ab_match.end()
content_end = len(html)
article_body_section = html[content_start:content_end]

# Find the actual closing tag that matches article-body's depth
# Simple approach: find </div></div></div> sequence near the end
print('\n--- Looking for proper article-body close ---')
# The article-body content goes until we see the closing structure
# Let me look for the pattern that closes article-body

# Check what comes after the first </div>
after_first_close = html[close+6:close+100]
print(f'After first </div>: {after_first_close[:80]}')

# Maybe the article-body actually contains more divs and we need to find
# a later </div> that properly closes it
# Let's look at the last 500 chars of the file
print(f'\n--- Last 500 chars of file ---')
print(html[-500:])
