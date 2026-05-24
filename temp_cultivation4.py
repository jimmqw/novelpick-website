content = open(r'C:\Users\Administrator\github\novelpick-website\best-cultivation-novels-2026.html', 'r', encoding='utf-8', errors='replace').read()

# Find prev-next nav
prevnext = content.find('class="prev-next"')
print(f'prev-next at: {prevnext}')
print(repr(content[prevnext-200:prevnext]))
