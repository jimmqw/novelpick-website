# -*- coding: utf-8 -*-
import re

fpath = r"C:\Users\Administrator\github\morai-website\ai-agent-tools-2026.html"
with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
    c = f.read()

# header check
print("=== header check ===")
hm = re.search(r'<header[^>]*>.*?</header>', c, re.DOTALL | re.IGNORECASE)
print(f"<header> tag: {hm is not None}")
hd = re.search(r'<div[^>]*\bid=["\']header["\'][^>]*>', c, re.IGNORECASE)
print(f'<div id="header">: {hd is not None}')
hc = re.search(r'<div[^>]*class=["\'][^"\']*header[^"\']*["\'][^>]*>', c, re.IGNORECASE)
print(f'class contains header: {hc is not None}')

# check what nav element looks like
nav_match = re.search(r'<nav[^>]*>.*?</nav>', c, re.DOTALL | re.IGNORECASE)
if nav_match:
    print(f"\nNav content (first 300): {nav_match.group(0)[:300]}")

# article-body class
ab = re.search(r'<div[^>]*class=["\']article-body["\'][^>]*>', c, re.IGNORECASE)
print(f"\nclass='article-body' div: {ab is not None}")
if ab:
    print(f"  -> {ab.group(0)}")

# article-body id
abid = re.search(r'<div[^>]*id=["\']article-body["\'][^>]*>', c, re.IGNORECASE)
print(f'id="article-body" div: {abid is not None}')

# the original check: id="article-body"
print(f"\nOriginal script uses id='article-body': {abid is not None}")
print(f"But the file uses class='article-body': {ab is not None}")

# footer
ft = re.search(r'<footer', c, re.IGNORECASE)
print(f"\nfooter: {ft is not None}")
if ft:
    print(f"  -> {ft.group(0)[:100]}")

# breadcrumb
bc = re.search(r'breadcrumb', c, re.IGNORECASE)
print(f"\nbreadcrumb: {bc is not None}")
