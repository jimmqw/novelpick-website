# -*- coding: utf-8 -*-
import re

files = [
    r"C:\Users\Administrator\github\morai-website\best-ai-image-editors-2026.html",
]

for fpath in files:
    # Read as binary first
    with open(fpath, 'rb') as f:
        raw = f.read()
    
    # Find footer
    footer_start = raw.find(b'<footer')
    footer_end = raw.find(b'</footer>')
    if footer_start >= 0 and footer_end >= 0:
        footer_raw = raw[footer_start:footer_end+9]
        # Find the position of 2026
        pos2026 = footer_raw.find(b'2026')
        if pos2026 > 0:
            before = footer_raw[max(0,pos2026-20):pos2026]
            print(f"Before 2026 (raw bytes): {before}")
            print(f"Before 2026 (hex): {before.hex()}")
            # Check for C2 A9 (UTF-8 encoding of ©)
            if b'\xc2\xa9' in footer_raw:
                print("Found UTF-8 © (C2 A9)")
            # Check for HTML entity
            if b'&#169;' in footer_raw.lower():
                print("Found &#169;")
            if b'&#xa9' in footer_raw.lower():
                print("Found &#xA9")
                
    # Now read as UTF-8 text
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    ft = re.search(r'<footer[^>]*>(.*?)</footer>', text, re.DOTALL | re.IGNORECASE)
    if ft:
        # Check for copyright in various forms
        cp_unicode = '\u00a9' in ft.group(0)  # literal ©
        cp_html_dec = '&#169;' in ft.group(0)
        cp_html_hex = '&#x' in ft.group(0).lower()
        cp_copy = 'copyright' in ft.group(0).lower()
        print(f"\nIn footer (UTF-8 text):")
        print(f"  Unicode ©: {cp_unicode}")
        print(f"  HTML decimal &#169;: {cp_html_dec}")
        print(f"  HTML hex &#x: {cp_html_hex}")
        print(f"  'copyright': {cp_copy}")
        
        # Print the footer text (no tags) around the year
        ft_text = re.sub(r'<[^>]+>', '', ft.group(1))
        idx = ft_text.find('2026')
        if idx >= 0:
            print(f"  Context around 2026: ...{ft_text[max(0,idx-20):idx+30]}...")
