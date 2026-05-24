# -*- coding: utf-8 -*-
import os, re

base = r'C:\Users\Administrator\.openclaw\workspace'

# Check zodiac file corruption
fp = os.path.join(base, 'fateandmethod-website', 'chinese-zodiac-2026-fire-snake-horoscope.html')
d = open(fp, encoding='utf-8').read()

print('=== ZODIAC FILE ===')
if 'Dodos-donts' in d:
    pos = d.find('Dodos-donts')
    print(f'STILL CORRUPTED at pos {pos}')
    print(f'  Context: ...{d[max(0,pos-60):pos+100]}...')
else:
    print('Dodos-donts: NOT FOUND (may be fixed)')

opens = d.count('<div ') + d.count('<div>')
closes = d.count('</div>')
print(f'Div balance: {opens} opens vs {closes} closes = {opens - closes}')

# Check claude file garbled
fp2 = os.path.join(base, 'morai-website', 'claude-3-7-sonnet-review.html')
d2 = open(fp2, encoding='utf-8').read()
print('\n=== CLAUDE FILE ===')
opens2 = d2.count('<div ') + d2.count('<div>')
closes2 = d2.count('</div>')
print(f'Div balance: {opens2} opens vs {closes2} closes = {opens2 - closes2}')
# Find \u9225 occurrences
for i, ch in enumerate(d2):
    if ord(ch) == 0x9225:
        ctx = repr(d2[max(0,i-10):i+20])
        print(f'Garbled at pos {i}: {ctx}')
        break

# Check all files in article list exist
print('\n=== FILE EXISTENCE CHECK ===')
articles = [
    ('morai-website', 'chatgpt-vs-claude-vs-gemini-2026.html'),
    ('morai-website', 'best-ai-tools-2026.html'),
    ('morai-website', 'ai-agent-tools-2026.html'),
    ('novelpick-website', 'books-like-solo-leveling-top15.html'),
    ('novelpick-website', 'best-chinese-wuxia-web-novels-2026.html'),
    ('novelpick-website', 'top-romance-web-novels-2026.html'),
    ('fateandmethod-website', 'feng-shui-2026-year-guide.html'),
    ('fateandmethod-website', 'bazi-beginners-complete-guide.html'),
    ('fateandmethod-website', 'five-elements-complete-guide.html'),
]
# Find correct solo-leveling filename
np_dir = os.path.join(base, 'novelpick-website')
for fn in os.listdir(np_dir):
    if 'solo' in fn.lower() or 'leveling' in fn.lower():
        print(f'  novelpick solo-leveling files: {fn}')

for site, fname in articles:
    fp = os.path.join(base, site, fname)
    status = 'OK' if os.path.exists(fp) else 'MISSING'
    print(f'  {site}/{fname}: {status}')
