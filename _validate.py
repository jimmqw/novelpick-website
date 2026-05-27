import re, sys, os

files = [
    r'C:\Users\Administrator\.openclaw\workspace\morai-website\best-ai-social-media-tools-2026.html',
    r'C:\Users\Administrator\.openclaw\workspace\novelpick-website\best-sci-fi-web-novels-2026.html',
    r'C:\Users\Administrator\.openclaw\workspace\fateandmethod-website\yin-yang-theory-guide.html',
]

for fp in files:
    if not os.path.exists(fp):
        print(f"MISSING: {os.path.basename(fp)}")
        continue
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()
    od = len(re.findall(r'<div\b', c))
    cd = len(re.findall(r'</div>', c))
    print(f"{os.path.basename(fp)}: div open={od} close={cd} balanced={od==cd} | html_end={'</html>' in c} | baidu={'hm.js' in c} | canonical={'canonical' in c} | size={len(c)}")
