import re

content = open(r'C:\Users\Administrator\github\morai-website\chatgpt-vs-claude.html', 'r', encoding='utf-8', errors='replace').read()

# Check article-meta-row content
meta = re.search(r'<div class="article-meta-row">(.*?)</div>', content, re.DOTALL)
if meta:
    print('Meta row:', repr(meta.group(1)[:200]))
else:
    print('No article-meta-row found')

# Check for Chinese date
for kw in ['四月', 'May', 'June', 'July']:
    idx = content.find(kw)
    if idx >= 0:
        print(f'Found date keyword: {kw} at {idx}: {repr(content[idx-20:idx+30])}')

# Check garbled
garbled = '[釥쏵쏶]' in content
print('Garbled chars:', garbled)

# Check AI phrases
ai_phrases = ['game-changer', 'revolutionary', 'cutting-edge', 'unparalleled', 'next-level',
              'transformative', 'unmatched', 'best-in-class', 'ultimate solution',
              'seamless integration', 'effortless', 'powerful tool', 'game changing']
found = [p for p in ai_phrases if p.lower() in content.lower()]
print('AI phrases found:', found)

# Now check div balance after fix
print('\nDiv counts:')
print('  opens:', content.count('<div '))
print('  closes:', content.count('</div>'))
print('  diff:', content.count('<div ') - content.count('</div>'))

# Check article-body text length
ab = content.find('class="article-body"')
ab_open = content.find('>', ab)
footer = content.find('<footer')
segment = content[ab_open+1:footer]
text = re.sub(r'<[^>]+>', '', segment).strip()
print(f'\nArticle-body text length: {len(text)}')
print(f'Preview: {text[:200]}')