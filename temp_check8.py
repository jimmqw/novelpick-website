import re

content = open(r'C:\Users\Administrator\github\fateandmethod-site\bazi.html', 'r', encoding='utf-8', errors='replace').read()

# Check last h2 before footer
h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', content, re.DOTALL | re.IGNORECASE)
print('H2 count:', len(h2s))
for h2 in h2s:
    clean = re.sub(r'<[^>]+>', '', h2).strip()
    print(' -', clean[:60])

# Check for any related/keep reading section
for kw in ['continue exploring', 'related', 'keep reading', 'recommended']:
    idx = content.lower().find(kw)
    if idx >= 0:
        print(f'Found "{kw}" at {idx}')
        print(repr(content[idx-30:idx+80]))

# Check the article ending
footer = content.find('<footer')
before_footer = content[footer-500:footer]
print('\n--- Last 500 before footer ---')
print(repr(before_footer))