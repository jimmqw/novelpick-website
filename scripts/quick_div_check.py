import re

path = r'C:\Users\Administrator\github\novelpick-website\best-solo-leveling-novels.html'
c = open(path, encoding='utf-8').read()
m = re.search(r'<div[^>]*class=["\'][^"\']*article-body[^"\']*["\'][^>]*>', c, re.I)
if m:
    ab_start = m.end()
    depth = 1
    pos = ab_start
    while pos < len(c) and depth > 0:
        no = c.find('<div', pos)
        nc = c.find('</div>', pos)
        if nc < 0:
            break
        if no >= 0 and no < nc:
            depth += 1
            pos = no + 5
        else:
            depth -= 1
            if depth == 0:
                break
            pos = nc + 6
    region = c[m.start():nc+6]
    opens = region.count('<div')
    closes = region.count('</div>')
    print(f'open={opens} close={closes} balance={opens-closes}')
    text = re.sub(r'<[^>]+>', '', region)
    print(f'article-body region: {len(region)} chars, text: {len(text.strip())} chars')
else:
    print('no article-body found')
