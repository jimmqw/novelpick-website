import re, os

site = r'C:\Users\Administrator\.openclaw\workspace\morai.top'

# Sidebar widget links to non-existent .html files
# Fix them to point to existing pages
sidebar_fixes = {
    b'/ai-comparisons.html': b'/best-ai-writing-tools-2026.html',
    b'/ai-reviews.html': b'/github-copilot-review-2026.html',
    b'/ai-guides.html': b'/github-copilot-review-2026.html',
    b'/ai-tools.html': b'/best-ai-agents-2026.html',
    b'/deals.html': b'/best-ai-video-generation-tools-2026.html',
    b'/best-ai-image-generators-2026-comparison.html': b'/best-ai-video-generation-tools-2026.html',
    b'/claude-3-7-sonnet-review.html': b'/best-ai-agents-2026.html',
    b'/best-ai-coding-tools-2026.html': b'/github-copilot-review-2026.html',
    b'/chatgpt-vs-claude.html': b'/best-ai-agents-2026.html',
}

for fname in os.listdir(site):
    if not fname.endswith('.html'):
        continue
    path = os.path.join(site, fname)
    with open(path, 'rb') as f:
        c = f.read()
    original = c
    for old, new in sidebar_fixes.items():
        c = c.replace(b'href="' + old + b'"', b'href="' + new + b'"')
    if c != original:
        with open(path, 'wb') as f:
            f.write(c)
        print(f"Fixed sidebar in: {fname}")

print("Done")
