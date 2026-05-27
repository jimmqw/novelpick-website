# -*- coding: utf-8 -*-
import os
import re
from pathlib import Path

workspace = Path(r"C:\Users\Administrator\.openclaw\workspace")

articles = [
    ("morai.top", "best-ai-agents-2026.html"),
    ("morai.top", "best-ai-image-generation-tools-2026.html"),
    ("morai.top", "best-ai-note-taking-tools-2026.html"),
    ("novelpick.top", "best-cultivation-novels-2026.html"),
    ("novelpick.top", "top-litrpg-web-novels-2026.html"),
    ("novelpick.top", "best-time-travel-web-novels-2026.html"),
    ("fateandmethod.com", "bazi-ten-gods-guide.html"),
    ("fateandmethod.com", "chinese-numerology-complete-guide.html"),
    ("fateandmethod.com", "feng-shui-2026-year-guide.html"),
    ("fateandmethod.com", "chinese-zodiac-compatibility-guide.html"),
]

def check_html(filepath):
    issues = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {"ERROR": [f"READ ERROR: {e}"]}

    # 1. Div nesting in article-body
    article_start = re.search(r'class="[^"]*article-body[^"]*"', content)
    if article_start:
        div_start = content.rfind('<div', 0, article_start.start())
        div_opens = [m.start() for m in re.finditer(r'<div\b', content)]
        div_closes = [m.start() for m in re.finditer(r'</div>', content)]
        for i, pos in enumerate(div_opens):
            if pos == div_start:
                all_tags = [(o, 1) for o in div_opens if o >= pos] + [(c, -1) for c in div_closes if c >= pos]
                all_tags.sort()
                bal = sum(delta for _, delta in all_tags)
                if bal != 0:
                    issues["DIV_NESTING"] = f"region unbalanced (balance={bal})"
                running = 0
                went_negative = False
                for _, delta in all_tags:
                    running += delta
                    if running < 0:
                        went_negative = True
                        break
                if went_negative:
                    issues["DIV_NESTING"] = (issues.get("DIV_NESTING","") + " extra closing tags").strip()
                break
        else:
            issues["DIV_NESTING"] = "could not locate article-body div start"
    else:
        issues["DIV_NESTING"] = "no article-body class found"

    # 2. Unicode replacement chars (mojibake)
    ufffd = content.count('\ufffd')
    if ufffd > 0:
        issues["GARBLE"] = f"{ufffd} Unicode replacement chars (U+FFFD)"

    # 3. Keep Reading
    kr_patterns = ['Keep Reading', 'Related Posts', '相关推荐', '继续阅读', 'Related Articles',
                   'You Might Also Like', 'Recommended', 'Continue Reading', 'Keep reading',
                   'recommended-reading', 'more-articles', 'related-articles', 'recommended']
    has_kr = any(p.lower() in content.lower() for p in kr_patterns)
    if not has_kr:
        issues["NO_KEEP_READING"] = "no related posts / Keep Reading section found"

    # 4. AI trace markers
    ai_hits = []
    ai_checks = {
        'cliche_global_opener': r'(?i)In\s+(?:today.s|the\s+ever-evolving|the\s+rapidly\s+changing|the\s+fast-paced)\s',
        'promotional_verb_phrase': r'(?i)(?:Unlock|Delve|Dive|Explore|Unleash|Elevate|Master|Revolutionize)\s+.{0,40}(?:the\s+power|the\s+potential|the\s+world|the\s+future|your\s+journey)',
        'hyperbolic_noun': r'(?i)(?:game-changer|paradigm\s+shift|unprecedented|groundbreaking|revolutionize)',
    }
    for name, pattern in ai_checks.items():
        m = re.findall(pattern, content)
        if len(m) > 1:
            ai_hits.append(f"{name} ({len(m)}x)")
    if ai_hits:
        issues["AI_TRACE"] = "; ".join(ai_hits)

    # 5. BLUF: h2 questions
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', content)
    question_h2s = [h.strip() for h in h2s if h.strip().endswith('?')]
    if question_h2s:
        issues["BLUF"] = f"{len(question_h2s)}/{len(h2s)} h2s are questions: {question_h2s[:4]}"

    # 6. Outdated year refs
    old_years = re.findall(r'(?:202[0-4]|Jan(?:uary)?\s+202[0-5]|Feb\s+202[0-5]|Mar\s+202[0-5]|Apr\s+202[0-5])', content[:3000])
    if old_years:
        issues["OUTDATED"] = f"old years: {old_years[:5]}"

    # 7. Check links
    links = re.findall(r'href="(https?://[^"]*)"', content)
    dead_count = 0
    for link in links[:20]:
        if 'fateandmethod.com' in link or 'morai.top' in link or 'novelpick.top' in link:
            continue  # skip same-domain links for now
    issues["INFO"] = f"{len(h2s)} h2 sections, {len(links)} external links, {len(content):,} chars"

    return issues


print("=" * 72)
print("BATCH ARTICLE CHECK - 10 articles from 3 sites")
print("=" * 72)

total_issues = 0
total_clean = 0
all_results = []

for site, filename in articles:
    filepath = workspace / site / filename
    if filepath.exists():
        fullname = f"{site}/{filename}"
        issues = check_html(filepath)
        all_results.append((fullname, filepath.stat().st_size, issues))

        has_problems = False
        problem_keys = [k for k in issues if k != 'INFO']
        clean = len(problem_keys) == 0
        for k, v in issues.items():
            if k == 'INFO':
                print(f"  [INFO] {fullname} [{v}] (size={filepath.stat().st_size:,}b)")
            else:
                print(f"  [ISSUE] {fullname} -- {k}: {v}")
                has_problems = True
        if not has_problems:
            total_clean += 1
            print(f"  [CLEAN] {fullname} -- all checks passed")
        else:
            total_issues += 1
    else:
        print(f"  [MISS] {site}/{filename} - NOT FOUND")

print(f"\n{'='*72}")
print(f"SUMMARY: {total_clean} clean, {total_issues} with issues out of {len(articles)} checked")
print("=" * 72)
