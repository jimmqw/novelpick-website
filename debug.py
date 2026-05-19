import os
os.chdir(r'C:\Users\Administrator\.openclaw\workspace\novelpick-website')
with open('best-cultivation-novels-2026.html', 'rb') as f:
    data = f.read()
idx = data.find(b'&amp;')
print('Found &amp; at:', idx)
print('Context:', data[idx-20:idx+50])