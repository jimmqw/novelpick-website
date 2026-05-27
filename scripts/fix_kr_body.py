"""Fix Keep Reading sections that were only added to CSS but not HTML body."""
import os
import re

ws = r"C:\Users\Administrator\.openclaw\workspace"

# Novelpick related articles
KEEP_READING_ITEMS = {
    "best-cultivation-novels-2026.html": [
        ("Top LitRPG Web Novels 2026", "/top-litrpg-web-novels-2026.html"),
        ("Best Reincarnation Web Novels 2026", "/best-reincarnation-web-novels-2026.html"),
        ("Best Time Travel Web Novels 2026", "/best-time-travel-web-novels-2026.html"),
        ("Top Romance Web Novels 2026", "/top-romance-web-novels-2026.html"),
        ("Books Like Solo Leveling", "/books-like-solo-leveling.html"),
    ],
    "top-litrpg-web-novels-2026.html": [
        ("Best Cultivation Novels 2026", "/best-cultivation-novels-2026.html"),
        ("Best Reincarnation Web Novels 2026", "/best-reincarnation-web-novels-2026.html"),
        ("Best Time Travel Web Novels 2026", "/best-time-travel-web-novels-2026.html"),
        ("Top Romance Web Novels 2026", "/top-romance-web-novels-2026.html"),
        ("Books Like Solo Leveling", "/books-like-solo-leveling.html"),
    ],
    "best-time-travel-web-novels-2026.html": [
        ("Best Cultivation Novels 2026", "/best-cultivation-novels-2026.html"),
        ("Top LitRPG Web Novels 2026", "/top-litrpg-web-novels-2026.html"),
        ("Best Reincarnation Web Novels 2026", "/best-reincarnation-web-novels-2026.html"),
        ("Top Romance Web Novels 2026", "/top-romance-web-novels-2026.html"),
        ("Books Like Solo Leveling", "/books-like-solo-leveling.html"),
    ],
}

KR_HTML = """<div class="keep-reading-section">
<h3>Keep Reading</h3>
<div class="keep-reading-grid">
{items}
</div>
</div>
"""

def make_kr(name):
    items = []
    for title, link in KEEP_READING_ITEMS[name]:
        items.append('<a href="{link}" class="keep-reading-item"><span class="kr-title">{title}</span></a>'.format(link=link, title=title))
    return KR_HTML.format(items="\n".join(items))

for filename in ["best-cultivation-novels-2026.html", "top-litrpg-web-novels-2026.html", "best-time-travel-web-novels-2026.html"]:
    fp = os.path.join(ws, "novelpick.top", filename)
    with open(fp, "r", encoding="utf-8") as f:
        c = f.read()
    
    original = c
    
    # Only check body (after </style>) for KR div
    style_end = c.find("</style>") + 8
    body = c[style_end:]
    
    if "keep-reading-section" in body:
        print(f"{filename}: Keep Reading already in body, skipping")
        continue
    
    # Find prev-next element - could be <div class="prev-next"> or <nav class="prev-next">
    pn_idx = c.find('<nav class="prev-next"')
    if pn_idx < 0:
        pn_idx = c.find('<div class="prev-next"')
    
    if pn_idx < 0:
        print(f"{filename}: ERROR - cannot find prev-next element")
        continue
    
    kr_html = make_kr(filename)
    
    # Insert KR before prev-next (at pn_idx)
    c = c[:pn_idx] + "\n" + kr_html + "\n" + c[pn_idx:]
    
    # Save
    with open(fp, "w", encoding="utf-8") as f:
        f.write(c)
    
    print(f"{filename}: inserted Keep Reading before prev-next ({len(c)} bytes, was {len(original)})")
    
    # Verify div balance
    opens = len(re.findall(r'<div\b', c))
    closes = len(re.findall(r'</div>', c))
    print(f"  div balance: {opens} opens, {closes} closes = {opens - closes}")
    print(f"  KR in body now: {'keep-reading-section' in c[style_end:]}")
