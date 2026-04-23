path = r'C:\Users\Administrator\.openclaw\workspace\morai.top\best-ai-agents-2026.html'
with open(path, encoding='utf-8', errors='replace') as f:
    c = f.read()
idx = c.find('prev-next')
# Find the HTML element, not CSS
search_start = c.find('<div class="prev-next"')
if search_start >= 0:
    print('Found at:', search_start)
    print(repr(c[search_start:search_start+300]))
else:
    print('No <div class=prev-next found')
    # Check what's around the CSS prev-next
    print(c[idx:idx+200])
