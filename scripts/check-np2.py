from pathlib import Path

# Check novelpick pages that lack article-body
for name in ['best-revenge-web-novels.html', 'best-smart-protagonist-fantasy-novels.html',
             'best-cultivation-novels-female-leads.html']:
    c = (Path(r'C:\Users\Administrator\github\novelpick-website') / name).read_text(encoding='utf-8', errors='replace')
    print(f'=== {name} ===')
    # Find body content
    body_start = c.find('<body>')
    if body_start < 0:
        body_start = c.find('<body ')
    if body_start > 0:
        section = c[body_start:body_start+3000]
        # Remove style blocks for clarity
        section_clean = section.replace('<style>', '<STYLE>').replace('</style>', '</STYLE>')
        # Print only up to where main content starts
        print(section_clean[:2000])
    print()
