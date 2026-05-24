content = open(r'C:\Users\Administrator\github\morai-website\best-ai-coding-assistants-2026.html', 'r', encoding='utf-8', errors='replace').read()

# The overall diff is +1 (47 opens, 46 closes)
# Before article-body: diff=+3 (11 opens, 8 closes)
# In article-body: diff=-2 (36 opens, 38 closes)
# After article-body: diff=0

# 11 + 36 = 47 opens total
# 8 + 38 = 46 closes total

# Inside article-body: 36 opens but 38 closes = -2 diff
# The article-body section has 2 more closes than opens
# Which means somewhere in article-body, there's a spurious </div>

# Let me look for the extra </div> inside article-body
ab_pos = content.find('class="article-body"')
footer_pos = content.find('<footer')
rec_pos = content.find('class="recommended"')
end_pos = min(footer_pos if footer_pos > 0 else 999999, rec_pos if rec_pos > 0 else 999999)

segment = content[ab_pos:end_pos]
lines = segment.split('\n')
print('Article-body segment lines with </div>:')
for i, line in enumerate(lines):
    if '</div>' in line:
        print(f'  line {i}: {repr(line.strip())}')

# Also look for any unclosed divs in the h2/section structure
# Find all <section or <aside tags
import re
sections = re.findall(r'<(section|aside|div)[^>]*>', segment)
print(f'\nSections in article-body: {len(sections)}')
for s in sections[:10]:
    print(f'  {s}')