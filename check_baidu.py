# -*- coding: utf-8 -*-
import re

# Check a few files that show "baidu missing" to see what they actually have
files_baidu = [
    (r"C:\Users\Administrator\github\novelpick-website\best-action-fantasy-web-novels-2026.html", "novelpick - baidu missing"),
    (r"C:\Users\Administrator\github\novelpick-website\best-reincarnation-web-novels-2026.html", "novelpick - only baidu missing"),
    (r"C:\Users\Administrator\github\morai-website\claude-code-vs-cursor-vs-github-copilot-2026.html", "morai - baidu missing"),
]

for fpath, desc in files_baidu:
    print(f"\n=== {fpath.split('\\')[-1]} ({desc}) ===")
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        c = f.read()
    
    # baidu
    baidu = re.search(r'hm\.baidu\.com', c)
    print(f"hm.baidu.com: {baidu is not None}")
    
    # also check for _hmt
    hmt = re.search(r'_hmt', c)
    print(f"_hmt: {hmt is not None}")
    
    # check body text
    body = re.search(r'<body[^>]*>(.*?)</body>', c, re.DOTALL | re.IGNORECASE)
    if body:
        text = re.sub(r'<[^>]+>', '', body.group(1))
        text = re.sub(r'\s+', '', text)
        print(f"body text: {len(text)} chars")

# Now check files that PASSED baidu check
files_ok = [
    (r"C:\Users\Administrator\github\novelpick-website\fantasy.html", "novelpick fantasy - OK"),
    (r"C:\Users\Administrator\github\novelpick-website\index.html", "novelpick index - FAIL"),
]

print("\n--- Comparing with files that passed ---")
for fpath, desc in files_ok:
    print(f"\n=== {fpath.split('\\')[-1]} ({desc}) ===")
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        c = f.read()
    baidu = re.search(r'hm\.baidu\.com', c)
    print(f"hm.baidu.com: {baidu is not None}")
    hmt = re.search(r'_hmt', c)
    print(f"_hmt: {hmt is not None}")
