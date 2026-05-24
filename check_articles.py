#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Systematic article checker for the 3-site cron task."""
import os, re, sys, json
from datetime import datetime
from pathlib import Path

BASE = Path(r"C:\Users\Administrator\.openclaw\workspace")

ARTICLES = [
    ("morai-website", "chatgpt-vs-claude-vs-gemini-2026.html"),
    ("morai-website", "claude-3-7-sonnet-review.html"),
    ("morai-website", "best-ai-tools-2026.html"),
    ("morai-website", "ai-agent-tools-2026.html"),
    ("novelpick-website", "best-chinese-wuxia-web-novels-2026.html"),
    ("novelpick-website", "books-like-solo-leveling.html"),
    ("novelpick-website", "top-romance-web-novels-2026.html"),
    ("fateandmethod-website", "feng-shui-2026-year-guide.html"),
    ("fateandmethod-website", "bazi-beginners-complete-guide.html"),
    ("fateandmethod-website", "chinese-zodiac-2026-fire-snake-horoscope.html"),
    ("fateandmethod-website", "five-elements-complete-guide.html"),
]

AI_PATTERNS = [
    (r"(unlock|unleash|dive into|delve into)", "AI cliche verb"),
    (r"(game-changer|revolutionize|paradigm shift)", "hyperbolic language"),
    (r"stands as a testament", "inflated symbolism"),
    (r"it.s not just .+ it.s also", "not-just-but-also pattern"),
    (r"in today.s (digital|fast-paced|ever-changing) \w+", "in-todays-X-landscape"),
    (r"what sets .+ apart is", "formulaic comparison"),
    (r"(unleash|harness) (the|your) (power|potential)", "motivational filler"),
]

def check_div_file(content, filepath):
    issues = []
    opens = len(re.findall(r'<div\b', content))
    closes = len(re.findall(r'</div>', content))
    if opens != closes:
        issues.append(("DIV_UNBALANCED", f"Full file: {opens} opens vs {closes} closes (diff={opens-closes})"))
    
    body_match = re.search(r'<div[^>]*class="[^"]*article-body[^"]*"[^>]*>', content)
    if body_match:
        start = body_match.end()
        depth = 1
        pos = start
        while pos < len(content) and depth > 0:
            next_open = content.find('<div', pos)
            next_close = content.find('</div>', pos)
            if next_close == -1:
                issues.append(("ARTICLE_BODY_UNCLOSED", "Could not find closing </div> for article-body"))
                break
            if next_open != -1 and next_open < next_close:
                depth += 1
                pos = next_open + 1
            else:
                depth -= 1
                pos = next_close + 6
        if depth > 0:
            issues.append(("ARTICLE_BODY_DEPTH", f"article-body depth={depth} at end of scan"))
    else:
        issues.append(("NO_ARTICLE_BODY", "No article-body div found"))
    return issues

def check_css(content, filepath):
    issues = []
    css_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    if not css_match:
        issues.append(("NO_CSS", "No <style> block found"))
        return issues
    css = css_match.group(1)
    last_meaningful = css.rstrip().rstrip(';').rstrip()
    if last_meaningful.endswith('{') or last_meaningful.endswith(':') or last_meaningful.endswith(';'):
        issues.append(("CSS_TRUNCATED", f"Ends with: ...{last_meaningful[-30:]}"))
    brace = 0
    for ch in css:
        if ch == '{': brace += 1
        elif ch == '}': brace -= 1
    if brace != 0:
        issues.append(("CSS_BRACE", f"Net braces: {brace}"))
    return issues

def check_ai_patterns(content, filepath):
    issues = []
    for pattern, label in AI_PATTERNS:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if len(matches) > 0:
            sample = str(matches[0])[:80]
            issues.append(("AI_PATTERN", f"'{label}': {len(matches)}x, e.g. '{sample}'"))
    return issues

def check_garbled_text(content, filepath):
    issues = []
    if '\ufffd' in content:
        pos = content.index('\ufffd')
        context = repr(content[max(0,pos-20):pos+80])
        issues.append(("REPLACEMENT_CHAR", f"At pos {pos}: {context}"))
    garbled_markers = ['\u9225', '\u9479', '\u7d8b', '\u4f9b', '\u93c8', '\u6d93', '\u93c4', '\u9430']
    for gm in garbled_markers:
        count = content.count(gm)
        if count > 2:
            issues.append(("GARBLED_CJK", f"'{gm}' appears {count} times"))
            break
    return issues

def check_links(content, filepath):
    issues = []
    site_dir = filepath.parent
    hrefs = re.findall(r'href="([^"]*)"', content)
    for href in hrefs:
        if href.endswith('.html') and not href.startswith('http') and not href.startswith('#'):
            target = (site_dir / href.lstrip('/')).resolve()
            if not target.exists():
                issues.append(("BROKEN_LINK", f"-> {href} (not found)"))
    return issues

def check_dates(content, filepath):
    issues = []
    date_formats = [
        r'(\d{4})[-/\xe5\xb9\xb4](\d{1,2})[-/\xe6\x9c\x88](\d{1,2})',
        r'(\d{4})-(\d{2})-(\d{2})',
    ]
    # Also catch Month DD, YYYY format
    month_names = 'January|February|March|April|May|June|July|August|September|October|November|December'
    text_date = re.search(rf'({month_names})\s+(\d{{1,2}}),\s+(\d{{4}})', content)
    if text_date:
        month_map = {'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}
        m_name = text_date.group(1)
        day = int(text_date.group(2))
        year = int(text_date.group(3))
        if m_name in month_map:
            try:
                article_date = datetime(year, month_map[m_name], day)
                age_days = (datetime.now() - article_date).days
                if age_days > 90:
                    issues.append(("OUTDATED", f"Date {m_name} {day}, {year} is {age_days}d old"))
            except:
                pass
            return issues
    for fmt in date_formats:
        matches = re.findall(fmt, content)
        if matches:
            y, m, d = map(int, matches[0])
            try:
                article_date = datetime(y, m, d)
                age_days = (datetime.now() - article_date).days
                if age_days > 90:
                    issues.append(("OUTDATED", f"Date {y}-{m:02d}-{d:02d} is {age_days}d old"))
            except:
                pass
            return issues
    issues.append(("NO_DATE", "No publish date found"))
    return issues

def check_related(content, filepath):
    if not re.search(r'(Keep Reading|Related Posts|You May Also Like|Related Articles|Recommended|Recommended Novels|\xe6\x8e\xa8\xe8\x8d\x90|\xe7\x9b\xb8\xe5\x85\xb3)', content, re.IGNORECASE):
        return [("NO_RELATED", "No related articles section")]
    return []

def check_content_quality(content, filepath):
    issues = []
    text = re.sub(r'<[^>]+>', '', content)
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) < 500:
        issues.append(("THIN_CONTENT", f"Only {len(text)} chars of text"))
    for m in re.finditer(r'<h2[^>]*>(.*?)</h2>', content):
        title = m.group(1)
        end = m.end()
        next_h2 = content.find('<h2', end)
        next_section = content.find('<section', end)
        next_footer = content.find('<footer', end)
        endpoints = [x for x in [next_h2, next_section, next_footer] if x != -1]
        section_end = min(endpoints) if endpoints else len(content)
        section_body = content[end:section_end]
        section_text = re.sub(r'<[^>]+>', '', section_body).strip()
        if len(section_text) < 30:
            issues.append(("THIN_H2", f"H2 '{title[:40]}' has only {len(section_text)} chars"))
    return issues

def main():
    results = {}
    total_issues = 0
    
    for site, filename in ARTICLES:
        filepath = BASE / site / filename
        key = f"{site}/{filename}"
        
        if not filepath.exists():
            results[key] = [("MISSING", "File not found")]
            total_issues += 1
            continue
        
        content = filepath.read_text(encoding='utf-8', errors='replace')
        all_issues = []
        
        for checker in [check_div_file, check_css, check_ai_patterns, 
                       check_garbled_text, check_links, check_dates, 
                       check_related, check_content_quality]:
            try:
                all_issues.extend(checker(content, filepath))
            except Exception as e:
                all_issues.append(("CHECKER_ERR", f"{checker.__name__}: {e}"))
        
        results[key] = all_issues
        total_issues += len(all_issues)
    
    # Print ASCII-safe report
    print(f"\n{'='*70}")
    print(f"  ARTICLE CHECK REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Total articles: {len(ARTICLES)} | Total issues: {total_issues}")
    print(f"{'='*70}")
    
    for key, issues in results.items():
        print(f"\n{'--'*30}")
        print(f"  FILE: {key}")
        print(f"{'--'*30}")
        if not issues:
            print("  [OK] PASS - No issues found")
        else:
            for issue_type, detail in issues:
                print(f"  [WARN] [{issue_type}] {detail}")

if __name__ == "__main__":
    main()
