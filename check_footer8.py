# -*- coding: utf-8 -*-
import re

files = [
    r"C:\Users\Administrator\github\morai-website\best-ai-image-editors-2026.html",
]

for fpath in files:
    with open(fpath, 'rb') as f:
        raw = f.read()
    
    # Find all occurrences of bytes that look like copyright or year
    # Search for '2026' and show bytes before
    pos = 0
    while True:
        pos = raw.find(b'2026', pos)
        if pos < 0:
            break
        before = raw[max(0,pos-30):pos]
        print(f"Before 2026 at {pos}: {before.hex()} | {before}")
        pos += 1
    
    # Also search for C2 A9 (UTF-8 (c))
    if b'\xc2\xa9' in raw:
        pos = raw.find(b'\xc2\xa9')
        print(f"\nFound C2 A9 (UTF-8 (c)) at {pos}")
        print(f"Context: {raw[max(0,pos-10):pos+20]}")
    else:
        print("\nNo C2 A9 found in file")
    
    # Check what character is actually before "2026" in the footer
    footer_start = raw.find(b'<footer')
    if footer_start >= 0:
        footer_region = raw[footer_start:footer_start+500]
        idx = footer_region.find(b'2026')
        if idx > 0:
            char_bytes = footer_region[idx-5:idx]
            print(f"\nBytes before 2026 in footer: {char_bytes.hex()}")
            # Interpret as UTF-8
            for i in range(1, 5):
                try:
                    candidate = footer_region[idx-i:idx]
                    text = candidate.decode('utf-8')
                    print(f"  Decoded {i} bytes: {candidate.hex()} -> '{text}'")
                except:
                    pass
