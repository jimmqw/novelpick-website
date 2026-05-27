# NovelPick SEO Fix Script — Add missing canonical + Baidu + OG to key pages
import os, re

BAIDU = '<script>var _hmt=_hmt||[];(function(){var hm=document.createElement("script");hm.src="https://hm.baidu.com/hm.js?d6d20fb609876081e0de8872c69e39aa";var s=document.getElementsByTagName("script")[0];s.parentNode.insertBefore(hm,s);})();</script>'
dir = r'C:\Users\Administrator\.openclaw\workspace\novelpick.top'

pages = {
    'books-like-solo-leveling.html': {
        'title': 'Books Like Solo Leveling – Top 15 Web Novels You Must Read',
        'desc': '15 web novels like Solo Leveling — dungeon crawlers, power fantasy, and hunter series ranked by gameplay depth and protagonist journey.',
        'og_url': 'https://novelpick.top/books-like-solo-leveling.html',
    },
    'contact.html': {
        'title': 'Contact NovelPick — Get in Touch',
        'desc': 'Reach NovelPick for novel recommendations, corrections, corrections, or partnership inquiries.',
        'og_url': 'https://novelpick.top/contact.html',
    },
    'about.html': {
        'title': 'About NovelPick — Our Curation Process',
        'desc': 'Learn about NovelPick — how we curate, rate, and recommend the best web novels across every genre.',
        'og_url': 'https://novelpick.top/about.html',
    },
}

for fname, meta in pages.items():
    fp = os.path.join(dir, fname)
    if not os.path.exists(fp):
        print(f'SKIP: {fname} not found')
        continue
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()

    # Check if already has the fixes
    if 'hm.baidu.com' in c and 'og:site_name' in c and 'rel="canonical"' in c:
        print(f'OK: {fname} — already fixed')
        continue

    changes = []
    if 'hm.baidu.com' not in c:
        c = c.replace('</head>', BAIDU + '\n</head>')
        changes.append('+baidu')
    if 'og:site_name' not in c:
        og_add = f'\n<meta property="og:site_name" content="NovelPick">\n<meta property="og:type" content="website">'
        c = c.replace('</head>', og_add + '\n</head>')
        changes.append('+og')
    if 'rel="canonical"' not in c:
        canon = f'<link rel="canonical" href="{meta["og_url"]}">'
        c = c.replace('</head>', canon + '\n</head>')
        changes.append('+canonical')
    if not changes:
        print(f'OK: {fname}')
        continue
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f'FIXED: {fname} — {" ".join(changes)}')