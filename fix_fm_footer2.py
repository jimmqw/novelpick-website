fpath = r'C:\Users\Administrator\.openclaw\workspace\fateandmethod-website\index.html'
with open(fpath, 'r', encoding='utf-8') as f:
    content = f.read()

# Check the structure
idx_body = content.find('</body>')
idx_footer1 = content.find('<footer class="footer">')
idx_footer2 = content.find('<footer>')

print('</body> at:', idx_body)
print('footer.classic at:', idx_footer1)
print('footer (second) at:', idx_footer2)
print()

# Print context around second footer
if idx_footer2 >= 0:
    print('Context around second footer:')
    print(repr(content[idx_footer2-100:idx_footer2+300]))
    print()
    print('Context around first footer:')
    print(repr(content[idx_footer1-100:idx_footer1+200]))

# Remove the second footer
if idx_footer2 > idx_body:
    # Second footer is after </body>, safe to remove
    old = content[idx_footer2-3:content.find('</footer>', idx_footer2)+8]
    print('Will remove:', repr(old))
    content = content.replace(old, '', 1)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Removed second footer')
else:
    print('Second footer is INSIDE body - need careful handling')