#!/usr/bin/env python3
"""Force-rebuild all HTML files with fixed parsers."""
import re, glob, os, sys

# Import fix_html
sys.path.insert(0, r'C:\Users\Administrator\.openclaw\workspace\scripts')
import importlib.util
spec = importlib.util.spec_from_file_location("fix_html", r'C:\Users\Administrator\.openclaw\workspace\scripts\fix_html.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def _rf(p):
    with open(p, 'rb') as f:
        raw = f.read()
    if raw.startswith(b'\xff\xfe') or raw.startswith(b'\xfe\xff'):
        return raw.decode('utf-16').encode('utf-8').decode('utf-8')
    for enc in ['utf-8-sig', 'utf-8', 'cp1252']:
        try: return raw.decode(enc)
        except: continue
    return raw.decode('utf-8', errors='replace')

def _norm(c):
    return c.replace('\r\n', '\n').replace('\r', '\n')

def _strip_nav_breadcrumb(body):
    """Strip duplicate nav and breadcrumb from article body content."""
    header_end = body.find('</header>')
    if header_end == -1:
        return body
    bah = body[header_end:]
    ni = bah.find('<nav>')
    if ni != -1:
        ne = bah.find('</nav>', ni) + len('</nav>')
        bah = bah[ne:]
    bi = bah.find('<div class="breadcrumb">')
    if bi != -1:
        be2 = bah.find('</div>', bi) + len('</div>')
        bah = bah[:bi] + bah[be2:]
    return body[:header_end] + bah

def force_fix(fpath, site):
    c = _norm(_rf(fpath))
    if c.count('<head>') >= 2:
        p = mod.parse_dup_head(c)
    else:
        p = mod.parse_scripts_in_head(c)
    # Strip nav/breadcrumb from body
    p['body'] = _strip_nav_breadcrumb(p['body'])
    new_html = mod.build_html(site, p)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f'  REBUILT: {os.path.basename(fpath)}')

for site, files in [
    ('morai', [
        'best-ai-agents-2026.html','best-ai-chatbots-2026.html',
        'best-ai-coding-assistants-2026.html','best-ai-coding-tools-2026.html',
        'best-ai-design-tools-2026.html','best-ai-email-tools-2026.html',
        'best-ai-image-editors-2026.html','best-ai-image-generators-2026-comparison.html',
        'best-ai-marketing-tools-2026.html','best-ai-meeting-tools-2026.html',
        'best-ai-note-taking-tools-2026.html','best-ai-productivity-tools-2026.html',
        'best-ai-research-assistants-2026.html','best-ai-seo-tools-2026.html',
        'best-ai-tools-2026.html','best-ai-translation-tools-2026.html',
        'best-ai-video-editing-tools-2026.html','best-ai-voice-cloning-tools-2026.html',
        'best-free-ai-tools-2026.html','chatgpt-vs-claude-vs-gemini-2026.html',
        'chatgpt-vs-claude.html','claude-3-7-sonnet-review.html',
        'cursor-ai-review.html','how-ai-agents-transform-knowledge-work-2026.html',
        'ai-agent-tools-2026.html','ai-agents-for-beginners-guide.html',
        'ai-code-review-complete-guide-2026.html','ai-code-review-tools.html',
        'ai-for-small-business-guide.html','ai-image-generators.html',
        'ai-writing-tools.html',
    ]),
    ('novelpick', [
        'best-action-fantasy-web-novels-2026.html','best-apocalypse-and-survival-novels.html',
        'best-apocalypse-survival-web-novels.html','best-cozy-fantasy-novels.html',
        'best-cyberpunk-novels.html','best-dark-fantasy-novels.html',
        'best-enemies-to-lovers-romance-novels.html','best-germinator-novels.html',
        'best-historical-fantasy-novels.html','best-litrpg-novels.html',
        'best-progression-fantasy-novels.html','best-reincarnation-novels.html',
        'best-science-fantasy-novels.html','best-solo-leveling-novels.html',
        'best-space-opera-novels-2026.html','best-space-opera-novels.html',
        'best-system-apocalypse-novels.html','best-time-loop-web-novels-2026.html',
        'best-time-travel-novels.html','best-urban-fantasy-novels-2026-v2.html',
        'best-urban-fantasy-novels-2026.html','best-urban-fantasy-novels.html',
        'best-wholesome-and-comfort-reads.html','best-xianxia-cultivation-novels.html',
        'books-like-cradle.html','books-like-harry-potter.html',
        'books-like-lord-of-the-rings.html','books-like-mistborn.html',
        'books-like-percy-jackson.html','shadow-slave-review.html',
        'shadow-slave-vs-legendary-mechanic.html','solo-leveling-inspired-novels.html',
        'solo-leveling-vs-shadow-slave.html',
    ]),
]:
    base = r'C:\Users\Administrator\.openclaw\workspace\morai-website' if site == 'morai' else r'C:\Users\Administrator\.openclaw\workspace\novelpick-website'
    print(f'=== {site.upper()} ===')
    for fn in files:
        fp = os.path.join(base, fn)
        if os.path.exists(fp):
            force_fix(fp, site)
        else:
            print(f'  MISSING: {fn}')
    print()
