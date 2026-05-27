import re
import os

ws = r"C:\Users\Administrator\.openclaw\workspace"

for name in ["best-cultivation-novels-2026", "top-litrpg-web-novels-2026", "best-time-travel-web-novels-2026"]:
    fp = os.path.join(ws, "novelpick.top", name + ".html")
    with open(fp, "r", encoding="utf-8") as f:
        c = f.read()
    
    # Find the prev-next section
    nav_style = c.find('<nav class="prev-next"')
    div_style = c.find('<div class="prev-next"')
    
    pn_idx = max(nav_style, div_style)
    pn_tag = "nav" if nav_style >= 0 else "div" if div_style >= 0 else "unknown"
    
    if pn_idx < 0:
        # fallback: find unquoted version
        pn_idx = c.find("class=prev-next")
        pn_tag = "unquoted"
    
    # Show context
    before = c[max(0, pn_idx-200):pn_idx]
    print(f"\n=== {name}.html ===")
    print(f"prev-next at {pn_idx}, tag=<{pn_tag}>")
    print(f"Before prev-next:\n{before[-120:]}")
    print(f"\nprev-next line: {c[pn_idx:pn_idx+50]}")
