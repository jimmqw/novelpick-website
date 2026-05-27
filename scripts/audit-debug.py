#!/usr/bin/env python3
"""Debug: check why audit false positives happen"""
import re, os

def analyze(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()
    
    name = os.path.basename(filepath)
    # Check header
    has_header = bool(re.search(r'<header\b', c))
    has_nav = bool(re.search(r'<nav\b', c))
    
    # Check article body extraction
    # Fallback 1: article tag
    m = re.search(r'<article[^>]*>(.*?)</article>', c, re.DOTALL)
    body_text = ''
    if m:
        body_text = m.group(1)
    else:
        # Fallback 2: article-body div
        m = re.search(r'class=["\']article-body["\'][^>]*>(.*?)(?=<div\s)', c, re.DOTALL)
        if m:
            body_text = m.group(1)
    
    # Clean text
    clean = re.sub(r'<[^>]+>', '', body_text)
    clean = re.sub(r'\s+', ' ', clean).strip()
    
    # Footer tag vs div
    has_footer_tag = bool(re.search(r'<footer\b', c))
    has_footer_div = bool(re.search(r'<div\s+class=["\']footer["\']', c))
    
    # Related articles
    has_related = bool(re.search(r'related|相关文章|relacionados', c, re.IGNORECASE))
    
    # Baidu
    has_baidu = bool(re.search(r'hm\.baidu\.com', c))
    
    # Background
    has_bg_color = bool(re.search(r'background-color', c))
    has_bg = bool(re.search(r'background[:\s]', c))
    
    # Read time
    has_readtime = bool(re.search(r'read[_-]time|阅读时间|min read|分钟阅读', c, re.IGNORECASE))
    
    return {
        'name': name,
        'has_header': has_header, 'has_nav': has_nav,
        'body_len': len(clean),
        'has_footer_tag': has_footer_tag, 'has_footer_div': has_footer_div,
        'has_related': has_related, 'has_baidu': has_baidu,
        'has_bg_color': has_bg_color, 'has_bg': has_bg,
        'has_readtime': has_readtime
    }

print(f"{'FILE':35s} {'hdr':3s} {'nav':3s} {'body_len':8s} {'ft_tag':3s} {'ft_div':3s} {'rel':3s} {'bd':3s} {'bg_clr':3s} {'bg':3s} {'rt':3s}")
print("-"*100)

test_files = [
    r'C:\Users\Administrator\github\morai-website\ai-agent-tools-2026.html',
    r'C:\Users\Administrator\github\morai-website\index.html',
    r'C:\Users\Administrator\github\morai-website\best-ai-research-assistants-2026.html',
    r'C:\Users\Administrator\github\novelpick-website\best-cultivation-novels-2026.html',
    r'C:\Users\Administrator\github\novelpick-website\index.html',
    r'C:\Users\Administrator\github\fateandmethod-site\index.html',
    r'C:\Users\Administrator\github\fateandmethod-site\bazi-ten-gods-guide.html',
]

for f in test_files:
    if os.path.exists(f):
        r = analyze(f)
        print(f"{r['name']:35s} {str(r['has_header']):3s} {str(r['has_nav']):3s} {str(r['body_len']):8s} {str(r['has_footer_tag']):3s} {str(r['has_footer_div']):3s} {str(r['has_related']):3s} {str(r['has_baidu']):3s} {str(r['has_bg_color']):3s} {str(r['has_bg']):3s} {str(r['has_readtime']):3s}")
