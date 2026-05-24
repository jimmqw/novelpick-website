import re

# Fix best-ai-agents-2026.html prev-next
path1 = r'C:\Users\Administrator\.openclaw\workspace\morai.top\best-ai-agents-2026.html'
with open(path1, encoding='utf-8', errors='replace') as f:
    c1 = f.read()

old1 = '<div class="prev-next">\n<div class="prev-article"><span class="pn-label">&lt;- Previous</span><a href="/best-ai-video-generation-tools-2026.html">Best AI Video Generation Tools 2026</a></div>\n<div class="next-article"><span class="pn-label">Next -&gt;</span><a href="/best-ai-agents-2026.html">Best AI Agents 2026</a></div>\n</div>'
new1 = '<div class="prev-next">\n<div class="prev-article"><span class="pn-label">&lt;- Previous</span><a href="/best-ai-video-generation-tools-2026.html">Best AI Video Generation Tools 2026</a></div>\n<div class="next-article"><span class="pn-label">Next -&gt;</span><a href="/github-copilot-review-2026.html">GitHub Copilot Review 2026</a></div>\n</div>'

if old1 in c1:
    c1 = c1.replace(old1, new1, 1)
    with open(path1, 'w', encoding='utf-8') as f:
        f.write(c1)
    print('Fixed best-ai-agents-2026.html')
else:
    print('Pattern not found in best-ai-agents-2026.html')
    # Try to find what's there
    idx = c1.find('prev-next')
    print(repr(c1[idx:idx+200]))

# Fix best-ai-video-generation-tools-2026.html prev-next
path2 = r'C:\Users\Administrator\.openclaw\workspace\morai.top\best-ai-video-generation-tools-2026.html'
with open(path2, encoding='utf-8', errors='replace') as f:
    c2 = f.read()

old2 = '<div class="prev-next">\n<div class="prev-article"><span class="pn-label">&lt;- Previous</span><a href="/best-ai-image-generators-2026-comparison.html">Best AI Image Generators 2026</a></div>\n<div class="next-article"><span class="pn-label">Next -&gt;</span><a href="/best-ai-agents-2026.html">Best AI Agents 2026</a></div>\n</div>'
new2 = '<div class="prev-next">\n<div class="prev-article"><span class="pn-label">&lt;- Previous</span><a href="/best-ai-agents-2026.html">Best AI Agents 2026</a></div>\n<div class="next-article"><span class="pn-label">Next -&gt;</span><a href="/github-copilot-review-2026.html">GitHub Copilot Review 2026</a></div>\n</div>'

if old2 in c2:
    c2 = c2.replace(old2, new2, 1)
    with open(path2, 'w', encoding='utf-8') as f:
        f.write(c2)
    print('Fixed best-ai-video-generation-tools-2026.html')
else:
    print('Pattern not found in best-ai-video-generation-tools-2026.html')
    idx = c2.find('prev-article')
    print(repr(c2[idx:idx+200]))
