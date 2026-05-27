fpath = r'C:\Users\Administrator\.openclaw\workspace\fateandmethod-website\index.html'
with open(fpath, 'r', encoding='utf-8') as f:
    content = f.read()

# The second footer (the one after the first footer in the body)
old = '''<footer class="footer">
        <p>© 2026 FateAndMethod.com — Bringing Chinese Metaphysics to the World</p>
    </footer>
<footer>
<a href="/">Fate & Method</a> | <a href="/ziwei.html">Zi Wei</a> | <a href="/liuyao.html">Liu Yao</a> | <a href="/bazi.html">Ba Zi</a> | <a href="/daily-wisdom.html">Daily Wisdom</a>
<p style="margin-top:0.5rem">© 2026 FateAndMethod.com — Explore Eastern Metaphysics</p>
</footer>'''

if old in content:
    content = content.replace(old, '''<footer class="footer">
        <p>© 2026 FateAndMethod.com — Bringing Chinese Metaphysics to the World</p>
    </footer>''')
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('SUCCESS - removed duplicate footer')
else:
    # Try each piece separately
    if '<footer>\n<a href="/">' in content:
        print('Found second footer start marker')
        # Find and remove it
        start = content.find('<footer>\n<a href="/">')
        end = content.find('</footer>', start) + 8
        remove = content[start:end]
        print('Will remove:', repr(remove[:100]))
        content = content[:start] + content[end:]
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print('SUCCESS - removed second footer')
    else:
        print('NOT FOUND')