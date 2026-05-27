import re

files = [
    r"C:\Users\Administrator\.openclaw\workspace\morai.top\best-ai-agents-2026.html",
    r"C:\Users\Administrator\.openclaw\workspace\morai.top\best-ai-image-generation-tools-2026.html",
    r"C:\Users\Administrator\.openclaw\workspace\morai.top\best-ai-note-taking-tools-2026.html",
    r"C:\Users\Administrator\.openclaw\workspace\novelpick.top\best-cultivation-novels-2026.html",
    r"C:\Users\Administrator\.openclaw\workspace\novelpick.top\top-litrpg-web-novels-2026.html",
    r"C:\Users\Administrator\.openclaw\workspace\novelpick.top\best-time-travel-web-novels-2026.html",
    r"C:\Users\Administrator\.openclaw\workspace\fateandmethod.com\bazi-ten-gods-guide.html",
    r"C:\Users\Administrator\.openclaw\workspace\fateandmethod.com\chinese-numerology-complete-guide.html",
    r"C:\Users\Administrator\.openclaw\workspace\fateandmethod.com\feng-shui-2026-year-guide.html",
    r"C:\Users\Administrator\.openclaw\workspace\fateandmethod.com\chinese-zodiac-compatibility-guide.html",
]

for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    name = fp.split('\\')[-1]
    site = fp.split('\\')[-2]
    
    total_o = len(re.findall(r'<div\b', content))
    total_c = len(re.findall(r'</div>', content))
    print(f"\n=== {site}/{name} ===")
    print(f"  File: {total_o} <div> / {total_c} </div> = {total_o - total_c}")
    
    # Find article-body element
    m = re.search(r'class="[^"]*article-body[^"]*"', content)
    if m:
        # Find the opening tag that has this class
        tag_start = content.rfind('<', 0, m.start())
        tag_end = content.find('>', m.start()) + 1
        opening_tag = content[tag_start:tag_end]
        tag_name_match = re.match(r'<(div|main|section|article)\b', opening_tag)
        if tag_name_match:
            tag_name = tag_name_match.group(1)
            close_tag = f'</{tag_name}>'
            # Track nesting from open to close
            depth = 1
            pos = tag_end
            while depth > 0 and pos < len(content):
                so = content.find(f'<{tag_name}', pos)
                sc = content.find(close_tag, pos)
                if sc == -1:
                    print(f"  ERROR: {tag_name} never closed, depth={depth}")
                    break
                if so != -1 and so < sc:
                    depth += 1
                    pos = so + len(tag_name) + 1
                else:
                    depth -= 1
                    pos = sc + len(close_tag)
            if depth == 0:
                region = content[tag_start:pos]
                r_o = len(re.findall(r'<div\b', region))
                r_c = len(re.findall(r'</div>', region))
                # The outer article-body container may be <main> not <div>
                print(f"  Article-body ({tag_name}): {r_o} <div> / {r_c} </div> = {r_o - r_c}")
            else:
                print(f"  Article-body: unclosed")
    else:
        print(f"  No article-body class. Checking for main content div...")
        # Maybe it uses a different class or no class
        m2 = re.search(r'<main\b', content)
        if m2:
            print(f"  Found <main> tag at position {m2.start()}")
        else:
            print(f"  No <main> tag either")
