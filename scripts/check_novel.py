import re, os

path = 'C:\\Users\\Administrator\\github\\novelpick-website\\best-action-fantasy-web-novels-2026.html'
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    c = f.read()
# Find what class the article uses
m = re.search(r'<article[^>]*class="([^"]+)"', c)
if m: print('article class:', m.group(1))
m2 = re.search(r'<div[^>]*class="([^"]*(?:body|content|main)[^"]*)"', c)
if m2: print('content div class:', m2.group(1))
# Check baidu
print('has baidu:', 'hm.baidu.com' in c)
# Check div balance
open_d = len(re.findall(r'<div\b(?!/)', c))
close_d = len(re.findall(r'</div>', c))
print('div balance: open=%d close=%d diff=%d' % (open_d, close_d, open_d - close_d))
# Find article content
am = re.search(r'<article[^>]*>(.*?)</article>', c, re.DOTALL)
if am:
    text = re.sub(r'<[^>]+>', '', am.group(1))
    print('article text length:', len(text))
else:
    print('no article tag found')