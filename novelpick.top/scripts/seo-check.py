import re, os

sites = {
    'morai': r'C:\Users\Administrator\github\morai-site',
    'novelpick': r'C:\Users\Administrator\github\novelpick-site',
}

high_priority = [
    'best-ai-agents-2026.html',
    'best-ai-coding-assistants-2026.html',
    'best-ai-chatbots-2026.html',
    'best-ai-image-generators-2026-comparison.html',
    'best-ai-coding-tools-2026.html',
    'claude-3-7-sonnet-review.html',
    'cursor-ai-review.html',
    'chatgpt-vs-claude.html',
    'best-solo-leveling-novels.html',
    'best-cultivation-novels-2026.html',
    'best-reincarnation-web-novels-2026.html',
    'books-like-solo-leveling.html',
    'best-urban-fantasy-novels-2026-v2.html',
]

for site, path in sites.items():
    print(f"\n=== {site} ===")
    for fname in high_priority:
        fpath = os.path.join(path, fname)
        if not os.path.exists(fpath):
            continue
        content = open(fpath, encoding='utf-8', errors='ignore').read()
        has_og = 'og:image' in content
        og_val = ''
        if has_og:
            m = re.search(r'og:image.*?content="([^"]+)"', content)
            if m:
                og_val = m.group(1)
        print(f"  {fname}: og:image={'YES: '+og_val if has_og else 'MISSING'}")
