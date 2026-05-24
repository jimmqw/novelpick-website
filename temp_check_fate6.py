import re

# Check fateandmethod files for div imbalance root cause
files = {
    'chinese-zodiac-personality-traits.html': r'C:\Users\Administrator\github\fateandmethod-site\chinese-zodiac-personality-traits.html',
    'chinese-zodiac-compatibility-guide.html': r'C:\Users\Administrator\github\fateandmethod-site\chinese-zodiac-compatibility-guide.html',
    'daily-wisdom.html': r'C:\Users\Administrator\github\fateandmethod-site\daily-wisdom.html',
}

for name, fpath in files.items():
    content = open(fpath, 'r', encoding='utf-8', errors='replace').read()
    
    # Count divs in whole file
    opens = content.count('<div ')
    closes = content.count('</div>')
    diff = opens - closes
    
    # Find article content boundaries
    main_pos = content.find('<main>')
    footer_pos = content.find('<footer')
    
    if main_pos < 0:
        print(f'\n{name}: NO <main> tag! diff={diff}')
        continue
    
    segment = content[main_pos:footer_pos]
    seg_opens = segment.count('<div ')
    seg_closes = segment.count('</div>')
    seg_diff = seg_opens - seg_closes
    
    before_diff = (content[:main_pos].count('<div ') - content[:main_pos].count('</div>'))
    
    print(f'\n{name}: overall diff={diff}, in-main diff={seg_diff}, before-main diff={before_diff}')
    
    # Find the spurious </div>
    # Look for extra </div> in segment
    if seg_diff < 0:
        # More closes than opens = extra </div>
        # Find where by checking the last </div> before footer
        last_div_before_footer = content.rfind('</div>', 0, footer_pos)
        # Check what follows
        print(f'  Last </div> at {last_div_before_footer}: {repr(content[last_div_before_footer-30:last_div_before_footer+20])}')
        # Check if this is actually closing the main tag
        after = content[last_div_before_footer+6:footer_pos].strip()
        print(f'  After last </div>: {repr(after[:60])}')