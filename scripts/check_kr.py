import re, os

ws = r"C:\Users\Administrator\.openclaw\workspace"

fate_files = [
    "bazi-ten-gods-guide.html",
    "chinese-numerology-complete-guide.html", 
    "feng-shui-2026-year-guide.html",
    "chinese-zodiac-compatibility-guide.html",
]

for name in fate_files:
    fp = os.path.join(ws, "fateandmethod.com", name)
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # Find Keep Reading in body (after </style>)
    style_end = c.find("</style>")
    if style_end > 0:
        body_after_style = c[style_end+8:]
        kr_pos = body_after_style.find("keep-reading-section")
        has_kr_body = kr_pos > 0
        print(f"{name}:")
        print(f"  CSS has KR styles: {'keep-reading-section' in c[:style_end+8]}")
        print(f"  Body has KR div: {has_kr_body}")
        
        # Check article-body class format
        ab_quoted = 'class="article-body"' in c
        ab_unquoted = 'class=article-body' in c and 'class="article-body"' not in c
        print(f"  article-body class (quoted): {ab_quoted}")
        print(f"  article-body class (unquoted): {ab_unquoted}")
        
        # Check prev-next format
        pn_quoted = c.count('class="prev-next"')
        pn_unquoted = c.count('class=prev-next')
        print(f"  prev-next (quoted): {pn_quoted}")
        print(f"  prev-next (unquoted): {pn_unquoted}")
        
        if has_kr_body:
            # Show what's around it
            kr_start = style_end + 8 + kr_pos
            print(f"  KR context: ...{c[kr_start-30:kr_start+40]}...")
        print()
