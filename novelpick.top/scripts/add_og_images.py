import re, os

def add_og_image(html_content, site_name, article_title):
    """Add og:image tag to HTML if missing."""
    og_url = f'https://{site_name}/og-image.png'
    
    # Check if og:image already exists
    if 'og:image' in html_content:
        return html_content, False, 'already present'
    
    # Find the og:description tag and add og:image after it
    # Pattern: <meta property="og:description" content="...">
    pattern = r'(<meta property="og:description" content="[^"]+"\s*/?>)'
    replacement = rf'\1\n<meta property="og:image" content="{og_url}">'
    
    new_content = re.sub(pattern, replacement, html_content, count=1)
    
    if new_content == html_content:
        # Try og:url
        pattern2 = r'(<meta property="og:url" content="[^"]+"\s*/?>)'
        replacement2 = rf'\1\n<meta property="og:image" content="{og_url}">'
        new_content = re.sub(pattern2, replacement2, html_content, count=1)
    
    if new_content == html_content:
        return html_content, False, 'no anchor found'
    
    return new_content, True, 'added'

def process_site(site_name, site_path):
    count = 0
    modified = []
    for fname in os.listdir(site_path):
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(site_path, fname)
        try:
            content = open(fpath, encoding='utf-8', errors='ignore').read()
        except:
            continue
        
        new_content, was_added, status = add_og_image(content, site_name, fname)
        
        if was_added:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            modified.append(fname)
            count += 1
    
    return count, modified

morai_count, morai_files = process_site('morai.top', r'C:\Users\Administrator\github\morai-site')
print(f'morai.top: {morai_count} files updated')

novelpick_count, novelpick_files = process_site('novelpick.top', r'C:\Users\Administrator\github\novelpick-site')
print(f'novelpick.top: {novelpick_count} files updated')

fate_count, fate_files = process_site('fateandmethod.com', r'C:\Users\Administrator\github\fateandmethod-site')
print(f'fateandmethod.com: {fate_count} files updated')

print(f'\nTotal: {morai_count + novelpick_count + fate_count} files')
