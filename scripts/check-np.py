from pathlib import Path

novel_dir = Path(r'C:\Users\Administrator\github\novelpick-website')
for name in ['best-cultivation-novels-female-leads.html', 'best-revenge-web-novels.html',
             'best-smart-protagonist-fantasy-novels.html', 'books-like-solo-leveling.html',
             'best-villain-protagonist-web-novels.html', 'best-xianxia-cultivation-novels.html']:
    c = (novel_dir / name).read_text(encoding='utf-8', errors='replace')
    print(f'{name}:')
    print(f'  len={len(c)}, has nav={"nav" in c.lower()}, footer={"<footer" in c.lower()}')
    print(f'  breadcrumb={"breadcrumb" in c.lower()}, article-body={"article-body" in c}')
    print(f'  Baidu={"hm.baidu.com" in c}, copy={"&copy;" in c}')
    print()
