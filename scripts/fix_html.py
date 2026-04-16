#!/usr/bin/env python3
"""Fix malformed article HTML files in morai.top and novelpick.top repos."""
import os, re, glob

SITES = {
    "morai": {
        "dir": r"C:\Users\Administrator\.openclaw\workspace\morai-website",
        "vars": """        :root {
            --bg: #060b14;
            --card: #111d2e;
            --border: #1a2a3a;
            --accent: #00d4ff;
            --accent-dim: rgba(0, 212, 255, 0.12);
            --text: #c8d4e0;
            --text-dim: #6a7a8a;
            --text-bright: #e8f0f8;
        }""",
        "fonts": """    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">""",
        "baidu": """<script>
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?d1d9d04b764a3f8f5a92e975825446e6";
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(hm, s);
})();
</script>""",
        "nav_logo": "&lt;morai/&gt;",
        "nav_links": [
            ("./ai-tools.html","AI Tools"),
            ("./ai-reviews.html","Reviews"),
            ("./ai-guides.html","Guides"),
            ("./ai-comparisons.html","Comparisons"),
        ],
    },
    "novelpick": {
        "dir": r"C:\Users\Administrator\.openclaw\workspace\novelpick-website",
        "vars": """        :root {
            --bg: #0d0a14;
            --card: #1a1424;
            --border: #2a2040;
            --accent: #c9a0dc;
            --accent-rose: #f0a0b0;
            --accent-dim: rgba(201, 160, 220, 0.12);
            --text: #b8a8c8;
            --text-dim: #7a6888;
            --text-bright: #ede0f5;
        }""",
        "fonts": """    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,800;1,700&family=Inter:wght@400;500;600;700&family=Lora:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">""",
        "baidu": """<script>
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?d6d20fb609876081e0de8872c69e39aa";
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(hm, s);
})();
</script>""",
        "nav_logo": "NovelPick",
        "nav_links": [
            ("./fantasy.html","Fantasy"),
            ("./litrpg.html","LitRPG"),
            ("./scifi.html","Sci-Fi"),
            ("./romance.html","Romance"),
        ],
    },
}

MORAI_CSS = """
        body { font-family: Inter, -apple-system, sans-serif; background: var(--bg); color: var(--text); line-height: 1.75; -webkit-font-smoothing: antialiased; }
        a { color: var(--accent); text-decoration: none; }
        a:hover { opacity: 0.8; }
        nav { position: fixed; top: 0; left: 0; right: 0; z-index: 100; background: rgba(6,11,20,0.92); backdrop-filter: blur(12px); border-bottom: 1px solid var(--border); padding: 0 2rem; }
        .nav-inner { max-width: 860px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; height: 60px; }
        .nav-logo { font-family: JetBrains Mono, monospace; font-weight: 700; font-size: 1.1rem; color: var(--accent); letter-spacing: -0.02em; }
        .nav-links { display: flex; gap: 1.8rem; list-style: none; }
        .nav-links a { font-size: 0.82rem; font-weight: 500; color: var(--text-dim); letter-spacing: 0.02em; transition: color 0.2s; }
        .nav-links a:hover, .nav-links a.active { color: var(--accent); }
        .progress-bar { position: fixed; top: 60px; left: 0; right: 0; height: 2px; z-index: 99; background: var(--border); }
        .progress-fill { height: 100%; background: var(--accent); width: 0%; transition: width 0.1s linear; }
        .article-container { max-width: 740px; margin: 0 auto; padding: 3rem 1.5rem 6rem; }
        .article-category { display: inline-flex; align-items: center; font-family: JetBrains Mono, monospace; font-size: 0.72rem; font-weight: 600; color: var(--accent); letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 1.2rem; }
        .article-category::before { content: ''; display: inline-block; width: 6px; height: 6px; background: var(--accent); border-radius: 50%; margin-right: 0.6rem; }
        .article-title { font-size: clamp(1.9rem, 4vw, 2.6rem); font-weight: 800; color: var(--text-bright); line-height: 1.18; letter-spacing: -0.025em; margin-bottom: 1rem; }
        .article-subtitle { font-size: 1.1rem; color: var(--text-dim); font-weight: 400; line-height: 1.6; margin-bottom: 1.8rem; }
        .article-meta { display: flex; align-items: center; gap: 1.2rem; padding: 1rem 0; border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); margin-bottom: 2.5rem; }
        .meta-item { display: flex; align-items: center; gap: 0.4rem; font-size: 0.82rem; color: var(--text-dim); font-family: JetBrains Mono, monospace; }
        .meta-sep { width: 1px; height: 14px; background: var(--border); }
        .article-lead { font-size: 1.08rem; color: var(--text); line-height: 1.8; margin-bottom: 2rem; padding-left: 1.2rem; border-left: 2px solid var(--accent); }
        .article-content h2 { font-size: 1.35rem; font-weight: 700; color: var(--text-bright); margin: 2.5rem 0 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border); }
        .article-content h3 { font-size: 1.1rem; font-weight: 600; color: var(--text-bright); margin: 1.8rem 0 0.6rem; }
        .article-content p { font-size: 0.97rem; color: var(--text); margin-bottom: 1.1rem; line-height: 1.8; }
        .article-content ul, .article-content ol { margin: 0.8rem 0 1.2rem 1.5rem; }
        .article-content li { font-size: 0.97rem; color: var(--text); margin-bottom: 0.4rem; line-height: 1.7; }
        .article-content strong { color: var(--text-bright); font-weight: 600; }
        .article-content a { color: var(--accent); }
        .article-content .meta { font-family: JetBrains Mono, monospace; font-size: 0.75rem; color: var(--text-dim); margin-bottom: 1.5rem; }
        .tool-card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; margin: 1.8rem 0; }
        .tool-card-name { font-size: 1.05rem; font-weight: 700; color: var(--text-bright); margin-bottom: 0.3rem; }
        .tool-card-meta { font-family: JetBrains Mono, monospace; font-size: 0.75rem; color: var(--accent); margin-bottom: 0.8rem; }
        .tool-card-best { font-size: 0.82rem; color: var(--text-dim); margin-bottom: 0.8rem; }
        .tool-card-pros-cons { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; font-size: 0.85rem; }
        .tool-pros strong, .tool-cons strong { }
        .tool-pros strong { color: #4ade80; }
        .tool-cons strong { color: #f87171; }
        .tool-pros, .tool-cons { margin: 0; list-style: none; }
        .tool-pros li, .tool-cons li { margin-bottom: 0.3rem; }
        .pros-box { background: rgba(74,222,128,0.08); border: 1px solid rgba(74,222,128,0.2); border-radius: 8px; padding: 1rem; margin: 0.8rem 0; }
        .cons-box { background: rgba(248,113,113,0.08); border: 1px solid rgba(248,113,113,0.2); border-radius: 8px; padding: 1rem; margin: 0.8rem 0; }
        .pros-box strong { color: #4ade80; }
        .cons-box strong { color: #f87171; }
        .pros-box p, .cons-box p { margin-bottom: 0.4rem; font-size: 0.9rem; }
        .pros-box p:last-child, .cons-box p:last-child { margin-bottom: 0; }
        .highlight-box, .verdict { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; margin: 1.8rem 0; }
        .highlight-box h3, .verdict h3 { font-size: 1rem; font-weight: 700; color: var(--accent); margin-bottom: 0.8rem; }
        .highlight-box p, .verdict p { font-size: 0.95rem; color: var(--text); margin-bottom: 0; }
        .related-articles { margin-top: 2.5rem; }
        .related-articles h3 { font-size: 1rem; font-weight: 700; color: var(--text-bright); margin-bottom: 1rem; }
        .related-grid { display: flex; flex-direction: column; gap: 0.8rem; }
        .related-card { background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 1rem; transition: border-color 0.2s; }
        .related-card:hover { border-color: var(--accent); }
        .related-card a { display: flex; align-items: center; gap: 0.8rem; }
        .related-tag { font-size: 0.7rem; font-weight: 600; color: var(--accent); letter-spacing: 0.06em; text-transform: uppercase; white-space: nowrap; }
        .related-title { font-size: 0.88rem; color: var(--text); }
        .related-card:hover .related-title { color: var(--text-bright); }
        .share-bar { position: fixed; left: 2rem; top: 50%; transform: translateY(-50%); display: flex; flex-direction: column; gap: 0.6rem; z-index: 90; }
        .share-btn { width: 38px; height: 38px; background: var(--card); border: 1px solid var(--border); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: var(--text-dim); font-size: 0.85rem; transition: all 0.2s; }
        .share-btn:hover { background: var(--accent-dim); border-color: var(--accent); color: var(--accent); }
        .article-footer { margin-top: 3rem; padding-top: 2rem; border-top: 1px solid var(--border); }
        .back-to-top { display: inline-flex; align-items: center; gap: 0.4rem; font-size: 0.82rem; color: var(--text-dim); padding: 0.5rem 0; }
        .back-to-top:hover { color: var(--accent); }
        @media (max-width: 768px) { .share-bar { display: none; } .article-container { padding: 2rem 1.2rem 4rem; } .tool-card-pros-cons { grid-template-columns: 1fr; } .nav-links { display: none; } }"""

NOVELPICK_CSS = """
        body { font-family: Inter, -apple-system, sans-serif; background: var(--bg); color: var(--text); line-height: 1.8; -webkit-font-smoothing: antialiased; }
        a { color: var(--accent); text-decoration: none; }
        a:hover { color: var(--accent-rose); }
        nav { position: fixed; top: 0; left: 0; right: 0; z-index: 100; background: rgba(13,10,20,0.92); backdrop-filter: blur(12px); border-bottom: 1px solid var(--border); padding: 0 2rem; }
        .nav-inner { max-width: 860px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; height: 60px; }
        .nav-logo { font-family: Playfair Display, serif; font-weight: 700; font-size: 1.3rem; color: var(--accent); letter-spacing: 0.01em; }
        .nav-links { display: flex; gap: 1.8rem; list-style: none; }
        .nav-links a { font-size: 0.82rem; font-weight: 500; color: var(--text-dim); letter-spacing: 0.03em; transition: color 0.2s; }
        .nav-links a:hover, .nav-links a.active { color: var(--accent); }
        .progress-bar { position: fixed; top: 60px; left: 0; right: 0; height: 2px; z-index: 99; background: var(--border); }
        .progress-fill { height: 100%; background: linear-gradient(90deg, var(--accent), var(--accent-rose)); width: 0%; transition: width 0.1s linear; }
        .article-container { max-width: 720px; margin: 0 auto; padding: 3rem 1.5rem 6rem; }
        .article-category { display: inline-flex; align-items: center; gap: 0.5rem; font-size: 0.72rem; font-weight: 600; color: var(--accent-rose); letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 1.2rem; }
        .article-title { font-family: Playfair Display, serif; font-size: clamp(2rem, 4.5vw, 2.8rem); font-weight: 700; color: var(--text-bright); line-height: 1.2; margin-bottom: 1.2rem; }
        .article-subtitle { font-family: Lora, serif; font-size: 1.05rem; color: var(--text-dim); font-style: italic; line-height: 1.65; margin-bottom: 2rem; }
        .article-meta { display: flex; align-items: center; gap: 1rem; padding: 1.2rem 0; border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); margin-bottom: 2.5rem; }
        .meta-item { display: flex; align-items: center; gap: 0.4rem; font-size: 0.82rem; color: var(--text-dim); }
        .meta-sep { width: 1px; height: 14px; background: var(--border); }
        .meta-rating { color: var(--accent-rose); }
        .article-cover { width: 100%; height: 280px; background: linear-gradient(135deg, #1a1230 0%, #2a1840 50%, #1a1230 100%); border-radius: 12px; margin-bottom: 2.5rem; display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden; }
        .article-cover::after { content: ''; position: absolute; inset: 0; background: radial-gradient(ellipse at 30% 50%, rgba(201,160,220,0.15) 0%, transparent 60%), radial-gradient(ellipse at 70% 50%, rgba(240,160,176,0.1) 0%, transparent 60%); }
        .cover-text { font-family: Playfair Display, serif; font-size: 2rem; font-style: italic; color: rgba(201,160,220,0.2); position: relative; z-index: 1; }
        .article-lead { font-family: Lora, serif; font-size: 1.08rem; color: var(--text); line-height: 1.8; margin-bottom: 2rem; padding-left: 1.2rem; border-left: 2px solid var(--accent); }
        .article-content p { font-size: 0.97rem; color: var(--text); margin-bottom: 1.3rem; line-height: 1.85; }
        .article-content h2 { font-family: Playfair Display, serif; font-size: 1.5rem; font-weight: 700; color: var(--text-bright); margin: 2.8rem 0 1rem; padding-bottom: 0.6rem; border-bottom: 1px solid var(--border); }
        .article-content h3 { font-family: Playfair Display, serif; font-size: 1.15rem; font-weight: 600; color: var(--accent); margin: 1.8rem 0 0.6rem; }
        .article-content strong { color: var(--text-bright); font-weight: 600; }
        .article-content ul, .article-content ol { margin: 0.8rem 0 1.2rem 1.5rem; }
        .article-content li { font-size: 0.97rem; color: var(--text); margin-bottom: 0.4rem; line-height: 1.7; }
        .novel-card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; margin: 1.8rem 0; position: relative; }
        .novel-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, var(--accent), var(--accent-rose)); border-radius: 12px 12px 0 0; }
        .novel-rank { font-family: Playfair Display, serif; font-size: 2.5rem; font-weight: 700; color: var(--border); position: absolute; top: 1rem; right: 1.2rem; }
        .novel-title { font-family: Playfair Display, serif; font-size: 1.15rem; font-weight: 700; color: var(--text-bright); margin-bottom: 0.3rem; padding-right: 3rem; }
        .novel-tags { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 0.8rem; }
        .tag { font-size: 0.7rem; font-weight: 600; padding: 0.2rem 0.6rem; border-radius: 50px; letter-spacing: 0.04em; }
        .tag-platform { background: var(--accent-dim); color: var(--accent); border: 1px solid rgba(201,160,220,0.2); }
        .tag-status { background: rgba(240,160,176,0.1); color: var(--accent-rose); border: 1px solid rgba(240,160,176,0.2); }
        .tag-genre { background: rgba(160,200,255,0.08); color: #a0c8ff; border: 1px solid rgba(160,200,255,0.15); }
        .novel-desc { font-size: 0.9rem; color: var(--text); line-height: 1.7; font-family: Lora, serif; }
        .pros-box { background: rgba(74,222,128,0.08); border: 1px solid rgba(74,222,128,0.2); border-radius: 8px; padding: 1rem; margin: 0.8rem 0; }
        .cons-box { background: rgba(248,113,113,0.08); border: 1px solid rgba(248,113,113,0.2); border-radius: 8px; padding: 1rem; margin: 0.8rem 0; }
        .pros-box strong { color: #4ade80; }
        .cons-box strong { color: #f87171; }
        .pros-box p, .cons-box p { margin-bottom: 0.4rem; font-size: 0.9rem; }
        .pros-box p:last-child, .cons-box p:last-child { margin-bottom: 0; }
        .rating-box { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; margin: 1.8rem 0; }
        .rating-box h3 { font-family: Playfair Display, serif; font-size: 1rem; font-weight: 700; color: var(--accent); margin-bottom: 1rem; }
        .related-articles { margin-top: 2.5rem; }
        .related-articles h3 { font-family: Playfair Display, serif; font-size: 1.1rem; font-weight: 700; color: var(--text-bright); margin-bottom: 1rem; }
        .related-grid { display: flex; flex-direction: column; gap: 0.8rem; }
        .related-card { background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 1rem; transition: border-color 0.2s; }
        .related-card:hover { border-color: var(--accent); }
        .related-card a { display: flex; align-items: center; gap: 0.8rem; }
        .related-tag { font-size: 0.7rem; font-weight: 600; color: var(--accent-rose); letter-spacing: 0.06em; text-transform: uppercase; white-space: nowrap; }
        .related-title { font-size: 0.88rem; color: var(--text); }
        .related-card:hover .related-title { color: var(--text-bright); }
        .share-bar { position: fixed; left: 2rem; top: 50%; transform: translateY(-50%); display: flex; flex-direction: column; gap: 0.6rem; z-index: 90; }
        .share-btn { width: 38px; height: 38px; background: var(--card); border: 1px solid var(--border); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: var(--text-dim); font-size: 0.85rem; transition: all 0.2s; }
        .share-btn:hover { background: var(--accent-dim); border-color: var(--accent); color: var(--accent); }
        .article-footer { margin-top: 3rem; padding-top: 2rem; border-top: 1px solid var(--border); }
        .back-to-top { display: inline-flex; align-items: center; gap: 0.4rem; font-size: 0.82rem; color: var(--text-dim); }
        .back-to-top:hover { color: var(--accent); }
        @media (max-width: 768px) { .share-bar { display: none; } .article-container { padding: 2rem 1.2rem 4rem; } .nav-links { display: none; } }"""

PROGRESS_SCRIPT = """<script>
        window.addEventListener('scroll', function() {
            var el = document.getElementById('progressFill');
            if (!el) return;
            var scrollTop = window.scrollY;
            var docHeight = document.documentElement.scrollHeight - window.innerHeight;
            var pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
            el.style.width = pct + '%';
        });
    </script>"""


def has_duplicate_heads(c):
    return c.count('<head>') >= 2


def has_scripts_in_head(c):
    s = c.find('</style>')
    h = c.find('</head>')
    if s == -1 or h == -1:
        return False
    return '<script' in c[s:h]


def parse_dup_head(c):
    fh = c.find('<head>')
    sh = c.find('<head>', fh + 1)
    fc = c.find('</head>')
    # Meta from BOTH sections:
    # 1. From first <head> to second <head>: charset, viewport, canonical, fonts
    first_meta_block = c[fh + 6:sh]
    # 2. From second <head> to first </head>: og tags, twitter tags, title, description
    second_meta_block = c[sh + 6:fc].strip()
    # Extract meta/link/title from both blocks
    first_tags = [ln.strip() for ln in first_meta_block.split('\n')
                  if ln.strip().startswith(('<meta ', '<link '))]
    second_tags = [ln.strip() for ln in second_meta_block.split('\n')
                   if ln.strip().startswith(('<meta ', '<title>', '<link '))]
    meta_tags = first_tags + second_tags
    # CSS is the orphaned <style> block after first </head>
    ss = c.find('<style>', fc)
    se = c.find('</style>', ss)
    css = c[ss:se + 8]
    # Body starts after the orphaned </head> (which follows </style>)
    oh = c.find('</head>', se)
    bs = c.find('<body>', oh)
    be_tag = c.find('>', bs) + 1
    be = c.rfind('</body>')
    if be == -1:
        be = len(c)
    body = c[be_tag:be].strip()
    scripts = re.findall(r'<script[^>]*>.*?</script>', body, re.DOTALL)
    for s in scripts:
        body = body.replace(s, '\n__SP__\n')
    # Strip nav and breadcrumb that appear after </header> (duplicate site nav in article)
    header_end = body.find('</header>')
    if header_end != -1:
        body_after_header = body[header_end:]
        nav_in_after = body_after_header.find('<nav>')
        if nav_in_after != -1:
            nav_end = body_after_header.find('</nav>', nav_in_after) + len('</nav>')
            body = body[:header_end] + body_after_header[nav_end:]
        breadcrumb_in_after = body.find('<div class="breadcrumb">')
        if breadcrumb_in_after != -1:
            breadcrumb_end = body.find('</div>', breadcrumb_in_after) + len('</div>')
            body = body[:breadcrumb_in_after] + body[breadcrumb_end:]
    return {'meta_tags': meta_tags, 'css': css, 'body': body.strip(), 'scripts': scripts}


def parse_scripts_in_head(c):
    hs = c.find('<head>')
    hc = c.find('</head>')
    ss = c.find('<style>', hs)
    # Meta tags: between <head> and <style>
    meta_block = c[hs + 6:ss].strip()
    meta_tags = [ln.strip() for ln in meta_block.split('\n')
                 if ln.strip().startswith(('<meta ', '<title>', '<link '))]
    se = c.find('</style>', ss)
    css = c[ss:se + 8]
    # Scripts: between </style> and </head>
    scripts = re.findall(r'<script[^>]*>.*?</script>', c[se:hc], re.DOTALL)
    bs = c.find('<body>', hc)
    be_tag = c.find('>', bs) + 1
    be = c.rfind('</body>')
    if be == -1:
        be = len(c)
    body = c[be_tag:be].strip()
    # Strip nav and breadcrumb that appear after </header> (duplicate site nav in article)
    header_end = body.find('</header>')
    if header_end != -1:
        bah = body[header_end:]
        ni = bah.find('<nav>')
        if ni != -1:
            ne = bah.find('</nav>', ni) + len('</nav>')
            body = body[:header_end] + bah[ne:]
        bi = body.find('<div class="breadcrumb">')
        if bi != -1:
            be2 = body.find('</div>', bi) + len('</div>')
            body = body[:bi] + body[be2:]
    return {'meta_tags': meta_tags, 'css': css, 'body': body.strip(), 'scripts': scripts}


def dedup_meta(tags):
    seen, out = [], []
    for t in tags:
        if 'property="' in t:
            k = re.search(r'property="([^"]+)"', t)
            key = k.group(1) if k else t
        elif 'name="' in t:
            k = re.search(r'name="([^"]+)"', t)
            key = k.group(1) if k else t
        elif 'charset="' in t or 'viewport' in t:
            key = t
        else:
            key = t
        if key not in seen:
            seen.append(key)
            out.append(t)
    return out


def build_html(site, parsed):
    cfg = SITES[site]
    css = MORAI_CSS if site == 'morai' else NOVELPICK_CSS
    # Meta tags: og, twitter, description, keywords (exclude charset/viewport - added below)
    og_tags = [t.strip() for t in parsed['meta_tags']
               if t.startswith('<meta ') and 'charset' not in t and 'viewport' not in t]
    canonical_tags = [t.strip() for t in parsed['meta_tags'] if 'canonical' in t]
    # Build meta block: charset, viewport, og, canonical
    parts = ['    <meta charset="UTF-8">',
             '    <meta name="viewport" content="width=device-width, initial-scale=1.0">']
    parts.extend('    ' + t for t in og_tags)
    parts.extend('    ' + t for t in canonical_tags)
    meta_html = '\n'.join(parts)
    nav_html = '\n'.join(
        f'                <li><a href="{h}">{l}</a></li>'
        for h, l in cfg['nav_links']
    )
    scripts_html = '\n'.join(parsed['scripts'])
    vars_css = SITES[site]['vars']
    fonts_html = cfg['fonts']
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
{meta_html}
{fonts_html}
    <style>
{vars_css}
{css}
    </style>
</head>
<body>
<nav>
        <div class="nav-inner">
            <a href="./index.html" class="nav-logo">{cfg['nav_logo']}</a>
            <ul class="nav-links">
{nav_html}
            </ul>
        </div>
    </nav>
<div class="progress-bar"><div class="progress-fill" id="progressFill"></div>
{parsed['body']}
{PROGRESS_SCRIPT}
{scripts_html}
{cfg['baidu']}
</body>
</html>'''


def _read_file(fpath):
    # Check for UTF-16 BOM first
    with open(fpath, 'rb') as f:
        raw = f.read()
    if raw.startswith(b'\xff\xfe') or raw.startswith(b'\xfe\xff'):
        # UTF-16 file - convert to UTF-8
        try:
            return raw.decode('utf-16').encode('utf-8').decode('utf-8')
        except Exception:
            pass
    # Try standard encodings
    for enc in ['utf-8-sig', 'utf-8', 'cp1252']:
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode('utf-8', errors='replace')

def _normalize(c):
    return c.replace('\r\n', '\n').replace('\r', '\n')



def fix_file(fpath, site):
    c = _normalize(_read_file(fpath))
    dup = has_duplicate_heads(c)
    sin = has_scripts_in_head(c)
    if not dup and not sin:
        print(f'  clean: {os.path.basename(fpath)}')
        return False
    if dup:
        p = parse_dup_head(c)
    elif sin:
        p = parse_scripts_in_head(c)
    else:
        return False
    new_html = build_html(site, p)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f'  FIXED: {os.path.basename(fpath)}')
    return True


MORAI_FILES = [
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
]

NOVELPICK_FILES = [
    'best-action-fantasy-web-novels-2026.html',
    'best-apocalypse-and-survival-novels.html',
    'best-apocalypse-survival-web-novels.html',
    'best-cozy-fantasy-novels.html',
    'best-cyberpunk-novels.html',
    'best-dark-fantasy-novels.html',
    'best-enemies-to-lovers-romance-novels.html',
    'best-germinator-novels.html',
    'best-historical-fantasy-novels.html',
    'best-litrpg-novels.html',
    'best-progression-fantasy-novels.html',
    'best-reincarnation-novels.html',
    'best-science-fantasy-novels.html',
    'best-solo-leveling-novels.html',
    'best-space-opera-novels-2026.html',
    'best-space-opera-novels.html',
    'best-system-apocalypse-novels.html',
    'best-time-loop-web-novels-2026.html',
    'best-time-travel-novels.html',
    'best-urban-fantasy-novels-2026-v2.html',
    'best-urban-fantasy-novels-2026.html',
    'best-urban-fantasy-novels.html',
    'best-wholesome-and-comfort-reads.html',
    'best-xianxia-cultivation-novels.html',
    'books-like-cradle.html',
    'books-like-harry-potter.html',
    'books-like-lord-of-the-rings.html',
    'books-like-mistborn.html',
    'books-like-percy-jackson.html',
    'shadow-slave-review.html',
    'shadow-slave-vs-legendary-mechanic.html',
    'solo-leveling-inspired-novels.html',
    'solo-leveling-vs-shadow-slave.html',
]


def main():
    total_fixed = total_err = 0
    for site, files in [('morai', MORAI_FILES), ('novelpick', NOVELPICK_FILES)]:
        cfg = SITES[site]
        fixed = err = 0
        for fn in files:
            fp = os.path.join(cfg['dir'], fn)
            if not os.path.exists(fp):
                continue
            ok = fix_file(fp, site)
            if ok is True:
                fixed += 1
            elif ok is None:
                err += 1
        print(f'{site}: fixed={fixed}, err={err}')
        total_fixed += fixed
        total_err += err
    print(f'TOTAL: fixed={total_fixed}, err={total_err}')


if __name__ == '__main__':
    main()
