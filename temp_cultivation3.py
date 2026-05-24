content = open(r'C:\Users\Administrator\github\novelpick-website\best-cultivation-novels-2026.html', 'r', encoding='utf-8', errors='replace').read()

main_close = content.find('</main>')
print(f'Main closes at: {main_close}')
print(repr(content[main_close-200:main_close+50]))
