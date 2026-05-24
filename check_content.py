# -*- coding: utf-8 -*-
import re

# Sample a few files that show "0 character" article body
files = [
    r"C:\Users\Administrator\github\morai-website\ai-comparisons.html",
    r"C:\Users\Administrator\github\novelpick-website\best-action-fantasy-web-novels-2026.html",
    r"C:\Users\Administrator\github\fateandmethod-site\bazi-beginners-complete-guide.html",
]

for fpath in files:
    print(f"\n=== {fpath.split('\\')[-1]} ===")
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        c = f.read()

    # Check article-body class
    ab = re.search(r'<div[^>]*class=["\']article-body["\'][^>]*>', c, re.IGNORECASE)
    print(f"class='article-body': {ab is not None}")
    if ab:
        print(f"  Match: {ab.group(0)}")
        # Find closing div
        start = ab.end()
        depth = 1
        i = start
        while i < len(c) and depth > 0:
            if c[i:i+5] in ['<div ', '<div>']:
                depth += 1
            elif c[i:i+6] == '</div>':
                depth -= 1
            i += 1
        inner = c[start:i-6]
        text = re.sub(r'<[^>]+>', '', inner)
        text = re.sub(r'\s+', '', text)
        print(f"  Text length: {len(text)}")
        print(f"  First 100 chars: {text[:100]}")

    # Check article tag
    at = re.search(r'<article[^>]*>(.*?)</article>', c, re.DOTALL | re.IGNORECASE)
    print(f"article tag: {at is not None}")
    if at:
        text = re.sub(r'<[^>]+>', '', at.group(1))
        text = re.sub(r'\s+', '', text)
        print(f"  Text length: {len(text)}")

    # Check main content
    main = re.search(r'<main[^>]*>(.*?)</main>', c, re.DOTALL | re.IGNORECASE)
    print(f"main tag: {main is not None}")
    if main:
        text = re.sub(r'<[^>]+>', '', main.group(1))
        text = re.sub(r'\s+', '', text)
        print(f"  Text length: {len(text)}")

    # Check body
    body = re.search(r'<body[^>]*>(.*?)</body>', c, re.DOTALL | re.IGNORECASE)
    if body:
        text = re.sub(r'<[^>]+>', '', body.group(1))
        text = re.sub(r'\s+', '', text)
        print(f"body text length: {len(text)}")
