import re
import os

# Check actual morai article
sample = r'C:\Users\Administrator\github\morai-website\best-ai-agents-2026.html'
if os.path.exists(sample):
    content = open(sample, encoding='utf-8').read()
    
    # Find article-body region
    ab_start = content.find('article-body')
    if ab_start >= 0:
        # Count divs in a window after article-body
        region = content[ab_start:ab_start+10000]
        
        opens = region.count('<div')
        closes = region.count('</div>')
        print(f"article-body region: open divs={opens}, close divs={closes}, balance={opens-closes}")
        
        # Find the closing of article-body
        ab_end_tag = content.find('</div>', ab_start)
        if ab_end_tag >= 0:
            # Find the last meaningful close before sidebar
            after_ab = content[ab_start:ab_end_tag+6]
            last_div_close = after_ab.rfind('</div>')
            print(f"\nLast </div> in article-body region at offset {last_div_close}")
            print("Context after last div:", after_ab[last_div_close:last_div_close+200])
        else:
            print("\nNo closing </div> after article-body start")
            print("Last 500 chars of article-body region:")
            print(region[-500:])
    else:
        print("No article-body found")
        idx = content.find('article-layout')
        print("article-layout at:", idx)
else:
    print("File not found:", sample)
