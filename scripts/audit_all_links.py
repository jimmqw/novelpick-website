import os

for site_name, site_path in [
    ('morai.top', r'C:\Users\Administrator\.openclaw\workspace\morai.top'),
    ('novelpick.top', r'C:\Users\Administrator\.openclaw\workspace\novelpick.top'),
    ('fateandmethod.com', r'C:\Users\Administrator\.openclaw\workspace\fateandmethod.com'),
]:
    print(f"\n=== {site_name} ===")
    files = [f for f in os.listdir(site_path) if f.endswith('.html')]
    broken = []
    for fname in files:
        path = os.path.join(site_path, fname)
        with open(path, 'rb') as f:
            content = f.read()
        # Check for directory-style links (no .html/.htm extension)
        import re
        # Find href="/xxx/" patterns
        hrefs = re.findall(b'href="(/[^"]+/)"', content)
        for href in hrefs:
            broken.append(f"{fname}: {href.decode()}")
        # Check for broken internal page links (href to non-existent local files)
        local_links = re.findall(b'href="(/[^"]*\.html)"', content)
        for link in local_links:
            target = link.decode().lstrip('/')
            target_path = os.path.join(site_path, target)
            if not os.path.exists(target_path):
                broken.append(f"{fname}: broken link {link.decode()}")
    if broken:
        for b in broken:
            print(f"  BROKEN: {b}")
    else:
        print(f"  All links OK ({len(files)} pages checked)")
