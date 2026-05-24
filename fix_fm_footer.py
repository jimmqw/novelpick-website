fpath = r'C:\Users\Administrator\.openclaw\workspace\fateandmethod-website\index.html'
with open(fpath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix duplicate footer - remove the second footer
old_footer = '''<footer class="footer">
        <p>© 2026 FateAndMethod.com — Bringing Chinese Metaphysics to the World</p>
    </footer>
<footer>
<a href="/">Fate & Method</a> | <a href="/ziwei.html">Zi Wei</a> | <a href="/liuyao.html">Liu Yao</a> | <a href="/bazi.html">Ba Zi</a> | <a href="/daily-wisdom.html">Daily Wisdom</a>
<p style="margin-top:0.5rem">© 2026 FateAndMethod.com — Explore Eastern Metaphysics</p>
</footer>'''

new_footer = '''<footer class="footer">
        <p>© 2026 FateAndMethod.com — Bringing Chinese Metaphysics to the World</p>
    </footer>'''

if old_footer in content:
    content = content.replace(old_footer, new_footer)
    print('Fixed duplicate footer')
else:
    print('Double footer pattern not found, checking separately')
    if '<footer class="footer">' in content:
        idx = content.find('<footer class="footer">')
        print('Found first footer at', idx)
        # Check if there's a second footer
        idx2 = content.find('<footer>', idx + 100)
        if idx2 >= 0:
            print('Found second footer at', idx2)
            segment = content[idx2:idx2+200]
            print(repr(segment))

with open(fpath, 'w', encoding='utf-8') as f:
    f.write(content)