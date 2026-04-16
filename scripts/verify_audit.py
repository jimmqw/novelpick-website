"""Verify audit script was giving false positives"""
import re
import os

def find_article_body_precise(content):
    m = re.search(r'<div[^>]*id=["\']?article-body["\']?[^>]*>', content, re.IGNORECASE)
    if not m:
        m = re.search(r'<div[^>]*class=["\']?[^"\']*article-body[^"\']*["\'][^>]*>', content, re.IGNORECASE)
    if not m:
        return None, None
    ab_start = m.end()
    depth = 1
    pos = ab_start
    while pos < len(content) and depth > 0:
        next_open = content.find('<div', pos)
        next_close = content.find('</div>', pos)
        if next_close < 0:
            break
        if next_open >= 0 and next_open < next_close:
            depth += 1
            pos = next_open + 5
        else:
            depth -= 1
            if depth == 0:
                return m.start(), next_close + 6
            pos = next_close + 6
    return m.start(), None

# Check the file that audit reported as "open=2 close=0"
novel = r'C:\Users\Administrator\github\novelpick-website\best-cyberpunk-novels.html'
content = open(novel, encoding='utf-8').read()
result = find_article_body_precise(content)
if result[0]:
    ab_start, ab_end = result
    region = content[ab_start:ab_end]
    opens = region.count('<div')
    closes = region.count('</div>')
    print(f"best-cyberpunk-novels.html: open={opens} close={closes} balance={opens-closes}")
    print(f"article-body region: {len(region)} chars")
    print(f"Content text length: {len(re.sub(r'<[^>]+>', '', region))}")
    print(f"First 200 chars: {region[:200]}")
else:
    print("No article-body found")

# Check another: best-cozy-fantasy-novels
novel2 = r'C:\Users\Administrator\github\novelpick-website\best-cozy-fantasy-novels.html'
content2 = open(novel2, encoding='utf-8').read()
result2 = find_article_body_precise(content2)
if result2[0]:
    ab_start, ab_end = result2
    region = content2[ab_start:ab_end]
    opens = region.count('<div')
    closes = region.count('</div>')
    text = re.sub(r'<[^>]+>', '', region)
    print(f"\nbest-cozy-fantasy-novels.html: open={opens} close={closes} balance={opens-closes}")
    print(f"Text length: {len(text.strip())} chars")
else:
    print("No article-body found in best-cozy-fantasy-novels.html")
