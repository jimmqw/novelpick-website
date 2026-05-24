import re

# Test on a real file
content = open(r'C:\Users\Administrator\github\fateandmethod-site\bazi.html', 'r', encoding='utf-8').read()

# Try different extraction approaches
m1 = re.search(r'<div[^>]*\bid=["\']article-body["\'][^>]*>(.*?)</div>\s*<footer', content, re.DOTALL | re.IGNORECASE)
print('id match:', m1 is not None)

m2 = re.search(r'<div[^>]*\bclass=["\'][^"\']*article-body[^"\']*["\'][^>]*>(.*?)</div>\s*<footer', content, re.DOTALL | re.IGNORECASE)
print('class match:', m2 is not None)

m3 = re.search(r'<article[^>]*>(.*?)<footer', content, re.DOTALL | re.IGNORECASE)
print('article match:', m3 is not None)

# Show the article-body div
idx = content.find('article-body')
if idx >= 0:
    snippet = content[idx-10:idx+80]
    print('snippet at', idx, ':', repr(snippet))

# Try with content split
article_start = content.find('<article')
footer_start = content.find('<footer')
if article_start >= 0 and footer_start >= 0:
    article_content = content[article_start:footer_start]
    text = re.sub(r'<[^>]+>', '', article_content)
    print('article text length (no tags):', len(text.strip()))
    print('first 200 chars:', text[:200])