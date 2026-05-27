# -*- coding: utf-8 -*-
import re

# Check best-ai-search-research-tools-2026.html
with open(r'C:\Users\Administrator\github\morai-website\best-ai-search-research-tools-2026.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

has_header_tag = bool(re.search(r'<header[^>]*>', content, re.IGNORECASE))
has_nav_class_nav = bool(re.search(r'<nav[^>]*class=["\'][^"\']*nav[^"\']*["\']', content, re.IGNORECASE))
has_nav_fixed = bool(re.search(r'<nav[^>]*position:\s*(fixed|sticky)', content, re.IGNORECASE))
has_div_header = bool(re.search(r'<div[^>]*class=["\'][^"\']*header[^"\']*["\']', content, re.IGNORECASE))
has_fixed_div = bool(re.search(r'position:\s*fixed[^;]*top:\s*0', content, re.IGNORECASE))

print('header_tag:', has_header_tag)
print('nav_class_nav:', has_nav_class_nav)
print('nav_fixed:', has_nav_fixed)
print('div_header:', has_div_header)
print('fixed_div:', has_fixed_div)

m = re.search(r'<nav[^>]*>', content, re.IGNORECASE)
if m:
    print('NAV TAG:', m.group(0))
else:
    print('NO NAV TAG')

# Check position:fixed in CSS
m2 = re.search(r'position:\s*fixed', content, re.IGNORECASE)
if m2:
    idx = m2.start()
    print('Fixed pos context:', content[idx-50:idx+100])
