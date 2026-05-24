# -*- coding: utf-8 -*-
import re

files = [
    r"C:\Users\Administrator\github\morai-website\best-ai-design-tools-2026.html",
    r"C:\Users\Administrator\github\morai-website\ai-agent-tools-2026.html",
    r"C:\Users\Administrator\github\morai-website\index.html",
    r"C:\Users\Administrator\github\morai-website\chatgpt-vs-claude-vs-gemini-2026.html",
    r"C:\Users\Administrator\github\morai-website\how-ai-agents-transform-knowledge-work-2026.html",
    r"C:\Users\Administrator\github\morai-website\best-ai-research-assistants-2026.html",
]

for fpath in files:
    print(f"\n=== {fpath.split('\\')[-1]} ===")
    try:
        with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
            c = f.read()
    except Exception as e:
        print(f"Error: {e}")
        continue

    # header
    hm = re.search(r'<header[^>]*>.*?</header>', c, re.DOTALL | re.IGNORECASE)
    hd = re.search(r'<div[^>]*\bid=["\']header["\'][^>]*>', c, re.IGNORECASE)
    hc = re.search(r'<div[^>]*class=["\'][^"\']*header[^"\']*["\'][^>]*>', c, re.IGNORECASE)
    print(f"header: {hm is not None or hd is not None or hc is not None}")
    if hc and not hm and not hd:
        print(f"  class header: {hc.group(0)[:80]}")

    # article
    ab = re.search(r'<div[^>]*id=["\']article[-_]?body["\'][^>]*>', c, re.IGNORECASE)
    at = re.search(r'<article[^>]*>(.*?)</article>', c, re.DOTALL | re.IGNORECASE)
    print(f"article-body div: {ab is not None}")
    print(f"article tag: {at is not None}")

    if at:
        text = re.sub(r'<[^>]+>', '', at.group(1))
        text = re.sub(r'\s+', '', text)
        print(f"article text len: {len(text)}")

    # breadcrumb
    bc = re.search(r'breadcrumb|面包屑', c, re.IGNORECASE)
    print(f"breadcrumb: {bc is not None}")

    # sidebar
    sb = re.search(r'sidebar|侧边栏|aside', c, re.IGNORECASE)
    print(f"sidebar: {sb is not None}")

    # related
    rl = re.search(r'related|相关文章|recommended', c, re.IGNORECASE)
    print(f"related: {rl is not None}")

    # footer
    ft = re.search(r'<footer', c, re.IGNORECASE)
    print(f"footer: {ft is not None}")

    # cp
    cp = re.search(r'©|copyright|&copy;|版权所有', c, re.IGNORECASE)
    print(f"copyright: {cp is not None}")

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
