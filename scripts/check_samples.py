# -*- coding: utf-8 -*-
import re

# Check morai index
with open(r'C:\Users\Administrator\github\morai-website\index.html', 'r', encoding='utf-8') as f:
    c = f.read()
print('=== MORAI INDEX ===')
print('<header:', '<header' in c)
print('nav:', '<nav' in c)
print('breadcrumb:', 'breadcrumb' in c.lower())
sidebar_m = re.search(r'<aside|<div[^>]*id=["\']?sidebar', c, re.IGNORECASE)
print('sidebar:', sidebar_m)
print('footer:', '<footer' in c.lower())
print('article-body:', 'article-body' in c)
print('viewport:', 'viewport' in c.lower())
print()

# Check fateandmethod index  
with open(r'C:\Users\Administrator\github\fateandmethod-site\index.html', 'r', encoding='utf-8') as f:
    c2 = f.read()
print('=== FATEANDMETHOD INDEX ===')
print('<header:', '<header' in c2)
print('nav:', '<nav' in c2)
print('breadcrumb:', 'breadcrumb' in c2.lower())
sidebar_m2 = re.search(r'<aside|<div[^>]*id=["\']?sidebar', c2, re.IGNORECASE)
print('sidebar:', sidebar_m2)
print('footer:', '<footer' in c2.lower())
print('article-body:', 'article-body' in c2)
print('og:title:', 'og:title' in c2)
print('canonical:', 'canonical' in c2)
print('viewport:', 'viewport' in c2.lower())
print()

# Check a novelpick article page
with open(r'C:\Users\Administrator\github\novelpick-website\best-solo-leveling-novels.html', 'r', encoding='utf-8') as f:
    c3 = f.read()
print('=== NOVELPICK ARTICLE ===')
print('<header:', '<header' in c3)
print('nav:', '<nav' in c3)
print('breadcrumb:', 'breadcrumb' in c3.lower())
print('footer:', '<footer' in c3.lower())
print('article-body:', 'article-body' in c3)
print('og:title:', 'og:title' in c3)
print('canonical:', 'canonical' in c3)
print('hm.baidu:', 'hm.baidu' in c3)
print('viewport:', 'viewport' in c3.lower())
