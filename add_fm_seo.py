import os, re

dir = r'C:\Users\Administrator\.openclaw\workspace\fateandmethod.com'

# Pages that are full articles (not just stubs)
article_pages = [
    'bazi-ten-gods-guide.html',
    'chinese-zodiac-compatibility-guide.html',
    'feng-shui-2026-year-guide.html',
    'index.html',
]

for fname in article_pages:
    path = os.path.join(dir, fname)
    if not os.path.exists(path):
        continue
    with open(path, encoding='utf-8', errors='replace') as f:
        c = f.read()
    
    # Add og:image if missing
    if 'og:image' not in c:
        # Find the last meta property tag before </head>
        head_end = c.find('</head>')
        if head_end >= 0:
            # Insert og:image before </head>
            og_tag = '\n<meta property="og:image" content="https://fateandmethod.com/og-default.png">'
            c = c[:head_end] + og_tag + c[head_end:]
            with open(path, 'w', encoding='utf-8') as f:
                f.write(c)
            print(f'Added og:image to {fname}')
        else:
            print(f'No </head> found in {fname}')
    else:
        print(f'{fname} already has og:image')

# Also add meta description if missing (only for article pages)
descriptions = {
    'bazi-ten-gods-guide.html': 'Master BaZi Ten Gods (十神) — the ten symbolic forces that shape your destiny. Complete guide with tables, interpretations, and practical applications.',
    'chinese-zodiac-compatibility-guide.html': 'Discover which Chinese zodiac signs are most compatible for love, career, and friendship. Complete compatibility chart, element analysis, and expert guidance for 2026.',
    'feng-shui-2026-year-guide.html': 'Feng Shui 2026 guide — Year of the Fire Snake. Learn how to arrange your space, activate key areas, and harness auspicious chi for fortune, health, and relationships.',
    'index.html': 'FateAndMethod.com — Your authoritative guide to Chinese metaphysics. Explore BaZi, Ziwei Dou Shu, Liuyao Yijing, Feng Shui, and other ancient divination systems.',
}

for fname, desc in descriptions.items():
    path = os.path.join(dir, fname)
    if not os.path.exists(path):
        continue
    with open(path, encoding='utf-8', errors='replace') as f:
        c = f.read()
    
    if 'meta name="description"' not in c:
        head_end = c.find('</head>')
        if head_end >= 0:
            desc_tag = f'\n<meta name="description" content="{desc}">'
            c = c[:head_end] + desc_tag + c[head_end:]
            with open(path, 'w', encoding='utf-8') as f:
                f.write(c)
            print(f'Added meta description to {fname}')
        else:
            print(f'No </head> found in {fname}')
    else:
        print(f'{fname} already has meta description')
