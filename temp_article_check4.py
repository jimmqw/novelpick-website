import re
from pathlib import Path

def safe_preview(text, max_chars=80):
    """Extract preview text, replacing problematic chars"""
    if not text:
        return ""
    # Remove tags
    clean = re.sub(r'<[^>]+>', '', text).strip()
    # Replace newlines/spaces
    clean = ' '.join(clean.split())
    # Truncate
    if len(clean) > max_chars:
        clean = clean[:max_chars] + '...'
    # Replace problematic unicode for console
    clean = clean.replace('\ufffd', '?').encode('ascii', 'replace').decode('ascii')
    return clean

def get_article_text(content):
    """Extract text from article-body container (div or main)"""
    patterns = [
        r'<div[^>]*\bid=["\']article-body["\'][^>]*>(.*?)</div>\s*(?=</article|\n\s*<footer|<div class="recommended|<div class="keep)',
        r'<div[^>]*\bclass=["\'][^"\']*\barticle-body\b[^"\']*["\'][^>]*>(.*?)</div>\s*(?=</article|\n\s*<footer|<div class="recommended|<div class="keep)',
        r'<main[^>]*\bclass=["\'][^"\']*\barticle-body\b[^"\']*["\'][^>]*>(.*?)</main>',
    ]
    for p in patterns:
        m = re.search(p, content, re.DOTALL | re.IGNORECASE)
        if m:
            text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
            return len(text), safe_preview(text, 80)
    return 0, ""

def check_file(path):
    try:
        content = open(path, 'r', encoding='utf-8').read()
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

# Print with ascii-only output
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
        preview = r['body_preview']
        if preview:
            print(f"          preview: {preview[:80]}")

# Summary
print("\n" + "="*60)
print("SUMMARY")
print("="*60)
total_warn = 0
for site, entries in all_results.items():
    warns = sum(1 for _, r in entries if "error" not in r and (
        r['body_len'] < 800 or r['div_balance'] != 0 or not r['keep_reading'] or r['garbled'] or r['ai_phrases'] >= 5
    ))
    total_warn += warns
    print(f"  {site}: {len(entries)} checked, {warns} with issues")
print(f"  TOTAL: {sum(len(v) for v in all_results.values())} checked, {total_warn} with issues")