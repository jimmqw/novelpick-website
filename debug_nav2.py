# -*- coding: utf-8 -*-
import re

# Check novelpick best-apocalypse-survival-web-novels.html
with open(r'C:\Users\Administrator\github\novelpick-website\best-apocalypse-survival-web-novels.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# My current header check:
has_header_tag = bool(re.search(r'<header[^>]*>', content, re.IGNORECASE))
has_nav_header = bool(re.search(r'<nav[^>]*class=["\'][^"\']*nav[^"\']*["\']', content, re.IGNORECASE))
has_fixed_nav = bool(re.search(r'<nav[^>]*position:\s*(fixed|sticky)', content, re.IGNORECASE))
has_div_header = bool(re.search(r'<div[^>]*class=["\'][^"\']*header[^"\']*["\']', content, re.IGNORECASE))
has_fixed_div = bool(re.search(r'(position:fixed|position\s*:\s*fixed).*top:\s*0', content, re.IGNORECASE))

print('header_tag:', has_header_tag)
print('nav_header:', has_nav_header)
print('fixed_nav:', has_fixed_nav)
print('div_header:', has_div_header)
print('fixed_div:', has_fixed_div)

# Check if <nav> exists
m = re.search(r'<nav\b', content, re.IGNORECASE)
print('nav exists:', bool(m))

# Check nav CSS
m2 = re.search(r'nav\s*\{[^}]*position:\s*(sticky|fixed)', content, re.IGNORECASE | re.DOTALL)
print('nav CSS position:', m2.group(0) if m2 else 'not found')
