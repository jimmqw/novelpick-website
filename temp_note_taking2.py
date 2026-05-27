content = open(r'C:\Users\Administrator\github\morai-website\best-ai-note-taking-tools-2026.html', 'rb').read()

# The file has <main> but no </main>. We need to add it.
# Insert </main> before <aside class="sidebar">
old = b'</div>\r\n\r\n<aside class="sidebar">'
new = b'</div>\r\n</main>\r\n\r\n<aside class="sidebar">'
if old in content:
    content = content.replace(old, new)
    open(r'C:\Users\Administrator\github\morai-website\best-ai-note-taking-tools-2026.html', 'wb').write(content)
    print('Added </main> tag')
else:
    print('Pattern not found')
    idx = content.find(b'<aside class="sidebar">')
    print('sidebar at:', idx)
    print('Before sidebar:', repr(content[idx-50:idx]))
