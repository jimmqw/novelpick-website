# Fix fateandmethod.com SEO — add Baidu + og:site_name to article pages missing both
import os

BAIDU = '<script>var _hmt=_hmt||[];(function(){var hm=document.createElement("script");hm.src="https://hm.baidu.com/hm.js?7a310f3a5b54d3c8565e5669ffb815a5";var s=document.getElementsByTagName("script")[0];s.parentNode.insertBefore(hm,s);})();</script>'
dir = r'C:\Users\Administrator\.openclaw\workspace\fateandmethod.com'

# Skip these — low value for tracking
skip = {'index.html', 'about.html', 'contact.html', 'privacy.html'}

files = [f for f in os.listdir(dir) if f.endswith('.html') and f not in skip]
fixed = 0
for fname in files:
    fp = os.path.join(dir, fname)
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()
    
    changes = []
    if 'hm.baidu.com' not in c:
        c = c.replace('</head>', BAIDU + '\n</head>')
        changes.append('+baidu')
    if 'og:site_name' not in c:
        c = c.replace('</head>', '<meta property="og:site_name" content="Fate and Method">\n</head>')
        changes.append('+og')
    
    if changes:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f'FIXED: {fname} — {" ".join(changes)}')
        fixed += 1
    else:
        print(f'OK:   {fname}')

print(f'\nTotal fixed: {fixed}/{len(files)} files')