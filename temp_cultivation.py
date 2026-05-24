content = open(r'C:\Users\Administrator\github\novelpick-website\best-cultivation-novels-2026.html', 'r', encoding='utf-8', errors='replace').read()

footer = content.find('<footer')
# Show the closing structure before footer
print('Last 1000 chars before footer:')
segment = content[footer-1000:footer]
print(repr(segment[-500:]))

# Find the last 5 </div> before footer
import re
div_closes = [m.start() for m in re.finditer(r'</div>', segment)]
print(f'\nLast </div> positions in segment (relative to segment):')
for pos in div_closes[-5:]:
    print(f'  {pos}: {repr(segment[pos-5:pos+20])}')

# Find the article-body closing
ab = content.find('class="article-body"')
ab_open = content.find('>', ab)
# Find </article> after article-body
art_close = content.find('</article>', ab_open)
print(f'\narticle-body opens at: {ab_open}')
print(f'</article> at: {art_close}')
print(f'Context: {repr(content[art_close-50:art_close+30])}')
