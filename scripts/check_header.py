# -*- coding: utf-8 -*-
import re

# Check morai index header structure
with open(r'C:\Users\Administrator\github\morai-website\index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find body and first 3000 chars
body_start = c.find('<body')
print("First 3000 chars from body:")
print(c[body_start:body_start+3000])
print()

# Check what header-like element morai uses
print("Has <header:", '<header' in c)
print("Has id=header:", re.search(r'id=["\']header', c))
print("Has class=header:", re.search(r'class=["\'][^"\']*header', c))
print()

# Check fateandmethod for similar
with open(r'C:\Users\Administrator\github\fateandmethod-site\index.html', 'r', encoding='utf-8') as f:
    fmg = f.read()
print("FATEANDMETHOD first 1500 chars from body:")
body_start2 = fmg.find('<body')
print(fmg[body_start2:body_start2+1500])
print()

# Check novelpick breadcrumb
with open(r'C:\Users\Administrator\github\novelpick-website\best-solo-leveling-novels.html', 'r', encoding='utf-8') as f:
    np = f.read()
# Find nav or header section
nav_match = re.search(r'<nav[^>]*>.*?</nav>', np, re.DOTALL | re.IGNORECASE)
if nav_match:
    print("NOVELPICK nav content:")
    print(nav_match.group(0)[:500])
