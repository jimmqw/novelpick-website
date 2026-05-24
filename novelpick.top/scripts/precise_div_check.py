import re

# Precise div balance check for article-body region
sample = r'C:\Users\Administrator\github\morai-website\best-ai-agents-2026.html'
content = open(sample, encoding='utf-8').read()

# Find article-body opening tag position
ab_match = re.search(r'<div[^>]*id=["\']?article-body["\']?[^>]*>', content, re.IGNORECASE)
if not ab_match:
    ab_match = re.search(r'<div[^>]*class=["\']?[^"\']*article-body[^"\']*["\'][^>]*>', content, re.IGNORECASE)

if ab_match:
    ab_start = ab_match.end()
    print(f"article-body starts at {ab_start}")
    print(f"Opening tag: {ab_match.group()}")
    
    # Now find the actual end of article-body (not just the first </div>)
    # We need to track nesting level
    depth = 1
    pos = ab_start
    last_div_open = -1
    last_div_close = -1
    
    while pos < len(content) and depth > 0:
        next_open = content.find('<div', pos)
        next_close = content.find('</div>', pos)
        
        if next_close < 0:
            print(f"ERROR: unmatched divs, depth={depth} at end")
            break
        
        if next_open >= 0 and next_open < next_close:
            depth += 1
            last_div_open = next_open
            pos = next_open + 5
        else:
            depth -= 1
            last_div_close = next_close
            if depth == 0:
                break
            pos = next_close + 6
    
    ab_end = last_div_close + 6  # include </div>
    print(f"article-body ends at {ab_end} (char {content[last_div_close-5:last_div_close+7]})")
    
    region = content[ab_start-1:last_div_close+6]
    print(f"\nRegion length: {len(region)} chars")
    
    # Count divs in region
    opens = region.count('<div')
    closes = region.count('</div>')
    print(f"open divs: {opens}, close divs: {closes}, balance: {opens-closes}")
    
    # Find where the imbalance occurs
    # Check what's near the end of the region
    print("\nLast 300 chars of article-body:")
    print(repr(region[-300:]))
    
    # Also find what comes AFTER article-body
    print("\nAfter article-body (next 200 chars):")
    print(repr(content[ab_end:ab_end+200]))
else:
    print("article-body not found")
