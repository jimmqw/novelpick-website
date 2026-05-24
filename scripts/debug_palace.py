with open(r'C:\Users\Administrator\.openclaw\workspace\fateandmethod.com\ziwei.html', 'rb') as f:
    content = f.read()
idx = content.find(b'<div class="palace-list">')
print('Found at byte:', idx)
palace_block = content[idx:idx+2500]
print(palace_block.decode('utf-8', errors='replace'))
