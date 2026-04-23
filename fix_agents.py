path = r'C:\Users\Administrator\.openclaw\workspace\morai.top\best-ai-agents-2026.html'
with open(path, encoding='utf-8', errors='replace') as f:
    c = f.read()

old = '<div class="prev-next">\n<div class="prev-article"><span class="pn-label">&lt;- Previous</span><a href="/best-ai-image-generators-2026-comparison.html">Best AI Image Generators 2026</a></div>\n<div class="next-article"><span class="pn-label">Next -&gt;</span><a href="/best-ai-video-generation-tools-2026.html">Best AI Video Generation Tools 2026</a></div>\n</div>'
new = '<div class="prev-next">\n<div class="prev-article"><span class="pn-label">&lt;- Previous</span><a href="/github-copilot-review-2026.html">GitHub Copilot Review 2026</a></div>\n<div class="next-article"><span class="pn-label">Next -&gt;</span><a href="/best-ai-video-generation-tools-2026.html">Best AI Video Generation Tools 2026</a></div>\n</div>'

if old in c:
    c = c.replace(old, new, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print('Fixed!')
else:
    print('Still not found - checking line endings')
    # Try with different line endings
    old2 = old.replace('\n', '\n')
    idx = c.find('<div class="prev-next">')
    print(repr(c[idx:idx+300]))
