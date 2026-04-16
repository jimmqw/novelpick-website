import re
import os

# Fix best-apocalypse-survival-web-novels.html
# Structure: article-layout > article-main > article-header (then content starts, no article-body)
path1 = r'C:\Users\Administrator\github\novelpick-website\best-apocalypse-survival-web-novels.html'
c1 = open(path1, encoding='utf-8').read()

# Insert breadcrumb right after </div> that closes article-header
bc1 = '<div class="breadcrumb"><a href="/">Home</a> / <a href="/fantasy.html">Apocalypse & Survival</a></div>'
# Find the article-header close, then insert after it
# The article-header closes with </div> and content starts immediately
# Use the specific pattern: article-header div closing followed by whitespace/newline
pat1 = re.compile(r'(<div class="article-header">.*?</div>)\s*(\n\s*<div)', re.DOTALL)
if pat1.search(c1):
    c1_new = pat1.sub(r'\1\n        ' + bc1 + r'\n    \2', c1)
    open(path1, 'w', encoding='utf-8').write(c1_new)
    print('Fixed: best-apocalypse-survival-web-novels.html')
else:
    # Try simpler approach - just after article-header closing div
    idx = c1.find('<div class="article-header">')
    if idx >= 0:
        # Find the </div> that closes this specific div
        depth = 1
        pos = idx + len('<div class="article-header">')
        while depth > 0 and pos < len(c1):
            no = c1.find('<div', pos)
            nc = c1.find('</div>', pos)
            if nc < 0:
                break
            if no >= 0 and no < nc:
                depth += 1
                pos = no + 5
            else:
                depth -= 1
                if depth == 0:
                    # Insert after this </div>
                    c1_new = c1[:nc+6] + '\n        ' + bc1 + c1[nc+6:]
                    open(path1, 'w', encoding='utf-8').write(c1_new)
                    print('Fixed: best-apocalypse-survival-web-novels.html (depth method)')
                    break
                pos = nc + 6
    else:
        print('ERROR: article-header not found in best-apocalypse-survival-web-novels.html')

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
