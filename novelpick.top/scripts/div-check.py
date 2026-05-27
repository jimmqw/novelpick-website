import re

# Check best-ai-agents-2026.html for div issues
with open(r'C:\Users\Administrator\.openclaw\workspace\morai.top\best-ai-agents-2026.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find article-body
m = re.search(r'<div class="article-body">(.*?)</div>', content, re.DOTALL)
if m:
    body = m.group(1)
    opens = body.count('<div')
    closes = body.count('</div')
    print(f'Opens: {opens}, Closes: {closes}, Balance: {opens - closes}')
    print('Last 600 chars:')
    print(repr(body[-600:]))
else:
    print('No article-body found')

print('\n--- best-ai-video-generation-tools-2026.html ---')
with open(r'C:\Users\Administrator\.openclaw\workspace\morai.top\best-ai-video-generation-tools-2026.html', 'r', encoding='utf-8') as f:
    content2 = f.read()

m2 = re.search(r'<div class="article-body">(.*?)</div>', content2, re.DOTALL)
if m2:
    body2 = m2.group(1)
    opens2 = body2.count('<div')
    closes2 = body2.count('</div')
    print(f'Opens: {opens2}, Closes: {closes2}, Balance: {opens2 - closes2}')
    print('Last 600 chars:')
    print(repr(body2[-600:]))