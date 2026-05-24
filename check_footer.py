# -*- coding: utf-8 -*-
import re

# Check some files flagged for "footer无版权信息"
files = [
    (r"C:\Users\Administrator\github\morai-website\best-ai-image-editors-2026.html", "morai - footer无版权"),
    (r"C:\Users\Administrator\github\fateandmethod-site\ziwei-combinations.html", "fate - footer无版权"),
    (r"C:\Users\Administrator\github\fateandmethod-site\daily-wisdom-car-sickness.html", "fate - footer无版权"),
]

for fpath, desc in files:
    print(f"\n=== {fpath.split('\\')[-1]} ({desc}) ===")
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        c = f.read()
    
    ft = re.search(r'<footer[^>]*>(.*?)</footer>', c, re.DOTALL | re.IGNORECASE)
    print(f"footer found: {ft is not None}")
    if ft:
        text = re.sub(r'<[^>]+>', '', ft.group(1))
        text = re.sub(r'\s+', '', text)
        print(f"footer text: {text[:200]}")
        cp = re.search(r'©|copyright|&copy;|版权所有', ft.group(0), re.IGNORECASE)
        print(f"copyright in footer: {cp is not None}")

# Also check novelpick for footer
print("\n--- novelpick index ---")
fpath = r"C:\Users\Administrator\github\novelpick-website\index.html"
with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
    c = f.read()
ft = re.search(r'<footer[^>]*>(.*?)</footer>', c, re.DOTALL | re.IGNORECASE)
print(f"footer found: {ft is not None}")
if ft:
    text = re.sub(r'<[^>]+>', '', ft.group(1))
    text = re.sub(r'\s+', '', text)
    print(f"footer text: {text[:200]}")
    cp = re.search(r'©|copyright|&copy;|版权所有', ft.group(0), re.IGNORECASE)
    print(f"copyright in footer: {cp is not None}")
