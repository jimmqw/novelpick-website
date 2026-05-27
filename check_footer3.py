# -*- coding: utf-8 -*-
import re

files = [
    (r"C:\Users\Administrator\github\morai-website\best-ai-image-editors-2026.html", "morai"),
    (r"C:\Users\Administrator\github\fateandmethod-site\ziwei-combinations.html", "fate"),
]

results = []
for fpath, desc in files:
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        c = f.read()
    
    ft = re.search(r'<footer[^>]*>(.*?)</footer>', c, re.DOTALL | re.IGNORECASE)
    if ft:
        footer_html = ft.group(0)
        cp1 = u'\u00a9' in footer_html  # (c)
        cp2 = '&copy;' in footer_html.lower()
        cp3 = re.search(r'copyright', footer_html, re.IGNORECASE) is not None
        cp4 = u'\u7248\u6743\u6240\u6709' in footer_html  # 版权所有
        results.append(f"File: {fpath.split('\\')[-1]} ({desc})")
        results.append(f"  Found (c): {cp1}")
        results.append(f"  Found &copy;: {cp2}")
        results.append(f"  Found copyright: {cp3}")
        results.append(f"  Found 版权所有: {cp4}")

with open(r"C:\Users\Administrator\.openclaw\workspace\footer_check.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(results))
print("Done")
