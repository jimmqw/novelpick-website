import re

# First, let's understand the fateandmethod article structure better
files_to_check = [
    r'C:\Users\Administrator\github\fateandmethod-site\chinese-zodiac-compatibility-guide.html',
    r'C:\Users\Administrator\github\fateandmethod-site\five-elements-complete-guide.html',
]

for fpath in files_to_check:
    content = open(fpath, 'r', encoding='utf-8', errors='replace').read()
    
    # Find article-body
    ab = content.find('article-body')
    if ab < 0:
        print(f'{fpath.split(chr(92))[-1]}: NO article-body found')
        continue
    
    # Find footer
    footer = content.find('<footer')
    rec = content.find('class="recommended"')
    end_pos = len(content)
    if footer > 0: end_pos = min(end_pos, footer)
    if rec > 0: end_pos = min(end_pos, rec)
    
    # Get the article-body div tag
    div_start = content.rfind('<div', 0, ab)
    div_open = content.find('>', div_start)
    
    print(f'\n{fpath.split(chr(92))[-1]}:')
    print(f'  article-body at: {ab}')
    print(f'  div tag at: {div_start}, > at: {div_open}')
    print(f'  div tag: {repr(content[div_start:div_open+1])}')
    
    # Extract content
    segment = content[div_start:end_pos]
    text = re.sub(r'<[^>]+>', '', segment).strip()
    print(f'  text length: {len(text)}')
    print(f'  first 100: {text[:100]}')
    print(f'  last 100: {text[-100:]}')