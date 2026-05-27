import re
with open(r'C:\Users\Administrator\.openclaw\workspace\morai.top\best-ai-agents-2026.html', 'rb') as f:
    c = f.read()
# Find all href that end in .html
hrefs = re.findall(b'href="([^"]+\.html)"', c)
for h in set(hrefs):
    print(h.decode())
