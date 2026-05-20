with open(r'C:\Users\Administrator\github\novelpick-website\scifi.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Show the section around byte 19500-19650
print('Content around related div:')
print(repr(content[19490:19650]))
print()
print('Content around byte 20500-20650 (second verdict-box):')
print(repr(content[20500:20650]))