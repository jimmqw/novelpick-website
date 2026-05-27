#!/usr/bin/env python3
import sys
sys.stdout.reconfigure(encoding='utf-8')

content = open(r'C:\Users\Administrator\.openclaw\workspace\novelpick-website\best-action-fantasy-web-novels-2026.html', encoding='utf-8').read()
body_start = content.find('<body>')
body_end = content.rfind('</body>')
body = content[body_start:body_end]

# Find </header>
he = body.find('</header>')
after = body[he:he+500]
print('Raw content after </header>:')
print(after[:500])
print()

# Also check the article-hero for morai
morai = open(r'C:\Users\Administrator\.openclaw\workspace\morai-website\best-ai-agents-2026.html', encoding='utf-8').read()
mbody = morai[morai.find('<body>'):morai.rfind('</body>')]
mhe = mbody.find('</header>')
mafter = mbody[mhe:mhe+500]
print('MORAI raw content after </header>:')
print(mafter[:500])
