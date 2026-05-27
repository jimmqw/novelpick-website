import re
from pathlib import Path

def get_article_text(content):
    """Extract text from article-body container (div or main)"""
    # Pattern: <div class="article-body"> or <main class="article-body">
    # also id="article-body" on a div
    patterns = [
        r'<div[^>]*\bid=["\']article-body["\'][^>]*>(.*?)</div>\s*(?=</article|\n\s*<footer|<div class="recommended|<div class="keep)',
        r'<div[^>]*\bclass=["\'][^"\']*\barticle-body\b[^"\']*["\'][^>]*>(.*?)</div>\s*(?=</article|\n\s*<footer|<div class="recommended|<div class="keep)',
        r'<main[^>]*\bclass=["\'][^"\']*\barticle-body\b[^"\']*["\'][^>]*>(.*?)</main>',
    ]
    for p in patterns:
        m = re.search(p, content, re.DOTALL | re.IGNORECASE)
        if m:
            text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
            return len(text), text[:80]
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

for site, fnames in files.items():
    base = bases[site]
    print(f"\n{'='*60}")
    print(f"SITE: {site}")
    print(f"{'='*60}")
    for fname in fnames:
        path = Path(base) / fname
        if not path.exists():
            print(f"  [SKIP] {fname} - not found")
            continue
        r = check_file(str(path))
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