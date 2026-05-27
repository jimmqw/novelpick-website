content = open(r'C:\Users\Administrator\github\morai-website\best-ai-meeting-tools-2026.html', 'rb').read()
idx = content.find(b'<div class="article-meta-row">')
print('article-meta-row div at byte:', idx)
if idx >= 0:
    val_start = content.find(b'>', idx) + 1
    val_end = content.find(b'</div>', val_start)
    val_bytes = content[val_start:val_end]
    print('Value bytes:', val_bytes)
    print('As utf-8:', val_bytes.decode('utf-8', errors='replace'))
    
    # Search for Chinese month in the body
    body_start = content.find(b'<body')
    print('\nSearching for Chinese chars in body:')
    for i in range(body_start, len(content)):
        if content[i] > 127:
            print(f'  Byte {i}: {hex(content[i])} = {chr(content[i])} (context: {content[max(0,i-5):i+10]})')
            break
