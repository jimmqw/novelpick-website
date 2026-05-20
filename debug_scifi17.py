with open(r'C:\Users\Administrator\github\novelpick-website\scifi.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check all occurrences of "verdict-box" in the content
import re
for m in re.finditer(r'verdict-box', content):
    print(f'Found at position {m.start()}: {repr(content[m.start()-20:m.start()+50])}')