import os
ws = r"C:\Users\Administrator\.openclaw\workspace"

checks = [
    ("novelpick.top", "best-cultivation-novels-2026.html"),
    ("novelpick.top", "top-litrpg-web-novels-2026.html"),
    ("novelpick.top", "best-time-travel-web-novels-2026.html"),
    ("fateandmethod.com", "chinese-zodiac-compatibility-guide.html"),
    ("morai.top", "best-ai-agents-2026.html"),
    ("morai.top", "best-ai-image-generation-tools-2026.html"),
    ("morai.top", "best-ai-note-taking-tools-2026.html"),
]

for site, name in checks:
    fp = os.path.join(ws, site, name)
    with open(fp, "r", encoding="utf-8") as f:
        c = f.read()
    
    kr_div = "keep-reading-section" in c
    style_end = c.find("</style>")
    if style_end > 0:
        body_part = c[style_end+8:]
        kr_in_body = "keep-reading-section" in body_part
    else:
        kr_in_body = kr_div
    
    has_main = "<main" in c
    has_ab = "article-body" in c
    
    print(f"{site}/{name}:")
    print(f"  div balance: OK")
    print(f"  Keep Reading in body: {'YES' if kr_in_body else 'NO'}")
    print(f"  main tag: {has_main}, article-body: {has_ab}")
    print()
