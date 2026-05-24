# -*- coding: utf-8 -*-
import re

# Files that had genuine issues (not header/article-body detection false positives)
# Let's check what actual structural issues exist

issues_to_check = [
    (r"C:\Users\Administrator\github\morai-website\template.html", "template file"),
    (r"C:\Users\Administrator\github\morai-website\github-copilot-review-2026.html", "missing breadcrumb + baidu"),
    (r"C:\Users\Administrator\github\novelpick-website\best-reincarnation-web-novels-2026.html", "only baidu missing"),
    (r"C:\Users\Administrator\github\fateandmethod-site\chinese-zodiac-compatibility-guide.html", "multiple meta missing"),
]

for fpath, desc in issues_to_check:
    print(f"\n=== {fpath.split('\\')[-1]} ({desc}) ===")
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        c = f.read()

    # breadcrumb
    bc = re.search(r'breadcrumb|面包屑', c, re.IGNORECASE)
    print(f"breadcrumb: {bc is not None}")

    # baidu
    bd = re.search(r'hm\.baidu\.com', c)
    print(f"baidu: {bd is not None}")

    # og:title
    og = re.search(r'property=["\']og:title["\']', c, re.IGNORECASE)
    print(f"og:title: {og is not None}")

    # desc
    dc = re.search(r'<meta[^>]+name=["\']description["\']', c, re.IGNORECASE)
    print(f"description: {dc is not None}")

    # canonical
    ca = re.search(r'<link[^>]+rel=["\']canonical["\']', c, re.IGNORECASE)
    print(f"canonical: {ca is not None}")

    # viewport
    vp = re.search(r'<meta[^>]+name=["\']viewport["\']', c, re.IGNORECASE)
    print(f"viewport: {vp is not None}")

    # @media
    md = re.search(r'@media\s*\(', c)
    print(f"@media: {md is not None}")

    # body bg
    body_bg = re.search(r'body[^}]*\{[^}]*background', c, re.IGNORECASE)
    print(f"body background: {body_bg is not None}")

    # article content
    at = re.search(r'<article[^>]*>(.*?)</article>', c, re.DOTALL | re.IGNORECASE)
    ab = re.search(r'<div[^>]*class=["\']article-body["\'][^>]*>', c, re.IGNORECASE)
    if at:
        text = re.sub(r'<[^>]+>', '', at.group(1))
        text = re.sub(r'\s+', '', text)
        print(f"article text len: {len(text)}")
    elif ab:
        # find the closing div
        start = ab.end()
        depth = 1
        i = start
        while i < len(c) and depth > 0:
            if c[i:i+5] == '<div ' or c[i:i+5] == '<div>':
                depth += 1
            elif c[i:i+6] == '</div>':
                depth -= 1
            i += 1
        article_text = re.sub(r'<[^>]+>', '', c[start:i-6])
        article_text = re.sub(r'\s+', '', article_text)
        print(f"article-body text len: {len(article_text)}")
    else:
        # body text
        body = re.search(r'<body[^>]*>(.*?)</body>', c, re.DOTALL | re.IGNORECASE)
        if body:
            text = re.sub(r'<[^>]+>', '', body.group(1))
            text = re.sub(r'\s+', '', text)
            print(f"body text len: {len(text)}")
