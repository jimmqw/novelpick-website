import os, re

# === fateandmethod.com ===
site = r'C:\Users\Administrator\.openclaw\workspace\fateandmethod.com'
files = [os.path.join(site, f) for f in os.listdir(site) if f.endswith('.html')]

# Footer/nav links: /privacy/ -> /privacy.html etc.
footer_fixes = {
    b'href="/privacy/"': b'href="/privacy.html"',
    b'href="/about/"': b'href="/about.html"',
    b'href="/contact/"': b'href="/contact.html"',
    b'href="/xuankong/"': b'href="/xuankong.html"',
}

for path in files:
    with open(path, 'rb') as f:
        c = f.read()
    original = c
    for old, new in footer_fixes.items():
        c = c.replace(old, new)
    if c != original:
        with open(path, 'wb') as f:
            f.write(c)
        print(f"Fixed: {os.path.basename(path)}")

# === morai.top ===
site2 = r'C:\Users\Administrator\.openclaw\workspace\morai.top'
files2 = [os.path.join(site2, f) for f in os.listdir(site2) if f.endswith('.html')]

# Sidebar nav links that point to non-existent category pages
# Replace sidebar nav /ai-tools/ etc with homepage links
morai_nav_fixes = [
    (b'href="/ai-tools/"', b'href="/"'),
    (b'href="/ai-reviews/"', b'href="/best-ai-agents-2026.html"'),
    (b'href="/ai-comparisons/"', b'href="/best-ai-writing-tools-2026.html"'),
    (b'href="/ai-guides/"', b'href="/github-copilot-review-2026.html"'),
    (b'href="/deals/"', b'href="/best-ai-video-generation-tools-2026.html"'),
    # Also fix the nav links in the HTML nav bar
    (b'href="/ai-tools/"', b'href="/"'),
    (b'href="/reviews/"', b'href="/best-ai-agents-2026.html"'),
    (b'href="/news/"', b'href="/"'),
    (b'href="/guides/"', b'href="/best-ai-writing-tools-2026.html"'),
]

for path in files2:
    with open(path, 'rb') as f:
        c = f.read()
    original = c
    for old, new in morai_nav_fixes:
        c = c.replace(old, new)
    if c != original:
        with open(path, 'wb') as f:
            f.write(c)
        print(f"Fixed morai: {os.path.basename(path)}")

# === novelpick.top ===
site3 = r'C:\Users\Administrator\.openclaw\workspace\novelpick.top'
files3 = [os.path.join(site3, f) for f in os.listdir(site3) if f.endswith('.html')]

novel_fixes = [
    (b'href="/genre/fantasy/"', b'href="/best-cultivation-novels-2026.html"'),
    (b'href="/genre/litrpg/"', b'href="/best-cultivation-novels-2026.html"'),
    (b'href="/genre/romance/"', b'href="/top-romance-web-novels-2026.html"'),
    (b'href="/genre/scifi/"', b'href="/best-reincarnation-web-novels-2026.html"'),
    (b'href="/genre/action/"', b'href="/best-cultivation-novels-2026.html"'),
    (b'href="/rankings/"', b'href="/top-romance-web-novels-2026.html"'),
    (b'href="/reviews/"', b'href="/top-romance-web-novels-2026.html"'),
    (b'href="/privacy/"', b'href="/privacy.html"'),
    (b'href="/about/"', b'href="/about.html"'),
    (b'href="/contact/"', b'href="/contact.html"'),
    # Broken article links - replace with closest existing page
    (b'href="/best-action-fantasy-web-novels-2026.html"', b'href="/best-cultivation-novels-2026.html"'),
    (b'href="/best-cultivation-novels-female-leads.html"', b'href="/best-cultivation-novels-2026.html"'),
    (b'href="/best-smart-protagonist-novels.html"', b'href="/best-reincarnation-web-novels-2026.html"'),
]

for path in files3:
    with open(path, 'rb') as f:
        c = f.read()
    original = c
    for old, new in novel_fixes:
        c = c.replace(old, new)
    if c != original:
        with open(path, 'wb') as f:
            f.write(c)
        print(f"Fixed novelpick: {os.path.basename(path)}")

print("All fixes done")
