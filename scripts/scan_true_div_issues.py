"""Precise div balance check - scan all files and report true imbalance"""
import re
import os
from pathlib import Path

def find_article_body_precise(content):
    """Find article-body region by tracking nesting level"""
    # Find opening tag
    m = re.search(r'<div[^>]*id=["\']?article-body["\']?[^>]*>', content, re.IGNORECASE)
    if not m:
        m = re.search(r'<div[^>]*class=["\']?[^"\']*article-body[^"\']*["\'][^>]*>', content, re.IGNORECASE)
    if not m:
        return None, None
    
    ab_start = m.end()
    
    # Track nesting depth to find actual closing tag
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

def check_file(filepath):
    try:
        content = open(filepath, encoding='utf-8').read()
    except:
        return None
    
    result = find_article_body_precise(content)
    if result[0] is None:
        return None
    
    ab_start, ab_end = result
    if ab_end is None:
        return "UNCLOSED"
    
    region = content[ab_start:ab_end]
    opens = region.count('<div')
    closes = region.count('</div>')
    balance = opens - closes
    
    if balance != 0:
        return f"open={opens} close={closes} balance={balance}"
    return None

# Scan morai
morai_path = r'C:\Users\Administrator\github\morai-website'
morai_issues = []
for f in os.listdir(morai_path):
    if f.endswith('.html'):
        res = check_file(os.path.join(morai_path, f))
        if res:
            morai_issues.append(f"{f}: {res}")

print("=== MORAI DIV ISSUES ===")
for i in morai_issues:
    print(i)
print(f"Total: {len(morai_issues)}")

# Scan novelpick
novel_path = r'C:\Users\Administrator\github\novelpick-website'
novel_issues = []
for f in os.listdir(novel_path):
    if f.endswith('.html'):
        res = check_file(os.path.join(novel_path, f))
        if res:
            novel_issues.append(f"{f}: {res}")

print("\n=== NOVELPICK DIV ISSUES ===")
for i in novel_issues:
    print(i)
print(f"Total: {len(novel_issues)}")
