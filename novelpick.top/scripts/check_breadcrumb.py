# -*- coding: utf-8 -*-
import re

# Debug: check breadcrumb in novelpick articles
with open(r'C:\Users\Administrator\github\novelpick-website\best-solo-leveling-novels.html', 'r', encoding='utf-8') as f:
    c = f.read()

print("breadcrumb in content:", 'breadcrumb' in c.lower())
print("Has breadcrumb:", re.search(r'breadcrumb', c, re.IGNORECASE))

# Find the breadcrumb section
bc_match = re.search(r'breadcrumb.{0,200}', c, re.IGNORECASE | re.DOTALL)
if bc_match:
    print("Breadcrumb context:", bc_match.group(0)[:200])
print()

# Check morai article - does it have header?
with open(r'C:\Users\Administrator\github\morai-website\best-ai-coding-tools-2026.html', 'r', encoding='utf-8') as f:
    ma = f.read()
print("MORAI ARTICLE:")
print("<header:", '<header' in ma)
print("breadcrumb:", 'breadcrumb' in ma.lower())
print("footer:", '<footer' in ma)
print("article-body:", 'article-body' in ma)
print("og:title:", 'og:title' in ma)
print("hm.baidu:", 'hm.baidu' in ma)
print("canonical:", 'canonical' in ma)
print("has hero:", '.hero' in ma or 'class="hero"' in ma)
print()

# Check a fateandmethod article
with open(r'C:\Users\Administrator\github\fateandmethod-site\ziwei.html', 'r', encoding='utf-8') as f:
    fm = f.read()
print("FATEANDMETHOD ziwei.html:")
print("<header:", '<header' in fm)
print("breadcrumb:", 'breadcrumb' in fm.lower())
print("footer:", '<footer' in fm)
print("article-body:", 'article-body' in fm)
print("og:title:", 'og:title' in fm)
print("canonical:", 'canonical' in fm)
print("hm.baidu:", 'hm.baidu' in fm)
print("nav:", '<nav' in fm)
print()

# Check morai best-ai-design-tools specifically for header
with open(r'C:\Users\Administrator\github\morai-website\best-ai-design-tools-2026.html', 'r', encoding='utf-8') as f:
    md = f.read()
print("MORAI design-tools:")
print("<header:", '<header' in md)
print("breadcrumb:", 'breadcrumb' in md.lower())
print("footer:", '<footer' in md)
print("article-body:", 'article-body' in md)
print("og:title:", 'og:title' in md)
print("hm.baidu:", 'hm.baidu' in md)
print("canonical:", 'canonical' in md)
