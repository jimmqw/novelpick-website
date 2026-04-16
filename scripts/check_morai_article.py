# -*- coding: utf-8 -*-
import re

with open(r'C:\Users\Administrator\github\morai-website\best-ai-coding-tools-2026.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find article or main content block
print("Has <article:", bool(re.search(r'<article', c, re.IGNORECASE)))
print("Has main:", bool(re.search(r'<main', c, re.IGNORECASE)))
print()

# Find all class attrs containing 'article' or 'content' or 'post'
article_classes = re.findall(r'class="[^"]*"', c)
for cls in article_classes:
    if any(k in cls.lower() for k in ['article', 'content', 'post', 'main', 'body']):
        print(cls)

print()
# Find the main content area
main_match = re.search(r'<main[^>]*>(.*?)</main>', c, re.DOTALL | re.IGNORECASE)
if main_match:
    print("MAIN content (first 500):")
    print(re.sub(r'<[^>]+>', '', main_match.group(1))[:500])
else:
    print("No <main> found")
    # Find what follows breadcrumb
    idx = c.find('breadcrumb')
    if idx >= 0:
        print("After breadcrumb (200 chars):")
        print(re.sub(r'<[^>]+>', '', c[idx:idx+500]))
