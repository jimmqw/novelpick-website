content = open(r'C:\Users\Administrator\github\fateandmethod-site\bazi.html', 'r', encoding='utf-8', errors='replace').read()

# Check if there's any keep reading / recommended section
for kw in ['keep reading', 'recommended', 'related articles', 'you might also like']:
    idx = content.lower().find(kw)
    if idx >= 0:
        print(f'Found "{kw}" at {idx}: {repr(content[idx-30:idx+60])}')

# Also check near end of article
footer = content.find('<footer')
print(f'Footer at: {footer}')
if footer > 0:
    print('Before footer:', repr(content[footer-200:footer]))