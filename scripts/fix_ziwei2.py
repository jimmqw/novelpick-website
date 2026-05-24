with open(r'C:\Users\Administrator\.openclaw\workspace\fateandmethod.com\ziwei.html', 'rb') as f:
    content = f.read()

# Find the palace-list section
start = content.find(b'<div class="palace-list">')
end = content.find(b'</div>\n\n<h2>How to Read', start)
old_block = content[start:end+len('</div>')]
print("Old block length:", len(old_block))

# Build new block with correct English names
new_palaces = (
    b'  <div class="palace-item"><span class="palace-num">1</span><div><div class="palace-name">Life Palace</div><div class="palace-en">\xe5\x91\xbd\xe5\xae\xab \xe2\x80\x94 Core identity & willpower</div></div></div>\n'
    b'  <div class="palace-item"><span class="palace-num">2</span><div><div class="palace-name">Siblings Palace</div><div class="palace-en">\xe5\x85\x84\xe5\xbc\x9f\xe5\xae\xab \xe2\x80\x94 Siblings & peers</div></div></div>\n'
    b'  <div class="palace-item"><span class="palace-num">3</span><div><div class="palace-name">Property Palace</div><div class="palace-en">\xe7\x94\xb0\xe5\xae\x85\xe5\xae\xab \xe2\x80\x94 Assets, home & roots</div></div></div>\n'
    b'  <div class="palace-item"><span class="palace-num">4</span><div><div class="palace-name">Career Palace</div><div class="palace-en">\xe5\xae\x98\xe7\xa6\x8f\xe5\xae\xab \xe2\x80\x94 Career & ambition</div></div></div>\n'
    b'  <div class="palace-item"><span class="palace-num">5</span><div><div class="palace-name">Friends Palace</div><div class="palace-en">\xe4\xba\xa4\xe5\x8f\x8b\xe5\xae\xab \xe2\x80\x94 Friends & subordinates</div></div></div>\n'
    b'  <div class="palace-item"><span class="palace-num">6</span><div><div class="palace-name">Health Palace</div><div class="palace-en">\xe7\x96\xbe\xe5\x8e\x8f\xe5\xae\xab \xe2\x80\x94 Health & illness</div></div></div>\n'
    b'  <div class="palace-item"><span class="palace-num">7</span><div><div class="palace-name">Migration Palace</div><div class="palace-en">\xe8\xbf\x81\xe7\xa7\xbb\xe5\xae\xab \xe2\x80\x94 Travel & migration</div></div></div>\n'
    b'  <div class="palace-item"><span class="palace-num">8</span><div><div class="palace-name">Servants Palace</div><div class="palace-en">\xe5\xa5\x96\xe4\xbb\x86\xe5\xae\xab \xe2\x80\x94 Subordinates & helpers</div></div></div>\n'
    b'  <div class="palace-item"><span class="palace-num">9</span><div><div class="palace-name">Business Palace</div><div class="palace-en">\xe5\xae\x98\xe7\xa6\x8f\xe5\xae\xab \xe2\x80\x94 Financial career</div></div></div>\n'
    b'  <div class="palace-item"><span class="palace-num">10</span><div><div class="palace-name">Parents Palace</div><div class="palace-en">\xe7\x88\xb6\xe6\xaf\x8d\xe5\xae\xab \xe2\x80\x94 Parents & authority</div></div></div>\n'
    b'  <div class="palace-item"><span class="palace-num">11</span><div><div class="palace-name">Virtue Palace</div><div class="palace-en">\xe7\xa6\x8f\xe5\xbe\xb7\xe5\xae\xab \xe2\x80\x94 Happiness & virtue</div></div></div>\n'
    b'  <div class="palace-item"><span class="palace-num">12</span><div><div class="palace-name">Children Palace</div><div class="palace-en">\xe5\xad\x90\xe6\x81\xaf\xe5\xae\xab \xe2\x80\x94 Children & legacy</div></div></div>\n'
)

new_block = b'<div class="palace-list">\n' + new_palaces + b'</div>'

content = content[:start] + new_block + content[end+len('</div>'):]

with open(r'C:\Users\Administrator\.openclaw\workspace\fateandmethod.com\ziwei.html', 'wb') as f:
    f.write(content)
print("Done - palace names fixed")
