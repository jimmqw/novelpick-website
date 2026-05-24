"""Add breadcrumb to novelpick article pages"""
import re
import os

# Category mapping: article -> (category name, category URL)
CATEGORIES = {
    'best-action-fantasy-web-novels-2026.html': ('Action & Adventure', '/fantasy.html'),
    'best-apocalypse-and-survival-novels.html': ('Apocalypse & Survival', '/fantasy.html'),
    'best-apocalypse-survival-web-novels.html': ('Apocalypse & Survival', '/fantasy.html'),
    'best-cozy-fantasy-novels.html': ('Cozy & Comfort', '/fantasy.html'),
    'best-cyberpunk-novels.html': ('Sci-Fi & Cyberpunk', '/scifi.html'),
    'best-dark-fantasy-novels.html': ('Dark Fantasy', '/fantasy.html'),
    'best-enemies-to-lovers-romance-novels.html': ('Romance', '/romance.html'),
    'best-germinator-novels.html': ('Apocalypse & Survival', '/fantasy.html'),
    'best-historical-fantasy-novels.html': ('Historical Fantasy', '/fantasy.html'),
    'best-litrpg-novels.html': ('LitRPG', '/litrpg.html'),
    'best-progression-fantasy-novels.html': ('Progression Fantasy', '/litrpg.html'),
    'best-reincarnation-novels.html': ('Reincarnation', '/fantasy.html'),
    'best-science-fantasy-novels.html': ('Science Fantasy', '/scifi.html'),
    'best-smart-protagonist-fantasy-novels.html': ('Fantasy', '/fantasy.html'),
    'best-solo-leveling-novels.html': ('LitRPG', '/litrpg.html'),
    'best-space-opera-novels-2026.html': ('Space Opera', '/scifi.html'),
    'best-space-opera-novels.html': ('Space Opera', '/scifi.html'),
    'best-system-apocalypse-novels.html': ('Apocalypse & Survival', '/fantasy.html'),
    'best-time-loop-web-novels-2026.html': ('Time Loop', '/scifi.html'),
    'best-time-travel-novels.html': ('Time Travel', '/scifi.html'),
    'best-urban-fantasy-novels-2026-v2.html': ('Urban Fantasy', '/fantasy.html'),
    'best-urban-fantasy-novels-2026.html': ('Urban Fantasy', '/fantasy.html'),
    'best-urban-fantasy-novels.html': ('Urban Fantasy', '/fantasy.html'),
    'best-wholesome-and-comfort-reads.html': ('Cozy & Comfort', '/fantasy.html'),
    'best-xianxia-cultivation-novels.html': ('Xianxia', '/fantasy.html'),
    'books-like-cradle.html': ('Fantasy', '/fantasy.html'),
    'books-like-harry-potter.html': ('Fantasy', '/fantasy.html'),
    'books-like-lord-of-the-rings.html': ('Fantasy', '/fantasy.html'),
    'books-like-mistborn.html': ('Fantasy', '/fantasy.html'),
    'books-like-percy-jackson.html': ('Fantasy', '/fantasy.html'),
    'shadow-slave-review.html': ('Reviews', '/reviews.html'),
    'shadow-slave-vs-legendary-mechanic.html': ('Fantasy', '/fantasy.html'),
    'solo-leveling-inspired-novels.html': ('LitRPG', '/litrpg.html'),
    'solo-leveling-vs-shadow-slave.html': ('LitRPG', '/litrpg.html'),
}

base = r'C:\Users\Administrator\github\novelpick-website'
fixed = []
errors = []

for fname, (cat_name, cat_url) in CATEGORIES.items():
    path = os.path.join(base, fname)
    if not os.path.exists(path):
        errors.append(f'{fname}: NOT FOUND')
        continue
    
    with open(path, encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has breadcrumb
    if re.search(r'class=["\']breadcrumb', content, re.I):
        continue
    
    breadcrumb = f'<div class="breadcrumb"><a href="/">Home</a> / <a href="{cat_url}">{cat_name}</a></div>'
    
    # Insert after <div class="article-body"> and before <div class="article-header">
    # Pattern: <div class="article-body">\n<div class="article-header">
    pattern = re.compile(r'(<div class="article-body">)\s*(<div class="article-header">)', re.DOTALL)
    
    if pattern.search(content):
        new_content = pattern.sub(r'\1\n    ' + breadcrumb + r'\n    \2', content)
        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            fixed.append(fname)
        else:
            errors.append(f'{fname}: pattern match but no change')
    else:
        # Try alternate pattern
        pattern2 = re.compile(r'(<div class="article-body">)\s*(<div class="article-header">)', re.DOTALL)
        if pattern2.search(content):
            new_content = pattern2.sub(r'\1\n    ' + breadcrumb + r'\n    \2', content)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            fixed.append(fname)
        else:
            errors.append(f'{fname}: article-header pattern not found')

print(f'Added breadcrumbs to {len(fixed)} files:')
for f in fixed:
    print(f'  {f}')
if errors:
    print(f'\nErrors ({len(errors)}):')
    for e in errors:
        print(f'  {e}')
