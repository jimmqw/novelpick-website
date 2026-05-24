# -*- coding: utf-8 -*-
import re

files = [
    r"C:\Users\Administrator\github\morai-website\best-ai-image-editors-2026.html",
    r"C:\Users\Administrator\github\fateandmethod-site\ziwei-combinations.html",
]

for fpath in files:
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        c = f.read()
    
    ft = re.search(r'<footer[^>]*>(.*?)</footer>', c, re.DOTALL | re.IGNORECASE)
    if ft:
        footer_html = ft.group(0)
        # Check for HTML-encoded copyright
        cp169 = '&#169;' in footer_html
        cpXa9 = '&#xA9;' in footer_html or '&#xa9;' in footer_html
        print(f"File: {fpath.split('\\')[-1]}")
        print(f"  &#169; found: {cp169}")
        print(f"  &#xA9; found: {cpXa9}")
        
        # Find position of "2026" to see what comes before
        pos = footer_html.find('2026')
        if pos > 0:
            print(f"  Before 2026: {repr(footer_html[max(0,pos-20):pos])}")
