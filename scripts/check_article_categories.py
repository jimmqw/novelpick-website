"""Determine article categories for breadcrumb"""
import os
import re

base = r'C:\Users\Administrator\github\novelpick-website'
articles = [
    ('best-action-fantasy-web-novels-2026.html', 'Action & Adventure'),
    ('best-apocalypse-and-survival-novels.html', 'Apocalypse & Survival'),
    ('best-apocalypse-survival-web-novels.html', 'Apocalypse & Survival'),
    ('best-cozy-fantasy-novels.html', 'Cozy & Comfort'),
    ('best-cyberpunk-novels.html', 'Sci-Fi & Cyberpunk'),
    ('best-dark-fantasy-novels.html', 'Dark Fantasy'),
    ('best-enemies-to-lovers-romance-novels.html', 'Romance'),
    ('best-germinator-novels.html', 'Apocalypse & Survival'),
    ('best-historical-fantasy-novels.html', 'Historical Fantasy'),
    ('best-litrpg-novels.html', 'LitRPG'),
    ('best-progression-fantasy-novels.html', 'Progression Fantasy'),
    ('best-reincarnation-novels.html', 'Reincarnation'),
    ('best-science-fantasy-novels.html', 'Science Fantasy'),
    ('best-smart-protagonist-fantasy-novels.html', 'Fantasy'),
    ('best-solo-leveling-novels.html', 'LitRPG'),
    ('best-space-opera-novels-2026.html', 'Space Opera'),
    ('best-space-opera-novels.html', 'Space Opera'),
    ('best-system-apocalypse-novels.html', 'Apocalypse & Survival'),
    ('best-time-loop-web-novels-2026.html', 'Time Loop'),
    ('best-time-travel-novels.html', 'Time Travel'),
    ('best-urban-fantasy-novels-2026-v2.html', 'Urban Fantasy'),
    ('best-urban-fantasy-novels-2026.html', 'Urban Fantasy'),
    ('best-urban-fantasy-novels.html', 'Urban Fantasy'),
    ('best-wholesome-and-comfort-reads.html', 'Cozy & Comfort'),
    ('books-like-cradle.html', 'Fantasy'),
    ('books-like-harry-potter.html', 'Fantasy'),
    ('books-like-lord-of-the-rings.html', 'Fantasy'),
    ('books-like-mistborn.html', 'Fantasy'),
    ('books-like-percy-jackson.html', 'Fantasy'),
    ('shadow-slave-review.html', 'Reviews'),
    ('shadow-slave-vs-legendary-mechanic.html', 'Fantasy'),
    ('solo-leveling-inspired-novels.html', 'LitRPG'),
    ('solo-leveling-vs-shadow-slave.html', 'LitRPG'),
    ('best-xianxia-cultivation-novels.html', 'Xianxia'),
]

for fname, cat in sorted(articles):
    path = os.path.join(base, fname)
    if os.path.exists(path):
        c = open(path, encoding='utf-8').read()
        has_bc = bool(re.search(r'class=["\']breadcrumb', c, re.I))
        print(f'{fname}: {cat} (has_breadcrumb={has_bc})')
    else:
        print(f'{fname}: NOT FOUND')
