import re, sys
from pathlib import Path

def check_file(path_str):
    fp = Path(path_str)
    content = fp.read_text(encoding='utf-8', errors='replace')
    full = content  # full content
    first = content[:3000]

    has_header_tag = bool(re.search(r'<header[ >]', first, re.I))
    has_header_div = bool(re.search(r'<div[^>]*class="[^"]*header[^"]*"', first, re.I))
    has_article = bool(re.search(r'<article[ >]', first, re.I))
    has_baidu = 'hm.baidu.com' in full
    has_footer = bool(re.search(r'<footer[ >]', first, re.I))
    has_breadcrumb = 'breadcrumb' in first.lower()

    open_d = len(re.findall(r'<div[ >]', full, re.I))
    close_d = len(re.findall(r'</div>', full, re.I))

    print(f"=== {fp.name} ===")
    print(f"  <header> tag:  {has_header_tag}")
    print(f"  <div *header>: {has_header_div}")
    print(f"  <article>:     {has_article}")
    print(f"  <footer>:      {has_footer}")
    print(f"  breadcrumb:    {has_breadcrumb}")
    print(f"  Baidu:         {has_baidu}")
    print(f"  div open/close: {open_d}/{close_d}")
    print(f"  First 400 chars:")
    print(first[:400])
    print()

if __name__ == '__main__':
    for p in sys.argv[1:]:
        check_file(p)
