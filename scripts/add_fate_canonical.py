"""Add missing canonical tags to fateandmethod pages"""
import re
import os

FATE_PATH = r'C:\Users\Administrator\github\fateandmethod-site'

PAGES = {
    'bazi.html': 'https://fateandmethod.com/bazi.html',
    'xiaoliuren.html': 'https://fateandmethod.com/xiaoliuren.html',
    'xuankong.html': 'https://fateandmethod.com/xuankong.html',
    'taiyi.html': 'https://fateandmethod.com/taiyi.html',
    'daily-wisdom.html': 'https://fateandmethod.com/daily-wisdom.html',
}

CANONICAL_TAG = '<link rel="canonical" href="{}">'

fixed = 0
for fname, can_url in PAGES.items():
    path = os.path.join(FATE_PATH, fname)
    if not os.path.exists(path):
        print(f'{fname}: NOT FOUND')
        continue
    
    with open(path, encoding='utf-8') as f:
        content = f.read()
    
    # Check for actual canonical tag (not just the word)
    has_canonical_tag = bool(re.search(r'<link rel=["\']canonical["\']', content))
    
    if has_canonical_tag:
        print(f'{fname}: already has canonical')
        continue
    
    # Insert after og:title tag
    can_tag = CANONICAL_TAG.format(can_url)
    og_match = re.search(r'<meta property="og:title" content="[^"]+">', content)
    if og_match:
        new_content = content[:og_match.end()] + '\n    ' + can_tag + content[og_match.end():]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'{fname}: added canonical')
        fixed += 1
    else:
        print(f'{fname}: og:title not found, cannot insert canonical')
        # Try inserting after description
        desc_match = re.search(r'<meta name="description" content="[^"]+">', content)
        if desc_match:
            new_content = content[:desc_match.end()] + '\n    ' + can_tag + content[desc_match.end():]
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'{fname}: added canonical after description')
            fixed += 1

print(f'\nTotal canonical tags added: {fixed}')
