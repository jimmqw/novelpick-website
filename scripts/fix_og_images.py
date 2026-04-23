import re, os

def fix_og_image(html_content, site_name):
    """Fix og:image URL to use correct og-image.png path."""
    correct_url = f'https://{site_name}/og-image.png'
    wrong_url = f'https://{site_name}/og-default.png'
    
    if wrong_url in html_content:
        new_content = html_content.replace(wrong_url, correct_url)
        return new_content, True
    return html_content, False

# Fix workspace files (the ones that had wrong og-default.png)
sites = {
    'morai.top': r'C:\Users\Administrator\.openclaw\workspace\morai.top',
    'novelpick.top': r'C:\Users\Administrator\.openclaw\workspace\novelpick.top',
}

for site_name, site_path in sites.items():
    count = 0
    for fname in os.listdir(site_path):
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(site_path, fname)
        try:
            content = open(fpath, encoding='utf-8', errors='ignore').read()
        except:
            continue
        
        new_content, was_fixed = fix_og_image(content, site_name)
        
        if was_fixed:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Fixed: {fname}')
            count += 1
    
    print(f'{site_name}: {count} files fixed')
