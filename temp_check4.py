import re

for fname in ['bazi.html', 'liuyao.html', 'xuankong.html']:
    content = open(rf'C:\Users\Administrator\github\fateandmethod-site\{fname}', 'r', encoding='utf-8').read()
    
    # Check what tag contains article content
    body_start = content.find('<body')
    if body_start < 0:
        print(f'{fname}: no body tag')
        continue
    
    # Find all div.main-content or similar main containers
    patterns = [
        (r'<div[^>]*class=["\'][^"\']*main[^"\']*["\'][^>]*>'),  # div with "main" in class
        (r'<div[^>]*class=["\'][^"\']*content[^"\']*["\'][^>]*>'),  # div with "content" in class
        (r'<main[^>]*>'),  # main tag
        (r'<article[^>]*>'),  # article tag
    ]
    
    matched = False
    for p_name, p in patterns:
        m = re.search(p, content[body_start:])
        if m:
            pos = body_start + m.start()
            snippet = content[pos:pos+100].strip()
            print(f'{fname}: matched {p_name} at {pos}: {snippet[:80]}')
            matched = True
            break
    if not matched:
        print(f'{fname}: NO MAIN CONTAINER FOUND')
        # Show first 300 chars of body
        print(content[body_start:body_start+300])