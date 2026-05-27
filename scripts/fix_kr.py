"""Fix files that have KR CSS but not KR HTML div in body."""
import re, os

ws = r"C:\Users\Administrator\.openclaw\workspace"

keep_reading_items = {
    "bazi-ten-gods-guide.html": [
        ("Ba Zi Complete Guide", "/bazi.html"),
        ("Chinese Zodiac Signs 2026 Guide", "/chinese-zodiac-signs-2026-guide.html"),
        ("Chinese Numerology Complete Guide", "/chinese-numerology-complete-guide.html"),
        ("Ziwei 12 Palaces Guide", "/ziwei-12-palaces-guide.html"),
    ],
    "feng-shui-2026-year-guide.html": [
        ("Feng Shui Spring 2026", "/feng-shui-spring-2026.html"),
        ("Chinese Zodiac 2026 Fire Snake Horoscope", "/chinese-zodiac-2026-fire-snake-horoscope.html"),
        ("Chinese Zodiac Signs 2026 Guide", "/chinese-zodiac-signs-2026-guide.html"),
        ("Chinese Numerology Complete Guide", "/chinese-numerology-complete-guide.html"),
    ],
    "chinese-zodiac-compatibility-guide.html": [
        ("Chinese Zodiac Signs 2026 Guide", "/chinese-zodiac-signs-2026-guide.html"),
        ("Chinese Zodiac 2026 Fire Snake Horoscope", "/chinese-zodiac-2026-fire-snake-horoscope.html"),
        ("Ba Zi Complete Guide", "/bazi.html"),
        ("Feng Shui 2026 Year Guide", "/feng-shui-2026-year-guide.html"),
    ],
}

KEEP_READING = """
<div class="keep-reading-section">
<h3>Continue Reading</h3>
<div class="keep-reading-grid">
{items}
</div>
</div>
"""

def make_keep_reading(name):
    items = []
    for title, link in keep_reading_items[name]:
        items.append('<a href="{link}" class="keep-reading-item"><span class="kr-title">{title}</span></a>'.format(link=link, title=title))
    return KEEP_READING.format(items="\n".join(items))

for filename in ["bazi-ten-gods-guide.html", "feng-shui-2026-year-guide.html", "chinese-zodiac-compatibility-guide.html"]:
    fp = os.path.join(ws, "fateandmethod.com", filename)
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()
    
    original = c
    kr_html = make_keep_reading(filename)
    
    if filename == "chinese-zodiac-compatibility-guide.html":
        # This file uses unquoted attributes
        # Find the CTA box and insert KR before prev-next (which is OUTSIDE the layout div!)
        # Structure: <div class=cta-box>...</div></div></main>
        # Insert KR before prev-next
        # Actually, this file has prev-next outside the layout:
        # </aside></div><div class=prev-next>
        # I'll insert before the </div></main> (closing layout and main)
        # Actually I see: <div class=cta-box>...</div></div></main><aside class=sidebar>...</aside></div><div class=prev-next>
        # So </div> </main> closes layout and main
        
        # Let's insert after CTA box end, before the closing </div></main>
        insert_point = c.rfind("</div></main>")
        if insert_point > 0:
            # Check if KR already exists
            if "keep-reading-section" in c[insert_point - 500:insert_point + 100]:
                print(f"{filename}: KR already exists, skipping")
                continue
            c = c[:insert_point] + "\n" + kr_html + "\n" + c[insert_point:]
            print(f"{filename}: inserted KR before closing div/main")
    else:
        # These use quoted attributes
        # Find position to insert: before </div></main> (close of main/article-body)
        # Or before <div class=prev-next>
        # Check structure
        ab_close = c.find("</div></main>")
        if ab_close > 0 and "keep-reading-section" not in c[:ab_close]:
            c = c[:ab_close] + "\n" + kr_html + "\n" + c[ab_close:]
            print(f"{filename}: inserted KR before </div></main>")
        elif "keep-reading-section" not in c:
            # Try alternative: insert before <div class=prev-next>
            pn_idx = c.find('<div class=prev-next')
            if pn_idx > 0:
                c = c[:pn_idx] + "\n" + kr_html + "\n" + c[pn_idx:]
                print(f"{filename}: inserted KR before prev-next")
    if c != original:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"{filename}: saved ({len(c)} bytes, was {len(original)})")
    else:
        print(f"{filename}: no changes needed")
