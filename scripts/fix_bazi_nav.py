with open(r'C:\Users\Administrator\.openclaw\workspace\fateandmethod.com\bazi-ten-gods-guide.html', 'rb') as f:
    content = f.read()

# Fix /bazi/ -> /bazi.html
content = content.replace(b'href="/bazi/"', b'href="/bazi.html"')
content = content.replace(b'href="/divination/"', b'href="/liuyao.html"')
content = content.replace(b'href="/resources/"', b'href="/daily-wisdom.html"')

with open(r'C:\Users\Administrator\.openclaw\workspace\fateandmethod.com\bazi-ten-gods-guide.html', 'wb') as f:
    f.write(content)
print("Fixed bazi-ten-gods-guide.html nav links")
