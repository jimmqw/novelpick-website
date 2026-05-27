# -*- coding: utf-8 -*-
import re

# Check why copyright detection fails
files = [
    (r"C:\Users\Administrator\github\morai-website\best-ai-image-editors-2026.html", "morai"),
    (r"C:\Users\Administrator\github\fateandmethod-site\ziwei-combinations.html", "fate"),
]

for fpath, desc in files:
    print(f"\n=== {fpath.split('\\')[-1]} ({desc}) ===")
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        c = f.read()
    
    ft = re.search(r'<footer[^>]*>(.*?)</footer>', c, re.DOTALL | re.IGNORECASE)
    if ft:
        footer_html = ft.group(0)
        # Try to find copyright symbol in raw HTML
        cp1 = re.search(r'©', footer_html)
        cp2 = re.search(r'&copy;', footer_html)
        cp3 = re.search(r'copyright', footer_html, re.IGNORECASE)
        cp4 = re.search(r'版权所有', footer_html)
        print(f"Found '©' in footer HTML: {cp1 is not None}")
        print(f"Found '&copy;' in footer HTML: {cp2 is not None}")
        print(f"Found 'copyright' in footer HTML: {cp3 is not None}")
        print(f"Found '版权所有' in footer HTML: {cp4 is not None}")
        
        # Print raw bytes around copyright
        if cp1:
            pos = cp1.start()
            print(f"Context: ...{footer_html[max(0,pos-10):pos+20]}...")
