with open(r'C:\Users\Administrator\.openclaw\workspace\fateandmethod-website\five-elements-wu-xing-guide.html','r',encoding='utf-8') as f:
    html = f.read()

opens = html.count('<div')
closes = html.count('</div>')
print('DIVs: open=%d, close=%d, balanced=%s' % (opens, closes, opens==closes))

amp_correct = '&amp;' in html
raw_amp = '&amp;' not in html.replace('&amp;','')
print('All ampersands escaped as &amp;: %s' % amp_correct)

print('File size: %d bytes' % len(html))

checks = [
    ('Baidu tracking', 'hm.js?7a310f3a5b54d3c8565e5669ffb815a5' in html),
    ('og:site_name', 'og:site_name' in html),
    ('canonical', 'canonical' in html),
    ('sidebar toc', 'toc-list' in html),
    ('compat table', 'compat-table' in html),
    ('related section', 'related-section' in html),
    ('breadcrumb', 'breadcrumb' in html),
    ('nav logo FATE', 'FATE &amp; METHOD' in html),
    ('H1 em tag', '<em>Wu Xing</em>' in html),
    ('Eyebrow', 'CHINESE METAPHYSICS' in html),
    ('bazi-beginners link', 'bazi-beginners-complete-guide.html' in html),
    ('kua-number link', 'kua-number-complete-guide.html' in html),
]
for name, result in checks:
    print('%s: %s' % (name, result))