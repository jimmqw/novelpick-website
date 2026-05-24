import re

content = open(r'C:\Users\Administrator\github\morai-website\ai-code-review-tools.html', 'r', encoding='utf-8', errors='replace').read()

footer = content.find('<footer')
rec = content.find('recommended')
print('footer at:', footer, 'rec at:', rec)
print('Before footer:', repr(content[footer-100:footer]))

# Check article-body extraction with my regex
# My regex: r'<div[^>]*\bclass=["\']([^"\']*\barticle-body\b[^"\']*)["\'][^>]*>(.*?)</div>\s*(?=</article|\n\s*<footer|<div class="recommended|<div class="keep)'
m = re.search(r'<div[^>]*\bclass=["\']([^"\']*\barticle-body\b[^"\']*)["\'][^>]*>(.*?)</div>', content, re.DOTALL | re.IGNORECASE)
print('article-body match:', m is not None)
if m:
    text = re.sub(r'<[^>]+>', '', m.group(2)).strip()
    print('text len:', len(text))
    print('preview:', text[:200])
else:
    print('No match - check the HTML structure')
    # Show the article-body div
    idx = content.find('class="article-body"')
    print('class="article-body" at:', idx)
    if idx >= 0:
        print(repr(content[idx-20:idx+100]))