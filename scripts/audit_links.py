import os

site = r'C:\Users\Administrator\.openclaw\workspace\fateandmethod.com'
files = [f for f in os.listdir(site) if f.endswith('.html')]

broken = []
for fname in files:
    path = os.path.join(site, fname)
    with open(path, 'rb') as f:
        content = f.read()
    # Check for bad directory-style links
    bad_patterns = [b'/bazi/"', b'/divination/"', b'/resources/"', b'/ai-tools/"', b'/reviews/"', b'/guides/"', b'/genre/']
    for pat in bad_patterns:
        if pat in content:
            idx = content.find(pat)
            broken.append(f"{fname}: found {pat} at byte {idx}")

# Also check ziwei.html palace names
with open(os.path.join(site, 'ziwei.html'), 'rb') as f:
    ziwei = f.read()
if b'Life Palace' in ziwei and b'Siblings Palace' in ziwei:
    print("Ziwei palace names: OK")
else:
    print("Ziwei palace names: STILL BROKEN")

# Check index for broken link
with open(os.path.join(site, 'index.html'), 'rb') as f:
    idx_html = f.read()
if b'ziwei-12-palaces-guide' in idx_html:
    print("index.html: links to ziwei-12-palaces-guide.html OK")
elif b'ziwei.html' in idx_html:
    print("index.html: links to ziwei.html (page exists, acceptable)")
else:
    print("index.html: broken link still present")

if broken:
    print("\nBroken links found:")
    for b in broken:
        print(" -", b)
else:
    print("\nNo broken directory-style links found")
