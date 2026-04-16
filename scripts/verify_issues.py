# -*- coding: utf-8 -*-
"""Verify specific findings"""
import re

# 1. Check morai article - header tag vs nav-based
with open(r'C:\Users\Administrator\github\morai-website\best-ai-coding-tools-2026.html', 'r', encoding='utf-8') as f:
    m_art = f.read()
print("=== MORAI best-ai-coding-tools-2026.html ===")
print("<header tag:", bool(re.search(r'<header', m_art, re.IGNORECASE)))
print("nav:", bool(re.search(r'<nav', m_art, re.IGNORECASE)))
print("hero:", bool(re.search(r'<div class="hero|<section class="hero', m_art)))
print("article-body:", bool(re.search(r'id="article-body"', m_art)))
ab = re.search(r'<div[^>]*id="article-body"[^>]*>(.*?)</div>', m_art, re.DOTALL | re.IGNORECASE)
if ab:
    print("article-body text length:", len(re.sub(r'<[^>]+>', '', ab.group(1))))
print()

# 2. Check novelpick article - header tag and breadcrumb
with open(r'C:\Users\Administrator\github\novelpick-website\best-solo-leveling-novels.html', 'r', encoding='utf-8') as f:
    np = f.read()
print("=== NOVELPICK best-solo-leveling-novels.html ===")
print("<header tag:", bool(re.search(r'<header', np, re.IGNORECASE)))
print("nav:", bool(re.search(r'<nav', np, re.IGNORECASE)))
print("breadcrumb:", bool(re.search(r'breadcrumb', np, re.IGNORECASE)))
print("article-body:", bool(re.search(r'id="article-body"', np)))
ab2 = re.search(r'<div[^>]*id="article-body"[^>]*>(.*?)</div>', np, re.DOTALL | re.IGNORECASE)
if ab2:
    print("article-body found, text len:", len(re.sub(r'<[^>]+>', '', ab2.group(1))))
else:
    print("article-body NOT found with id=article-body")
    # Try class
    ab2b = re.search(r'<div[^>]*class="article-body"[^>]*>(.*?)</div>', np, re.DOTALL | re.IGNORECASE)
    if ab2b:
        print("Found with class=article-body, text len:", len(re.sub(r'<[^>]+>', '', ab2b.group(1))))
    # Check what id/classes contain article
    article_ids = re.findall(r'id="[^"]*article[^"]*"', np, re.IGNORECASE)
    article_classes = re.findall(r'class="[^"]*article[^"]*"', np, re.IGNORECASE)
    print("article id attrs:", article_ids)
    print("article class attrs:", article_classes)
print()

# 3. Check novelpick best-smart-protagonist (listed as OK but some flags)
with open(r'C:\Users\Administrator\github\novelpick-website\best-smart-protagonist-fantasy-novels.html', 'r', encoding='utf-8') as f:
    np2 = f.read()
print("=== NOVELPICK best-smart-protagonist ===")
print("<header tag:", bool(re.search(r'<header', np2, re.IGNORECASE)))
print("nav:", bool(re.search(r'<nav', np2, re.IGNORECASE)))
print("breadcrumb:", bool(re.search(r'breadcrumb', np2, re.IGNORECASE)))
print("article-body:", bool(re.search(r'id="article-body"', np2)))
print()

# 4. Check fateandmethod - what does header look like
with open(r'C:\Users\Administrator\github\fateandmethod-site\ziwei.html', 'r', encoding='utf-8') as f:
    fm = f.read()
print("=== FATEANDMETHOD ziwei.html ===")
print("<header tag:", bool(re.search(r'<header', fm, re.IGNORECASE)))
print("og:title:", bool(re.search(r'og:title', fm)))
print("canonical:", bool(re.search(r'canonical', fm, re.IGNORECASE)))
print("breadcrumb:", bool(re.search(r'breadcrumb', fm, re.IGNORECASE)))
article_ids_fm = re.findall(r'id="[^"]*article[^"]*"', fm, re.IGNORECASE)
article_classes_fm = re.findall(r'class="[^"]*article[^"]*"', fm, re.IGNORECASE)
print("article id attrs:", article_ids_fm)
print("article class attrs:", article_classes_fm)
print()

# 5. Check novelpick what structure article-body uses
with open(r'C:\Users\Administrator\github\novelpick-website\index.html', 'r', encoding='utf-8') as f:
    np_idx = f.read()
print("=== NOVELPICK index.html (only normal file) ===")
print("header:", bool(re.search(r'<header', np_idx, re.IGNORECASE)))
print("nav:", bool(re.search(r'<nav', np_idx, re.IGNORECASE)))
print("footer:", bool(re.search(r'<footer', np_idx, re.IGNORECASE)))
print("og:title:", bool(re.search(r'og:title', np_idx)))
print("canonical:", bool(re.search(r'canonical', np_idx)))
print("hm.baidu:", bool(re.search(r'hm\.baidu', np_idx)))
