# -*- coding: utf-8 -*-
import re

files = [
    r"C:\Users\Administrator\github\morai-website\best-ai-image-editors-2026.html",
    r"C:\Users\Administrator\github\fateandmethod-site\ziwei-combinations.html",
    r"C:\Users\Administrator\github\fateandmethod-site\daily-wisdom-car-sickness.html",
    r"C:\Users\Administrator\github\morai-website\ai-comparisons.html",
    r"C:\Users\Administrator\github\fateandmethod-site\index.html",
]

for fpath in files:
    with open(fpath, 'rb') as f:
        raw = f.read()
    
    footer_start = raw.find(b'<footer')
    footer_end = raw.find(b'</footer>')
    if footer_start >= 0 and footer_end >= 0:
        footer_raw = raw[footer_start:footer_end+9]
        # decode just the footer portion
        try:
            footer_text = footer_raw.decode('utf-8')
        except:
            footer_text = footer_raw.decode('utf-8', errors='replace')
        
        # Strip HTML
        footer_stripped = re.sub(r'<[^>]+>', '', footer_text)
        footer_stripped = re.sub(r'\s+', ' ', footer_stripped).strip()
        print(f"File: {fpath.split('\\')[-1]}")
        print(f"  Footer (stripped): {footer_stripped[:200]}")
        
        # Check for copyright patterns
        has_copy_symbol = u'\u00a9' in footer_text  # (c)
        has_copy_html = '&#169;' in footer_text or '&#xA9' in footer_text or '&#xa9' in footer_text
        has_banquan = u'\u7248\u6743' in footer_text  # 版权
        has_banquan_suoyou = u'\u7248\u6743\u6240\u6709' in footer_text  # 版权所有
        has_copyright_word = 'copyright' in footer_text.lower()
        print(f"  Has (c) symbol: {has_copy_symbol}")
        print(f"  Has &#169;: {has_copy_html}")
        print(f"  Has 版权: {has_banquan}")
        print(f"  Has 版权所有: {has_banquan_suoyou}")
        print(f"  Has copyright word: {has_copyright_word}")
        print()
