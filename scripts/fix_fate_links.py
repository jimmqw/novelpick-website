with open(r'C:\Users\Administrator\.openclaw\workspace\fateandmethod.com\index.html', 'rb') as f:
    content = f.read()

# Now that ziwei-12-palaces-guide.html exists, link directly to it
old = b'<a href="/ziwei.html" class="read-more">Explore palaces \xe2\x86\x92</a>'
new = b'<a href="/ziwei-12-palaces-guide.html" class="read-more">Explore palaces \xe2\x86\x92</a>'
if old in content:
    content = content.replace(old, new)
    print("Fixed index.html to point to ziwei-12-palaces-guide.html")
else:
    print("Not found - may already be correct or different encoding")

with open(r'C:\Users\Administrator\.openclaw\workspace\fateandmethod.com\index.html', 'wb') as f:
    f.write(content)
print("Done")
