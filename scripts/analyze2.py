from pathlib import Path
import sys

def analyze(fp):
    c = fp.read_text(encoding='utf-8', errors='replace')
    name = fp.name
    print(f"\n=== {name} ===")
    print(f"  Baidu: {'hm.baidu.com' in c}")
    print(f"  breadcrumb: {'breadcrumb' in c}")
    print(f"  sidebar: {'sidebar' in c}")
    print(f"  <footer>: {'<footer' in c}")
    print(f"  copyright: {chr(169) in c or 'copy' in c.lower()}")
    print(f"  article-body: {'article-body' in c}")
    print(f"  nav class='nav': {'class=\"nav\"' in c}")
    print(f"  site-nav: {'site-nav' in c}")
    print(f"  reading time: {'minute' in c.lower() or 'min read' in c.lower()}")
    print(f"  canonical: {'canonical' in c}")
    print(f"  og:title: {'og:title' in c}")
    print(f"  meta desc: {'name=\"description\"' in c}")
    print(f"  viewport: {'viewport' in c}")
    print(f"  @media: {'@media' in c}")
    print(f"  layout: {'class=\"layout\"' in c}")

analyze(Path(r"C:\Users\Administrator\github\novelpick-website\best-action-fantasy-web-novels-2026.html"))
analyze(Path(r"C:\Users\Administrator\github\novelpick-website\best-cultivation-novels-female-leads.html"))
analyze(Path(r"C:\Users\Administrator\github\novelpick-website\shadow-slave-review.html"))
analyze(Path(r"C:\Users\Administrator\github\novelpick-website\index.html"))
analyze(Path(r"C:\Users\Administrator\github\novelpick-website\fantasy.html"))
