#!/usr/bin/env python3
"""Fix malformed article HTML files — collapses duplicate <head> + orphaned </head>."""

import os, re, glob

# ── Site configurations ──────────────────────────────────────────────────────

SITES = {
    "morai": {
        "dir":        r"C:\Users\Administrator\.openclaw\workspace\morai-website",
        "vars":       """        :root {
            --bg: #060b14;
            --card: #111d2e;
            --border: #1a2a3a;
            --accent: #00d4ff;
            --accent-dim: rgba(0, 212, 255, 0.12);
            --text: #c8d4e0;
            --text-dim: #6a7a8a;
            --text-bright: #e8f0f8;
        }""",
        "fonts":      """    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">""",
        "baidu":      """<script>
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?d1d9d04b764a3f8f5a92e975825446e6";
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(hm, s);
})();
</script>""",
        "nav_logo":   "&lt;morai/&gt;",
        "nav_links":  [
            ("./ai-tools.html",      "AI Tools"),
            ("./ai-reviews.html",    "Reviews"),
            ("./ai-guides.html",     "Guides"),
            ("./ai-comparisons.html","Comparisons"),
        ],
    },
    "novelpick": {
        "dir":        r"C:\Users\Administrator\.openclaw\workspace\novelpick-website",
        "vars":       """        :root {
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
        "fonts":      """    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,800;1,700&family=Inter:wght@400;500;600;700&family=Lora:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">""",
        "baidu":      """<script>
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?d6d20fb609876081e0de8872c69e39aa";
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(hm, s);
})();
</script>""",
        "nav_logo":   "NovelPick",
        "nav_links":  [
            ("./fantasy.html", "Fantasy"),
            ("./litrpg.html",  "LitRPG"),
            ("./scifi.html",   "Sci-Fi"),
            ("./romance.html", "Romance"),
        ],
    },
}

# ── Complete CSS for each site ───────────────────────────────────────────────

MORAI_CSS = """
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.75;
            -webkit-font-smoothing: antialiased;
        }
        a { color: var(--accent); text-decoration: none; }
        a:hover { opacity: 0.8; }

        nav {
            position: fixed; top: 0; left: 0; right: 0; z-index: 100;
            background: rgba(6, 11, 20, 0.92);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border);
            padding: 0 2rem;
        }
        .nav-inner {
            max-width: 860px; margin: 0 auto;
            display: flex; align-items: center; justify-content: space-between;
            height: 60px;
        }
        .nav-logo {
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700; font-size: 1.1rem;
            color: var(--accent); letter-spacing: -0.02em;
        }
        .nav-links { display: flex; gap: 1.8rem; list-style: none; }
        .nav-links a {
            font-size: 0.82rem; font-weight: 500;
            color: var(--text-dim); letter-spacing: 0.02em;
            transition: color 0.2s;
        }
        .nav-links a:hover, .nav-links a.active { color: var(--accent); }

        .progress-bar {
            position: fixed; top: 60px; left: 0; right: 0; height: 2px; z-index: 99;
            background: var(--border);
        }
        .progress-fill {
            height: 100%; background: var(--accent);
            width: 0%; transition: width 0.1s linear;
        }

        .article-container {
            max-width: 740px; margin: 0 auto;
            padding: 3rem 1.5rem 6rem;
        }

        .article-category {
            display: inline-flex; align-items: center;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem; font-weight: 600;
            color: var(--accent); letter-spacing: 0.08em; text-transform: uppercase;
            margin-bottom: 1.2rem;
        }
        .article-category::before {
            content: '';
            display: inline-block; width: 6px; height: 6px;
            background: var(--accent); border-radius: 50%;
            margin-right: 0.6rem;
        }

        .article-title {
            font-size: clamp(1.9rem, 4vw, 2.6rem);
            font-weight: 800; color: var(--text-bright);
            line-height: 1.18; letter-spacing: -0.025em;
            margin-bottom: 1rem;
        }
        .article-subtitle {
            font-size: 1.1rem; color: var(--text-dim);
            font-weight: 400; line-height: 1.6;
            margin-bottom: 1.8rem;
        }

        .article-meta {
            display: flex; align-items: center; gap: 1.2rem;
            padding: 1rem 0;
            border-top: 1px solid var(--border);
            border-bottom: 1px solid var(--border);
            margin-bottom: 2.5rem;
        }
        .meta-item {
            display: flex; align-items: center; gap: 0.4rem;
            font-size: 0.82rem; color: var(--text-dim);
            font-family: 'JetBrains Mono', monospace;
        }
        .meta-sep { width: 1px; height: 14px; background: var(--border); }

        .article-lead {
            font-size: 1.08rem; color: var(--text);
            line-height: 1.8; margin-bottom: 2rem;
            padding-left: 1.2rem; border-left: 2px solid var(--accent);
        }

        .article-content h2 {
            font-size: 1.35rem; font-weight: 700;
            color: var(--text-bright);
            margin: 2.5rem 0 1rem; padding-bottom: 0.5rem;
            border-bottom: 1px solid var(--border);
        }
        .article-content h3 {
            font-size: 1.1rem; font-weight: 600;
            color: var(--text-bright); margin: 1.8rem 0 0.6rem;
        }
        .article-content p {
            font-size: 0.97rem; color: var(--text);
            margin-bottom: 1.1rem; line-height: 1.8;
        }
        .article-content ul, .article-content ol { margin: 0.8rem 0 1.2rem 1.5rem; }
        .article-content li {
            font-size: 0.97rem; color: var(--text);
            margin-bottom: 0.4rem; line-height: 1.7;
        }
        .article-content strong { color: var(--text-bright); font-weight: 600; }
        .article-content a { color: var(--accent); }
        .article-content .meta {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem; color: var(--text-dim);
            margin-bottom: 1.5rem;
        }

        .tool-card {
            background: var(--card); border: 1px solid var(--border);
            border-radius: 12px; padding: 1.5rem; margin: 1.8rem 0;
        }
        .tool-card-name {
            font-size: 1.05rem; font-weight: 700;
            color: var(--text-bright); margin-bottom: 0.3rem;
        }
        .tool-card-meta {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem; color: var(--accent); margin-bottom: 0.8rem;
        }
        .tool-card-best { font-size: 0.82rem; color: var(--text-dim); margin-bottom: 0.8rem; }
        .tool-card-pros-cons {
            display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; font-size: 0.85rem;
        }
        .tool-pros strong { color: #4ade80; }
        .tool-cons strong { color: #f87171; }
        .tool-pros, .tool-cons { margin: 0; list-style: none; }
        .tool-pros li, .tool-cons li { margin-bottom: 0.3rem; }

        .pros-box {
            background: rgba(74, 222, 128, 0.08);
            border: 1px solid rgba(74, 222, 128, 0.2);
            border-radius: 8px; padding: 1rem; margin: 0.8rem 0;
        }
        .cons-box {
            background: rgba(248, 113, 113, 0.08);
            border: 1px solid rgba(248, 113, 113, 0.2);
            border-radius: 8px; padding: 1rem; margin: 0.8rem 0;
        }
        .pros-box strong { color: #4ade80; }
        .cons-box strong { color: #f87171; }
        .pros-box p, .cons-box p { margin-bottom: 0.4rem; font-size: 0.9rem; }
        .pros-box p:last-child, .cons-box p:last-child { margin-bottom: 0; }

        .highlight-box, .verdict {
            background: var(--card); border: 1px solid var(--border);
            border-radius: 12px; padding: 1.5rem; margin: 1.8rem 0;
        }
        .highlight-box h3, .verdict h3 {
            font-size: 1rem; font-weight: 700;
            color: var(--accent); margin-bottom: 0.8rem;
        }
        .highlight-box p, .verdict p { font-size: 0.95rem; color: var(--text); margin-bottom: 0; }

        .related-articles { margin-top: 2.5rem; }
        .related-articles h3 {
            font-size: 1rem; font-weight: 700;
            color: var(--text-bright); margin-bottom: 1rem;
        }
        .related-grid { display: flex; flex-direction: column; gap: 0.8rem; }
        .related-card {
            background: var(--card); border: 1px solid var(--border);
            border-radius: 10px; padding: 1rem;
            transition: border-color 0.2s;
        }
        .related-card:hover { border-color: var(--accent); }
        .related-card a { display: flex; align-items: center; gap: 0.8rem; }
        .related-tag {
            font-size: 0.7rem; font-weight: 600;
            color: var(--accent); letter-spacing: 0.06em;
            text-transform: uppercase; white-space: nowrap;
        }
        .related-title { font-size: 0.88rem; color: var(--text); }
        .related-card:hover .related-title { color: var(--text-bright); }

        .share-bar {
            position: fixed; left: 2rem; top: 50%; transform: translateY(-50%);
            display: flex; flex-direction: column; gap: 0.6rem; z-index: 90;
        }
        .share-btn {
            width: 38px; height: 38px;
            background: var(--card); border: 1px solid var(--border);
            border-radius: 8px; display: flex; align-items: center; justify-content: center;
            color: var(--text-dim); font-size: 0.85rem; transition: all 0.2s;
        }
        .share-btn:hover {
            background: var(--accent-dim); border-color: var(--accent); color: var(--accent);
        }

        .article-footer {
            margin-top: 3rem; padding-top: 2rem;
            border-top: 1px solid var(--border);
        }
        .back-to-top {
            display: inline-flex; align-items: center; gap: 0.4rem;
            font-size: 0.82rem; color: var(--text-dim); padding: 0.5rem 0;
        }
        .back-to-top:hover { color: var(--accent); }

        @media (max-width: 768px) {
            .share-bar { display: none; }
            .article-container { padding: 2rem 1.2rem 4rem; }
            .tool-card-pros-cons { grid-template-columns: 1fr; }
            .nav-links { display: none; }
        }"""

NOVELPICK_CSS = """
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.8;
            -webkit-font-smoothing: antialiased;
        }
        a { color: var(--accent); text-decoration: none; }
        a:hover { color: var(--accent-rose); }

        nav {
            position: fixed; top: 0; left: 0; right: 0; z-index: 100;
            background: rgba(13, 10, 20, 0.92);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border);
            padding: 0 2rem;
        }
        .nav-inner {
            max-width: 860px; margin: 0 auto;
            display: flex; align-items: center; justify-content: space-between;
            height: 60px;
        }
        .nav-logo {
            font-family: 'Playfair Display', serif;
            font-weight: 700; font-size: 1.3rem;
            color: var(--accent); letter-spacing: 0.01em;
        }
        .nav-links { display: flex; gap: 1.8rem; list-style: none; }
        .nav-links a {
            font-size: 0.82rem; font-weight: 500;
            color: var(--text-dim); letter-spacing: 0.03em;
            transition: color 0.2s;
        }
        .nav-links a:hover, .nav-links a.active { color: var(--accent); }

        .progress-bar {
            position: fixed; top: 60px; left: 0; right: 0; height: 2px; z-index: 99;
            background: var(--border);
        }
        .progress-fill {
            height: 100%; background: linear-gradient(90deg, var(--accent), var(--accent-rose));
            width: 0%; transition: width 0.1s linear;
        }

        .article-container {
            max-width: 720px; margin: 0 auto;
            padding: 3rem 1.5rem 6rem;
        }

        .article-category {
            display: inline-flex; align-items: center; gap: 0.5rem;
            font-size: 0.72rem; font-weight: 600;
            color: var(--accent-rose); letter-spacing: 0.1em; text-transform: uppercase;
            margin-bottom: 1.2rem;
        }
        .category-icon { font-size: 1rem; }

        .article-title {
            font-family: 'Playfair Display', serif;
            font-size: clamp(2rem, 4.5vw, 2.8rem);
            font-weight: 700; color: var(--text-bright);
            line-height: 1.2; margin-bottom: 1.2rem;
        }
        .article-subtitle {
            font-family: 'Lora', serif;
            font-size: 1.05rem; color: var(--text-dim);
            font-style: italic; line-height: 1.65; margin-bottom: 2rem;
        }

        .article-meta {
            display: flex; align-items: center; gap: 1rem;
            padding: 1.2rem 0;
            border-top: 1px solid var(--border);
            border-bottom: 1px solid var(--border);
            margin-bottom: 2.5rem;
        }
        .meta-item {
            display: flex; align-items: center; gap: 0.4rem;
            font-size: 0.82rem; color: var(--text-dim);
        }
        .meta-sep { width: 1px; height: 14px; background: var(--border); }
        .meta-rating { color: var(--accent-rose); }

        .article-cover {
            width: 100%; height: 280px;
            background: linear-gradient(135deg, #1a1230 0%, #2a1840 50%, #1a1230 100%);
            border-radius: 12px; margin-bottom: 2.5rem;
            display: flex; align-items: center; justify-content: center;
            position: relative; overflow: hidden;
        }
        .article-cover::after {
            content: '';
            position: absolute; inset: 0;
            background: radial-gradient(ellipse at 30% 50%, rgba(201, 160, 220, 0.15) 0%, transparent 60%),
                        radial-gradient(ellipse at 70% 50%, rgba(240, 160, 176, 0.1) 0%, transparent 60%);
        }
        .cover-text {
            font-family: 'Playfair Display', serif;
            font-size: 2rem; font-style: italic;
            color: rgba(201, 160, 220, 0.2);
            position: relative; z-index: 1;
        }

        .article-lead {
            font-family: 'Lora', serif;
            font-size: 1.08rem; color: var(--text);
            line-height: 1.8; margin-bottom: 2rem;
            padding-left: 1.2rem; border-left: 2px solid var(--accent);
        }

        .article-content p {
            font-size: 0.97rem; color: var(--text);
            margin-bottom: 1.3rem; line-height: 1.85;
        }
        .article-content h2 {
            font-family: 'Playfair Display', serif;
            font-size: 1.5rem; font-weight: 700;
            color: var(--text-bright);
            margin: 2.8rem 0 1rem; padding-bottom: 0.6rem;
            border-bottom: 1px solid var(--border);
        }
        .article-content h3 {
            font-family: 'Playfair Display', serif;
            font-size: 1.15rem; font-weight: 600;
            color: var(--accent); margin: 1.8rem 0 0.6rem;
        }
        .article-content strong { color: var(--text-bright); font-weight: 600; }
        .article-content ul, .article-content ol { margin: 0.8rem 0 1.2rem 1.5rem; }
        .article-content li {
            font-size: 0.97rem; color: var(--text);
            margin-bottom: 0.4rem; line-height: 1.7;
        }

        .novel-card {
            background: var(--card); border: 1px solid var(--border);
            border-radius: 12px; padding: 1.5rem; margin: 1.8rem 0;
            position: relative;
        }
        .novel-card::before {
            content: '';
            position: absolute; top: 0; left: 0; right: 0; height: 3px;
            background: linear-gradient(90deg, var(--accent), var(--accent-rose));
            border-radius: 12px 12px 0 0;
        }
        .novel-rank {
            font-family: 'Playfair Display', serif;
            font-size: 2.5rem; font-weight: 700;
            color: var(--border);
            position: absolute; top: 1rem; right: 1.2rem;
        }
        .novel-title {
            font-family: 'Playfair Display', serif;
            font-size: 1.15rem; font-weight: 700;
            color: var(--text-bright); margin-bottom: 0.3rem;
            padding-right: 3rem;
        }
        .novel-tags { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 0.8rem; }
        .tag {
            font-size: 0.7rem; font-weight: 600;
            padding: 0.2rem 0.6rem; border-radius: 50px; letter-spacing: 0.04em;
        }
        .tag-platform { background: var(--accent-dim); color: var(--accent); border: 1px solid rgba(201, 160, 220, 0.2); }
        .tag-status { background: rgba(240, 160, 176, 0.1); color: var(--accent-rose); border: 1px solid rgba(240, 160, 176, 0.2); }
        .tag-genre { background: rgba(160, 200, 255, 0.08); color: #a0c8ff; border: 1px solid rgba(160, 200, 255, 0.15); }
        .novel-desc {
            font-size: 0.9rem; color: var(--text); line-height: 1.7;
            font-family: 'Lora', serif;
        }

        .pros-box {
            background: rgba(74, 222, 128, 0.08);
            border: 1px solid rgba(74, 222, 128, 0.2);
            border-radius: 8px; padding: 1rem; margin: 0.8rem 0;
        }
        .cons-box {
            background: rgba(248, 113, 113, 0.08);
            border: 1px solid rgba(248, 113, 113, 0.2);
            border-radius: 8px; padding: 1rem; margin: 0.8rem 0;
        }
        .pros-box strong { color: #4ade80; }
        .cons-box strong { color: #f87171; }
        .pros-box p, .cons-box p { margin-bottom: 0.4rem; font-size: 0.9rem; }
        .pros-box p:last-child, .cons-box p:last-child { margin-bottom: 0; }

        .rating-box {
            background: var(--card); border: 1px solid var(--border);
            border-radius: 12px; padding: 1.5rem; margin: 1.8rem 0;
        }
        .rating-box h3 {
            font-family: 'Playfair Display', serif;
            font-size: 1rem; font-weight: 700;
            color: var(--accent); margin-bottom: 1rem;
        }

        .related-articles { margin-top: 2.5rem; }
        .related-articles h3 {
            font-family: 'Playfair Display', serif;
            font-size: 1.1rem; font-weight: 700;
            color: var(--text-bright); margin-bottom: 1rem;
        }
        .related-grid { display: flex; flex-direction: column; gap: 0.8rem; }
        .related-card {
            background: var(--card); border: 1px solid var(--border);
            border-radius: 10px; padding: 1rem;
            transition: border-color 0.2s;
        }
        .related-card:hover { border-color: var(--accent); }
        .related-card a { display: flex; align-items: center; gap: 0.8rem; }
        .related-tag {
            font-size: 0.7rem; font-weight: 600;
            color: var(--accent-rose); letter-spacing: 0.06em;
            text-transform: uppercase; white-space: nowrap;
        }
        .related-title { font-size: 0.88rem; color: var(--text); }
        .related-card:hover .related-title { color: var(--text-bright); }

        .share-bar {
            position: fixed; left: 2rem; top: 50%; transform: translateY(-50%);
            display: flex; flex-direction: column; gap: 0.6rem; z-index: 90;
        }
        .share-btn {
            width: 38px; height: 38px;
            background: var(--card); border: 1px solid var(--border);
            border-radius: 8px; display: flex; align-items: center; justify-content: center;
            color: var(--text-dim); font-size: 0.85rem; transition: all 0.2s;
        }
        .share-btn:hover {
            background: var(--accent-dim); border-color: var(--accent); color: var(--accent);
        }

        .article-footer {
            margin-top: 3rem; padding-top: 2rem;
            border-top: 1px solid var(--border);
        }
        .back-to-top {
            display: inline-flex; align-items: center; gap: 0.4rem;
            font-size: 0.82rem; color: var(--text-dim);
        }
        .back-to-top:hover { color: var(--accent); }

        @media (max-width: 768px) {
            .share-bar { display: none; }
            .article-container { padding: 2rem 1.2rem 4rem; }
            .nav-links { display: none; }
        }"""

# ── Progress + scroll script ─────────────────────────────────────────────────

PROGRESS_SCRIPT = """<script>
        window.addEventListener('scroll', () => {
            const scrollTop = window.scrollY;
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
            const el = document.getElementById('progressFill');
            if (el) el.style.width = progress + '%';
        });
    </script>"""


# ── Core fix logic ───────────────────────────────────────────────────────────

def is_malformed(content: str) -> bool:
    """Check for the duplicate <head> + orphaned </head> pattern."""
    return content.count('<head>') >= 2 and '</head>' in content


def parse_malformed(content: str):
    """
    Extract parts from a malformed file.

    Returns dict with:
      meta_tags    — lines from first <head> block (meta, title, link)
      css          — the <style>...</style> block from the orphaned section
      body_content — everything in <body>
      tail_scripts — all <script> blocks from body
    """
    # Find the first <head> block (lines 1-2: <!DOCTYPE>/<html> then <head>)
    first_head_start = content.find('<head>')

    # The FIRST </head> in the file closes the first <head>
    # But we have: </head>\n<head>  (the orphan pattern)
    # So we look for </head> followed by whitespace+<head>
    dup_match = re.search(r'</head>\s*<head>', content)
    if dup_match:
        first_head_end = dup_match.start()
    else:
        # fallback
        first_head_end = content.find('</head>')
        if first_head_end == -1:
            return None

    first_head_inner = content[first_head_start + 6:first_head_end]

    # Collect meta/link/title lines from first head
    meta_tags = []
    for line in first_head_inner.splitlines():
        ls = line.strip()
        if ls.startswith('<meta ') or ls.startswith('<title>') or ls.startswith('<link '):
            meta_tags.append(ls)

    # Now find the second <head> and its </head>
    second_head_start = content.find('<head>', first_head_end)
    if second_head_start == -1:
        return None

    # The orphaned </head> is after </style>
    style_start = content.find('<style>', second_head_start)
    style_end = content.find('</style>', style_start)
    if style_end == -1:
        return None
    css = content[style_start:style_end + 8]  # include </style>

    # orphaned </head> is right after </style>
    orphaned_head_pos = content.find('</head>', style_end)
    if orphaned_head_pos == -1:
        return None

    # Body starts after the orphaned </head>
    body_start = content.find('<body>', orphaned_head_pos)
    if body_start == -1:
        return None
    body_tag_end = content.find('>', body_start) + 1

    # Find body end
    body_end = content.rfind('</body>')
    if body_end == -1:
        body_end = len(content)

    body_raw = content[body_tag_end:body_end]

    # Separate scripts from body content
    scripts = re.findall(r'<script[^>]*>.*?</script>', body_raw, re.DOTALL)
    for s in scripts:
        body_raw = body_raw.replace(s, '\n__SCRIPT_PLACEHOLDER__\n')

    return {
        'meta_tags':   meta_tags,
        'css':         css,
        'body_content': body_raw.strip(),
        'scripts':     scripts,
    }


def build_clean_html(site_name: str, parsed) -> str:
    """Reconstruct a clean HTML5 file from parsed parts."""
    cfg = SITES[site_name]
    css = MORAI_CSS if site_name == 'morai' else NOVELPICK_CSS

    # Build nav links HTML
    nav_links_html = '\n'.join(
        f'                <li><a href="{href}">{label}</a></li>'
        for href, label in cfg['nav_links']
    )

    # Deduplicate meta tags
    seen, deduped = [], []
    for tag in parsed['meta_tags']:
        if 'property="' in tag:
            k = re.search(r'property="([^"]+)"', tag)
            key = k.group(1) if k else tag
        elif 'name="' in tag:
            k = re.search(r'name="([^"]+)"', tag)
            key = k.group(1) if k else tag
        elif 'charset="' in tag or 'viewport' in tag:
            key = tag
        else:
            key = tag
        if key not in seen:
            seen.append(key)
            deduped.append(tag)
    meta_html = '\n    '.join(deduped)

    # Scripts at end of body
    scripts_html = '\n'.join(parsed['scripts'])

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
{cfg['fonts']}
{meta_html}
    <style>
{MORAI_CSS_VARS if site_name == 'morai' else NOVELPICK_CSS_VARS}
{css}
    </style>
</head>
<body>
<nav>
        <div class="nav-inner">
            <a href="./index.html" class="nav-logo">{cfg['nav_logo']}</a>
            <ul class="nav-links">
{nav_links_html}
            </ul>
        </div>
    </nav>
<div class="progress-bar"><div class="progress-fill" id="progressFill"></div>
{parsed['body_content']}
{PROGRESS_SCRIPT}
{scripts_html}
{cfg['baidu']}
</body>
</html>'''
    return html


def fix_file(filepath: str, site_name: str) -> bool:
    """Process one HTML file. Returns True if fixed, False if skipped."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if not is_malformed(content):
        print(f'  SKIP  (not malformed): {os.path.basename(filepath)}')
        return False

    parsed = parse_malformed(content)
    if not parsed:
        print(f'  FAIL  (parse error):   {os.path.basename(filepath)}')
        return False

    new_html = build_clean_html(site_name, parsed)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f'  FIXED: {os.path.basename(filepath)}')
    return True


# Pages that are index/category — not article pages — to skip
MORAI_SKIP = {
    'index.html','search.html','deals.html',
    'ai-tools.html','ai-reviews.html','ai-guides.html','ai-comparisons.html',
}

NOVELPICK_SKIP = {
    'index.html','fantasy.html','litrpg.html','scifi.html','romance.html','reviews.html',
}

def is_article(filepath, site):
    name = os.path.basename(filepath)
    skip = MORAI_SKIP if site == 'morai' else NOVELPICK_SKIP
    return name not in skip

def main():
    for site_name, cfg in SITES.items():
        print(f'\n=== {site_name.upper()} ===')
        fixed = skipped = failed = 0
        for filepath in glob.glob(os.path.join(cfg['dir'], '*.html')):
            if not is_article(filepath, site_name):
                print(f'  SKIP  (index/category): {os.path.basename(filepath)}')
                skipped += 1
                continue
            ok = fix_file(filepath, site_name)
            if ok: fixed += 1
            elif ok is False: skipped += 1
            else: failed += 1
        print(f'  RESULT: fixed={fixed}, skipped={skipped}, failed={failed}')

if __name__ == '__main__':
    main()
