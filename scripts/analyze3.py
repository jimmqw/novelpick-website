from pathlib import Path

def analyze(fp):
    c = fp.read_text(encoding='utf-8', errors='replace')
    name = fp.name
    print(f"\n=== {name} ===")
    
    # Find nav-related classes
    import re
    nav_matches = re.findall(r'class="[^"]*nav[^"]*"', c, re.I)
    print(f"  nav classes: {nav_matches}")
    
    # Find header structure
    head_matches = re.findall(r'class="[^"]*head[^"]*"', c, re.I)
    print(f"  header classes: {head_matches}")
    
    # Find body content structure
    body_start = c.find('<body')
    if body_start > 0:
        body_section = c[body_start:body_start+1500]
        print(f"  Body start section:")
        print(body_section)
    
    # Find article-body structure
    if 'article-body' in c:
        idx = c.find('class="article-body"')
        print(f"  article-body found at: {idx}")
        print(f"  Context: {c[max(0,idx-200):idx+300]}")

analyze(Path(r"C:\Users\Administrator\github\novelpick-website\best-action-fantasy-web-novels-2026.html"))
analyze(Path(r"C:\Users\Administrator\github\novelpick-website\best-cultivation-novels-female-leads.html"))
