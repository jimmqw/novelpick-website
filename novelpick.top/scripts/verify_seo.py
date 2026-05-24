import re
content = open(r'C:\Users\Administrator\github\morai-site\best-ai-agents-2026.html', encoding='utf-8', errors='ignore').read()
m = re.search(r'og:image.*?content="([^"]+)"', content)
print('og:image:', m.group(1) if m else 'NOT FOUND')

m2 = re.search(r'canonical.*?href="([^"]+)"', content)
print('canonical:', m2.group(1) if m2 else 'NOT FOUND')

m3 = re.search(r'og:type.*?content="([^"]+)"', content)
print('og:type:', m3.group(1) if m3 else 'NOT FOUND')

# Check og:url
m4 = re.search(r'og:url.*?content="([^"]+)"', content)
print('og:url:', m4.group(1) if m4 else 'NOT FOUND')

# Also check if og:site_name is present
print('og:site_name:', 'YES' if 'og:site_name' in content else 'NO')

# Check twitter card
print('twitter:card:', 'YES' if 'twitter:card' in content else 'NO')
