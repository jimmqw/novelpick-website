import re, os

workspace = r"C:\Users\Administrator\.openclaw\workspace"
files = [
    (r"morai.top\best-ai-agents-2026.html", "best-ai-agents-2026.html"),
    (r"morai.top\best-ai-image-generation-tools-2026.html", "best-ai-image-generation-tools-2026.html"),
    (r"morai.top\best-ai-note-taking-tools-2026.html", "best-ai-note-taking-tools-2026.html"),
    (r"novelpick.top\top-litrpg-web-novels-2026.html", "top-litrpg-web-novels-2026.html"),
    (r"fateandmethod.com\chinese-zodiac-compatibility-guide.html", "chinese-zodiac-compatibility-guide.html"),
]

for path_rel, name in files:
    fp = os.path.join(workspace, path_rel)
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    total_opens = len(re.findall(r'<div\b', content))
    total_closes = len(re.findall(r'</div>', content))
    print(f"\n=== {name} ===")
    print(f"File balance: {total_opens} opens, {total_closes} closes => {total_opens - total_closes}")
    
    # Find article-body
    m = re.search(r'class="[^"]*article-body[^"]*"', content)
    if m:
        div_start = content.rfind('<div', 0, m.start())
        # Track div depth
        depth = 0
        i = div_start
        while True:
            so = content.find('<div', i)
            sc = content.find('</div>', i)
            if sc == -1:
                break
            if so != -1 and so < sc:
                depth += 1
                i = so + 4
            else:
                depth -= 1
                if depth == 0:
                    end_pos = sc + 6
                    print(f"article-body region: {div_start}-{end_pos}, "
                          f"closes at line {content[:end_pos].count(chr(10))+1}")
                    # Now check balance within region
                    region = content[div_start:end_pos]
                    r_opens = len(re.findall(r'<div\b', region))
                    r_closes = len(re.findall(r'</div>', region))
                    print(f"Region balance: {r_opens} opens, {r_closes} closes => {r_opens - r_closes}")
                    # Number of article-body div opens = 1 (the outer one)
                    print(f"Expected: 1 (the article-body div itself)")
                    break
                i = sc + 6
    else:
        print("No article-body class found!")
        
    # Show last 600 chars to check structure
    print(f"Last 600 chars:")
    print(repr(content[-600:]))
