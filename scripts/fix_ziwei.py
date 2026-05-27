with open(r'C:\Users\Administrator\.openclaw\workspace\fateandmethod.com\ziwei.html', 'rb') as f:
    content = f.read()

# Fix palace names 2-12 (pinyin -> English)
replacements = [
    (b'<div class="palace-name">Ming</div><div class="palace-en">', b'<div class="palace-name">Siblings Palace</div><div class="palace-en">'),
    (b'<div class="palace-name">Ju</div><div class="palace-en">', b'<div class="palace-name">Property Palace</div><div class="palace-en">'),
    (b'<div class="palace-name">Yi</div><div class="palace-en">', b'<div class="palace-name">Career Palace</div><div class="palace-en">'),
]

# For palace 5 - replace just the second Yi occurrence in palace-list context
# We need to be more careful - there are multiple Yi occurrences
# Let's do it by finding unique surrounding context

old5 = b'<div class="palace-item"><span class="palace-num">5</span><div><div class="palace-name">Yi</div><div class="palace-en">\ufffd\ufffd\ufffd\ufffd\ufffd \ufffd\ufffd Siblings</div></div></div>'
new5 = b'<div class="palace-item"><span class="palace-num">5</span><div><div class="palace-name">Friends Palace</div><div class="palace-en">\ufffd\ufffd\ufffd\ufffd\ufffd \ufffd\ufffd Siblings</div></div></div>'

# Check if this pattern exists
if old5 in content:
    content = content.replace(old5, new5)
    print("Fixed palace 5")
else:
    print("Palace 5 pattern not found, trying alternate approach")
    # Find by position - the palace 5 item in the list
    # Let's just replace all <div class="palace-name">Yi</div> occurrences
    # But we need to be smart about which is which
    
    # Search for the exact byte sequence
    idx = content.find(b'<div class="palace-item"><span class="palace-num">5</span>')
    if idx >= 0:
        end = content.find(b'</div>\n</div>\n</div>', idx)
        old_block = content[idx:end+len('</div>\n</div>\n</div>')]
        print("Palace 5 block:")
        print(old_block[:200])
        print(old_block.decode('utf-8', errors='replace'))

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f"Fixed: {old[:50]}")
    else:
        print(f"NOT FOUND: {old[:50]}")

with open(r'C:\Users\Administrator\.openclaw\workspace\fateandmethod.com\ziwei.html', 'wb') as f:
    f.write(content)
print("Done")
