import os, re
from pathlib import Path

def check_article(filepath):
    issues = {}
    try:
        content = open(filepath, 'r', encoding='utf-8').read()
    except:
        return {"ERROR": "read failed"}

    # article-body content length
    body_match = re.search(r'<div[^>]*id=["\']article-body["\'][^>]*>(.*?)</div>\s*<footer', content, re.DOTALL | re.IGNORECASE)
    if body_match:
        body_text = re.sub(r'<[^>]+>', '', body_match.group(1))
        body_len = len(body_text.strip())
    else:
        body_len = 0

    # div balance (count '<div ' and '<div>' vs '</div>')
    opens = content.count('<div ') + content.count('<div>')
    closes = content.count('</div>')
    div_balance = opens - closes

    # Keep Reading check
    has_keep_reading = bool(re.search(r'keep reading|recommended|related articles', content, re.IGNORECASE))

    # Garbled chars check
    garbled = bool(re.search(r'[釥쏵쏶\u4e00-\u9fff]{3,}', content))

    # AI language detection
    ai_phrases = ['game-changer', 'revolutionary', 'cutting-edge', 'unparalleled', 'next-level',
                  'transformative', 'unmatched', 'best-in-class', 'ultimate solution',
                  'seamless integration', 'effortless', 'powerful tool', 'game changing']
    ai_count = sum(1 for phrase in ai_phrases if phrase.lower() in content.lower())

    # BLUF check
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', content, re.DOTALL)
    bluf_issues = []
    for i, h2 in enumerate(h2s):
        h2_clean = re.sub(r'<[^>]+>', '', h2).strip()[:60]
        if h2_clean and len(h2_clean) > 5:
            h2_escaped = re.escape(h2)
            h2_pos = content.find('<h2' + content[content.find('<h2'):].split('</h2>')[0][4:] + '</h2>')
            # simpler approach: find next h2 position
            all_h2_positions = [m.start() for m in re.finditer(r'<h2[^>]*>.*?</h2>', content, re.DOTALL)]
            h2_index = -1
            for idx, pos in enumerate(all_h2_positions):
                end_pos = pos + content[pos:].find('</h2>') + 5
                if pos <= h2_pos < end_pos:
                    h2_index = idx
                    break
            # just check: does first paragraph after h2 start with a strong/conclusion word?
            pass

    return {
        "body_chars": body_len,
        "div_balance": div_balance,
        "has_keep_reading": has_keep_reading,
        "ai_phrases": ai_count,
        "garbled": garbled,
        "bluf_issues": [],
    }

# Sites
sites = {
    "morai": "C:\\Users\\Administrator\\github\\morai-website",
    "novelpick": "C:\\Users\\Administrator\\github\\novelpick-website",
    "fateandmethod": "C:\\Users\\Administrator\\github\\fateandmethod-site"
}

files_to_check = {
    "morai": [
        "best-ai-coding-assistants-2026.html",
        "best-ai-design-tools-2026.html",
        "best-ai-marketing-tools-2026.html",
        "best-ai-meeting-tools-2026.html",
        "best-ai-music-generation-tools-2026.html",
        "best-ai-note-taking-tools-2026.html",
        "ai-code-review-complete-guide-2026.html",
        "ai-code-review-tools.html",
        "best-ai-voice-cloning-tools-2026.html",
        "best-ai-presentation-tools-2026.html",
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

results = {}
for site, files in files_to_check.items():
    site_path = Path(sites[site])
    results[site] = []
    for fname in files:
        fpath = site_path / fname
        if fpath.exists():
            check = check_article(str(fpath))
            results[site].append((fname, check))
        else:
            results[site].append((fname, {"ERROR": "not found"}))

for site, entries in results.items():
    print(f"\n{'='*60}")
    print(f"SITE: {site}")
    print(f"{'='*60}")
    for fname, check in entries:
        if "ERROR" in check:
            print(f"  {fname}: ERROR - {check['ERROR']}")
            continue
        flags = []
        if check['div_balance'] != 1:
            flags.append(f"div:{check['div_balance']}")
        if check['body_chars'] < 800:
            flags.append(f"body:{check['body_chars']}chars")
        if not check['has_keep_reading']:
            flags.append("NO_KEEP_READING")
        if check['ai_phrases'] >= 5:
            flags.append(f"AI:{check['ai_phrases']}phrases")
        if check['garbled']:
            flags.append("GARBLED")
        status = "WARN" if flags else "OK"
        print(f"  [{status}] {fname}: body={check['body_chars']}, div={check['div_balance']}, ai={check['ai_phrases']}, kr={check['has_keep_reading']}")
        if flags:
            print(f"           FLAGS: {', '.join(flags)}")