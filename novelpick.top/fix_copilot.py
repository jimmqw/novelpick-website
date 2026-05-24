path = r'C:\Users\Administrator\.openclaw\workspace\morai.top\github-copilot-review-2026.html'
with open(path, encoding='utf-8', errors='replace') as f:
    c = f.read()
# Find the end of article-body div
idx = c.rfind('</div>')
print('last </div> at:', idx)
print(repr(c[idx-100:idx+20]))
# Also find footer position
footer_idx = c.find('<div class="footer"')
print('footer at:', footer_idx)
