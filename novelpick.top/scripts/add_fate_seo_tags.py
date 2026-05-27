"""Add og:title and canonical to fateandmethod pages"""
import re
import os

FATE_PATH = r'C:\Users\Administrator\github\fateandmethod-site'

PAGES = {
    'index.html': {
        'og:title': 'Fate & Method — Chinese Metaphysics in English',
        'canonical': 'https://fateandmethod.com/'
    },
    'ziwei.html': {
        'og:title': 'Zi Wei Dou Shu — China\'s Imperial Astrology System | Fate & Method',
        'canonical': 'https://fateandmethod.com/ziwei.html'
    },
    'ziwei-intro.html': {
        'og:title': 'What Is Zi Wei Dou Shu? Getting Started | Fate & Method',
        'canonical': 'https://fateandmethod.com/ziwei-intro.html'
    },
    'ziwei-stars.html': {
        'og:title': 'Zi Wei Star Types: Bright, Neutral & Dark | Fate & Method',
        'canonical': 'https://fateandmethod.com/ziwei-stars.html'
    },
    'ziwei-palaces.html': {
        'og:title': 'Zi Wei Twelve Palaces: Life\'s Domains | Fate & Method',
        'canonical': 'https://fateandmethod.com/ziwei-palaces.html'
    },
    'ziwei-reading.html': {
        'og:title': 'How to Read a Zi Wei Chart | Fate & Method',
        'canonical': 'https://fateandmethod.com/ziwei-reading.html'
    },
    'ziwei-combinations.html': {
        'og:title': 'Zi Wei Star Combinations & Interactions | Fate & Method',
        'canonical': 'https://fateandmethod.com/ziwei-combinations.html'
    },
    'liuyao.html': {
        'og:title': 'Liu Yao (Six Lines) — The Art of Change | Fate & Method',
        'canonical': 'https://fateandmethod.com/liuyao.html'
    },
    'bazi.html': {
        'og:title': 'Ba Zi (Four Pillars) — Time-Based Destiny | Fate & Method',
        'canonical': 'https://fateandmethod.com/bazi.html'
    },
    'daliuren.html': {
        'og:title': 'Da Liu Ren — Great Worth of the Six Relations | Fate & Method',
        'canonical': 'https://fateandmethod.com/daliuren.html'
    },
    'xiaoliuren.html': {
        'og:title': 'Xiao Liu Ren — Little Worth of the Six Relations | Fate & Method',
        'canonical': 'https://fateandmethod.com/xiaoliuren.html'
    },
    'meihua.html': {
        'og:title': 'Mei Hua (Plum Blossom) Numerology | Fate & Method',
        'canonical': 'https://fateandmethod.com/meihua.html'
    },
    'xuankong.html': {
        'og:title': 'Xuan Kong (Flying Stars) — Time-Space Feng Shui | Fate & Method',
        'canonical': 'https://fateandmethod.com/xuankong.html'
    },
    'taiyi.html': {
        'og:title': 'Tai Yi (Grand Unity) — Celestial Stem Magic | Fate & Method',
        'canonical': 'https://fateandmethod.com/taiyi.html'
    },
    'daily-wisdom.html': {
        'og:title': 'Daily Wisdom — Quick Metaphysical Insights | Fate & Method',
        'canonical': 'https://fateandmethod.com/daily-wisdom.html'
    },
    'daily-wisdom-car-sickness.html': {
        'og:title': 'Car Sickness & Travel: Daily Wisdom | Fate & Method',
        'canonical': 'https://fateandmethod.com/daily-wisdom-car-sickness.html'
    },
    'daily-wisdom-garlic-diarrhea.html': {
        'og:title': 'Garlic & Digestion: Daily Wisdom | Fate & Method',
        'canonical': 'https://fateandmethod.com/daily-wisdom-garlic-diarrhea.html'
    },
    'daily-wisdom-name-destiny.html': {
        'og:title': 'Names & Destiny: Daily Wisdom | Fate & Method',
        'canonical': 'https://fateandmethod.com/daily-wisdom-name-destiny.html'
    },
    'daily-wisdom-name-psychology.html': {
        'og:title': 'Name Psychology: Daily Wisdom | Fate & Method',
        'canonical': 'https://fateandmethod.com/daily-wisdom-name-psychology.html'
    },
    'daily-wisdom-sun-absorption.html': {
        'og:title': 'Sun Absorption & Energy: Daily Wisdom | Fate & Method',
        'canonical': 'https://fateandmethod.com/daily-wisdom-sun-absorption.html'
    },
}

fixed = []
errors = []

for fname, data in PAGES.items():
    path = os.path.join(FATE_PATH, fname)
    if not os.path.exists(path):
        errors.append(f'{fname}: NOT FOUND')
        continue
    
    with open(path, encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    changes = []
    
    # Add og:title if missing
    if 'og:title' not in content:
        og_tag = f'<meta property="og:title" content="{data["og:title"]}">'
        # Insert after description meta tag
        desc_match = re.search(r'<meta name="description" content="[^"]+">', content)
        if desc_match:
            new_content = content[:desc_match.end()] + '\n    ' + og_tag + content[desc_match.end():]
            changes.append('og:title')
        else:
            # Try alternate description pattern
            desc_match2 = re.search(r'<meta name=[\'"]description[\'"] content=[\'"][^\'"]+[\'"]>', content)
            if desc_match2:
                new_content = content[:desc_match2.end()] + '\n    ' + og_tag + content[desc_match2.end():]
                changes.append('og:title')
    
    # Add canonical if missing
    if 'canonical' not in content:
        can_tag = f'<link rel="canonical" href="{data["canonical"]}">'
        # Insert after og:title (in the new content)
        og_match = re.search(r'<meta property="og:title" content="[^"]+">', new_content)
        if og_match:
            new_content = new_content[:og_match.end()] + '\n    ' + can_tag + new_content[og_match.end():]
            changes.append('canonical')
        else:
            # Insert after description in new content
            desc_match = re.search(r'<meta name="description" content="[^"]+">', new_content)
            if desc_match:
                new_content = new_content[:desc_match.end()] + '\n    ' + can_tag + new_content[desc_match.end():]
                changes.append('canonical')
    
    if changes:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        fixed.append(f'{fname}: added {", ".join(changes)}')
    else:
        fixed.append(f'{fname}: already has tags')

print(f'Processed {len(PAGES)} pages:')
for f in fixed:
    print(f'  {f}')
if errors:
    print(f'\nErrors: {errors}')
