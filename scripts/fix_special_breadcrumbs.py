import re
import os

# Fix best-apocalypse-survival-web-novels.html - uses article-layout structure
path1 = r'C:\Users\Administrator\github\novelpick-website\best-apocalypse-survival-web-novels.html'
c1 = open(path1, encoding='utf-8').read()

# Pattern: <div class="article-header"> comes right after <div class="article-main">
# Insert breadcrumb before article-header
bc1 = '<div class="breadcrumb"><a href="/">Home</a> / <a href="/fantasy.html">Apocalypse & Survival</a></div>'
# After article-main opening, before article-header
pat1 = re.compile(r'(<div class="article-main">)\s*(<div class="article-header">)', re.DOTALL)
if pat1.search(c1):
    c1_new = pat1.sub(r'\1\n        ' + bc1 + r'\n        \2', c1)
    open(path1, 'w', encoding='utf-8').write(c1_new)
    print('Fixed: best-apocalypse-survival-web-novels.html')
else:
    print('ERROR: pattern not found in best-apocalypse-survival-web-novels.html')

# Fix best-time-loop-web-novels-2026.html - uses article-header-box
path2 = r'C:\Users\Administrator\github\novelpick-website\best-time-loop-web-novels-2026.html'
c2 = open(path2, encoding='utf-8').read()

bc2 = '<div class="breadcrumb"><a href="/">Home</a> / <a href="/scifi.html">Time Loop</a></div>'
pat2 = re.compile(r'(<div class="article-body">)\s*(<div class="article-header-box">)', re.DOTALL)
if pat2.search(c2):
    c2_new = pat2.sub(r'\1\n    ' + bc2 + r'\n    \2', c2)
    open(path2, 'w', encoding='utf-8').write(c2_new)
    print('Fixed: best-time-loop-web-novels-2026.html')
else:
    print('ERROR: pattern not found in best-time-loop-web-novels-2026.html')
