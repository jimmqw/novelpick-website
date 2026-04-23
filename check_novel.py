path = r'C:\Users\Administrator\.openclaw\workspace\novelpick.top\best-reincarnation-web-novels-2026.html'
with open(path, 'rb') as f:
    c = f.read()
# Show last part of file looking for href links
idx = c.rfind(b'href')
if idx >= 0:
    print(c[idx:idx+100])
else:
    print('No href found in last part')
    # Show last 500 bytes
    print(c[-500:])
