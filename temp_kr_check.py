import os
import re

site = r'C:\Users\Administrator\github\fateandmethod-site'
files = ['bazi.html', 'liuyao.html', 'xuankong.html', 'meihua.html', 'five-elements-complete-guide.html']
for f in files:
    path = os.path.join(site, f)
    content = open(path, 'r', encoding='utf-8', errors='replace').read()
    
    # Find related section
    rel = re.search(r'class="([^"]*related[^"]*)"', content, re.IGNORECASE)
    also_check = re.search(r'class="([^"]*[Rr]elated[^"]*)"', content)
    h3 = re.search(r'<h3>([^<]*[Rr]elated[^<]*)</h3>', content)
    section = re.search(r'<section[^>]*class="([^"]*)"', content)
    
    print(f'\n{f}:')
    if rel:
        print(f'  Related class: {rel.group(1)}')
    if also_check:
        print(f'  Also matched: {also_check.group(1)}')
    if h3:
        print(f'  H3 related: {h3.group(1)}')
    if section:
        all_sections = re.findall(r'<section[^>]*class="([^"]*)"', content)
        print(f'  All sections: {all_sections}')
    if not rel and not also_check and not h3:
        print('  NO KR SECTION FOUND')
    
    # Check for the specific "Explore Other Systems" section
    if 'Explore Other Systems' in content:
        idx = content.find('Explore Other Systems')
        print(f'  Found "Explore Other Systems" at {idx}')
        print(f'  Context: {repr(content[idx-50:idx+100])}')
