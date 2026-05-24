import re
from pathlib import Path

def safe_preview(text, max_chars=80):
    if not text:
        return ""
    clean = re.sub(r'<[^>]+>', '', text).strip()
    clean = ' '.join(clean.split())
    if len(clean) > max_chars:
        clean = clean[:max_chars] + '...'
    clean = clean.replace('\ufffd', '?').encode('ascii', 'replace').decode('ascii')
    return clean

def get_article_text(content):
    """Extract text from article-body div, stopping at footer/recommended"""
    # Find article-body div (by class or id)
    patterns = [
        '<div class="article-body">',
        "<div class='article-body'>",
        '<div id="article-body">',
        '<main class="article-body">',
    ]
    ab_pos = -1
    for p in patterns:
        ab_pos = content.find(p)
        if ab_pos >= 0:
            break
    if ab_pos < 0:
        return 0, ""
    
    # Find the end boundary: footer or recommended div or article closing
    footer_pos = content.find('<footer', ab_pos)
    rec_pos = content.find('<div class="recommended"', ab_pos)
    rec_pos2 = content.find('<div class="keep-reading"', ab_pos)
    article_end = content.find('</article>', ab_pos)
    
    end_pos = len(content)
    if footer_pos > 0:
        end_pos = min(end_pos, footer_pos)
    if rec_pos > 0:
        end_pos = min(end_pos, rec_pos)
    if rec_pos2 > 0:
        end_pos = min(end_pos, rec_pos2)
    if article_end > 0:
        end_pos = min(end_pos, article_end)
    
    # The article-body div itself contains content until the next </div> that isn't nested
    # Find the matching close: after ab_pos, search for </div> and track nesting
    # Simple heuristic: the article-body div closes at the </div> that matches its depth
    # For most pages: div opens = closes, so look for a single </div> near footer_pos
    
    # Alternative: just grab content between ab_pos and end_pos
    segment = content[ab_pos:end_pos]
    text = re.sub(r'<[^>]+>', '', segment).strip()
    return len(text), safe_preview(text, 80)

def check_file(path):
    try:
        content = open(path, 'r', encoding='utf-8', errors='replace').read()
    except Exception as e:
        return {"error": str(e)}
    
    body_len, body_preview = get_article_text(content)
    
    # div balance
    opens = content.count('<div ')
    closes = content.count('</div>')
    balance = opens - closes
    
    # Keep reading
    kr = bool(re.search(r'keep reading|recommended|related articles|you might also like', content, re.IGNORECASE))
    
    # Garbled chars
    garbled = bool(re.search(r'[釥쏵쏶]', content))
    
    # AI phrases
    ai_phrases = ['game-changer', 'revolutionary', 'cutting-edge', 'unparalleled', 'next-level',
                  'transformative', 'unmatched', 'best-in-class', 'ultimate solution',
                  'seamless integration', 'effortless', 'powerful tool', 'game changing']
    ai_count = sum(1 for p in ai_phrases if p.lower() in content.lower())
    
    # Meta description check
    has_meta_desc = bool(re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'][^"\']{20,}', content, re.IGNORECASE))
    
    # H2 count
    h2s = re.findall(r'<h2[^>]*>.*?</h2>', content, re.DOTALL | re.IGNORECASE)
    
    return {
        "body_len": body_len,
        "body_preview": body_preview,
        "div_balance": balance,
        "keep_reading": kr,
        "garbled": garbled,
        "ai_phrases": ai_count,
        "has_meta_desc": has_meta_desc,
        "h2_count": len(h2s),
    }

files = {
    "morai": [
        "best-ai-coding-assistants-2026.html",
        "best-ai-marketing-tools-2026.html",
        "best-ai-meeting-tools-2026.html",
        "best-ai-music-generation-tools-2026.html",
        "best-ai-note-taking-tools-2026.html",
        "ai-code-review-complete-guide-2026.html",
        "ai-code-review-tools.html",
        "best-ai-voice-cloning-tools-2026.html",
        "best-ai-presentation-tools-2026.html",
        "chatgpt-vs-claude.html",
    ],
    "novelpick": [
        "best-apocalypse-and-survival-novels.html",
        "best-cozy-fantasy-novels.html",
        "best-cultivation-novels-2026.html",
        "best-dark-fantasy-novels.html",
        "best-enemies-to-lovers-romance-novels.html",
        "best-germinator-novels.html",
        "best-harem-fantasy-novels-2026.html",
        "best-historical-fantasy-novels.html",
        "best-litrpg-novels.html",
        "best-progression-fantasy-novels.html",
    ],
    "fateandmethod": [
        "bazi.html",
        "liuyao.html",
        "xuankong.html",
        "meihua.html",
        "feng-shui-fundamentals.html",
        "feng-shui-2026-year-guide.html",
        "chinese-zodiac-compatibility-guide.html",
        "chinese-zodiac-personality-traits.html",
        "five-elements-complete-guide.html",
        "daily-wisdom.html",
    ]
}

bases = {
    "morai": r"C:\Users\Administrator\github\morai-website",
    "novelpick": r"C:\Users\Administrator\github\novelpick-website",
    "fateandmethod": r"C:\Users\Administrator\github\fateandmethod-site"
}

all_results = {}
for site, fnames in files.items():
    base = bases[site]
    all_results[site] = []
    for fname in fnames:
        path = Path(base) / fname
        if not path.exists():
            all_results[site].append((fname, {"error": "not found"}))
            continue
        r = check_file(str(path))
        all_results[site].append((fname, r))

for site, entries in all_results.items():
    print(f"\n{'='*60}")
    print(f"SITE: {site}")
    print(f"{'='*60}")
    for fname, r in entries:
        if "error" in r:
            print(f"  [ERR] {fname}: {r['error']}")
            continue
        flags = []
        if r['body_len'] < 800:
            flags.append(f"body={r['body_len']}")
        if r['div_balance'] != 0:
            flags.append(f"div={r['div_balance']}")
        if not r['keep_reading']:
            flags.append("NO_KR")
        if r['garbled']:
            flags.append("GARBLED")
        if r['ai_phrases'] >= 5:
            flags.append(f"AI={r['ai_phrases']}")
        if not r['has_meta_desc']:
            flags.append("NO_META_DESC")
        if r['h2_count'] == 0:
            flags.append("NO_H2")
        status = "WARN" if flags else "OK"
        print(f"  [{status}] {fname}: body={r['body_len']} chars, div={r['div_balance']}, h2={r['h2_count']}, ai={r['ai_phrases']}, kr={r['keep_reading']}")
        if flags:
            print(f"          FLAGS: {', '.join(flags)}")
        if r['body_preview']:
            print(f"          preview: {r['body_preview'][:80]}")

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
for site, entries in all_results.items():
    warns = sum(1 for _, r in entries if "error" not in r and (
        r['body_len'] < 800 or r['div_balance'] != 0 or not r['keep_reading'] or r['garbled'] or r['ai_phrases'] >= 5
    ))
    print(f"  {site}: {len(entries)} checked, {warns} with issues")