import re

with open(r'C:\Users\Administrator\.openclaw\workspace\morai.top\best-ai-agents-2026.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Count occurrences
print('article-body openings:', content.count('class="article-body"'))
print('article-body div tag count:', content.count('<div class="article-body"'))

# Find the section
idx = content.find('<div class="article-body"')
if idx >= 0:
    section = content[idx:idx+5000]
    print('\nFirst 200 chars of article-body section:')
    print(repr(section[:200]))
    print('\n\nSearching for close div...')
    
    # Find the matching close </div>
    # Count nested divs
    depth = 1
    pos = len('<div class="article-body">')
    while depth > 0 and pos < len(section):
        next_open = section.find('<div', pos)
        next_close = section.find('</div>', pos)
        if next_close == -1:
            print('No closing div found!')
            break
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 5
        else:
            depth -= 1
            pos = next_close + 6
    
    print(f'Article-body ends at offset {pos} in section')
    print('Last 300 chars of article-body:')
    print(repr(section[pos-300:pos+50]))