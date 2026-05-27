import re

content = open(r'C:\Users\Administrator\github\morai-website\best-ai-coding-assistants-2026.html', 'r', encoding='utf-8', errors='replace').read()

# Find article-body div
ab_patterns = ['class="article-body"', 'id="article-body"', "class='article-body'"]
ab_pos = -1
for p in ab_patterns:
    ab_pos = content.find(p)
    if ab_pos >= 0:
        print(f'Found: {p} at {ab_pos}')
        break

footer_pos = content.find('<footer')
rec_pos = content.find('class="recommended"')

end_pos = len(content)
if footer_pos > 0:
    end_pos = min(end_pos, footer_pos)
if rec_pos > 0:
    end_pos = min(end_pos, rec_pos)

segment = content[ab_pos:end_pos]
opens = segment.count('<div ')
closes = segment.count('</div>')
print(f'In article-body segment: opens={opens}, closes={closes}, diff={opens-closes}')

# Show full context around the problem
# Find all </div> in the segment
div_closes = [m.start() for m in re.finditer(r'</div>', segment)]
print(f'Total </div> in segment: {len(div_closes)}')
print(f'Last 5 div close positions: {div_closes[-5:]}')

# Show content around the last </div> in segment
if div_closes:
    last = div_closes[-1]
    print(f'Last div close context: {repr(segment[last-100:last+20])}')

# Check what comes after the last </div> in segment
print(f'After last </div>: {repr(segment[last+6:last+100])}')