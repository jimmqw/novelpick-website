#!/usr/bin/env python3
"""Website quality audit - accurate for actual HTML structure of morai/novelpick"""
import re, sys
from pathlib import Path

# List pages that don't need article-body or reading-time
LIST_PAGES = set(['index.html', 'search.html', 'ai-tools.html', 'ai-guides.html',
                  'ai-reviews.html', 'ai-comparisons.html', 'deals.html',
                  'fantasy.html', 'litrpg.html', 'romance.html', 'scifi.html',
                  'reviews.html'])

# Pages with alternative layout (no sidebar, different nav style)
ALT_LAYOUT = set(['github-copilot-review-2026.html',
                  'best-ai-design-tools-2026.html',
                  'chatgpt-vs-claude-vs-gemini-2026.html',
                  'how-ai-agents-transform-knowledge-work-2026.html',
                  'best-ai-research-assistants-2026.html',
                  'claude-code-vs-cursor-vs-github-copilot-2026.html',
                  'best-ai-search-research-tools-2026.html',
                  'ai-tools.html'])

def audit_site(site_dir, site_name, is_novelpick=False):
    issues_all = []
    total = ok = 0

    html_files = sorted(Path(site_dir).rglob("*.html"))
    html_files = [f for f in html_files if f.name != "template.html"]

    for fp in html_files:
        total += 1
        try:
            c = fp.read_text(encoding='utf-8', errors='replace')
        except:
            c = fp.read_text(encoding='latin-1')
        name = fp.name
        iss = []

        is_list = name in LIST_PAGES
        is_alt = name in ALT_LAYOUT

        # === Nav ===
        if 'nav' not in c.lower():
            iss.append("nav section missing")
        elif not re.search(r'class="[^"]*nav[^"]*"', c):
            iss.append("nav class missing")

        # Breadcrumb - skip for index
        if 'breadcrumb' not in c.lower():
            if name != 'index.html':
                iss.append("breadcrumb missing")

        # Sidebar - only check for layout pages
        if not is_alt:
            if 'sidebar' in c.lower():
                m = re.search(r'<aside[^>]*class="[^"]*sidebar[^"]*"[^>]*>(.*?)</aside>', c, re.I | re.DOTALL)
                if m:
                    stext = re.sub(r'<[^>]+>', '', m.group(1)).strip()
                    if len(stext) < 20:
                        iss.append("sidebar empty/short")
            else:
                if 'class="layout"' in c:
                    iss.append("sidebar missing")

        # Related articles
        if not re.search(r'(related|推荐|popular|recommended)', c, re.I):
            if name not in ('index.html', 'search.html'):
                iss.append("related articles missing")

        # Footer
        if '<footer' not in c.lower():
            iss.append("footer missing")
        else:
            if not re.search(r'(&copy;|©|' + chr(169) + r'|copyright)', c, re.I):
                iss.append("footer lacks copyright")

        # === Baidu analytics ===
        if 'hm.baidu.com' not in c:
            iss.append("Baidu analytics missing")

        # === Article body ===
        if 'article-body' in c.lower():
            m = re.search(r'class="[^"]*article-body[^"]*"[^>]*>', c)
            if m:
                segment = c[m.end():]
                depth = 1
                pos = 0
                while pos < len(segment) and depth > 0:
                    if segment[pos:pos+4] == '<div' and segment[pos+4:pos+5] in (' ', '>'):
                        # Not closing tag
                        if segment[pos+4] != '/':
                            depth += 1
                    if segment[pos:pos+6] == '</div>':
                        depth -= 1
                    pos += 1
                article_text = re.sub(r'<[^>]+>', '', segment[:pos]).strip()
                if len(article_text) < 200:
                    iss.append(f"article short ({len(article_text)} chars)")
        elif not is_list and not is_alt:
            iss.append("article-body missing")

        # === SEO meta ===
        if 'og:title' not in c:
            iss.append("missing og:title")
        if 'name="description"' not in c:
            iss.append("missing meta description")
        if 'canonical' not in c:
            iss.append("missing canonical link")

        # Reading time - skip for list pages
        if not is_list:
            if not re.search(r'(reading[\-\s]?time|min read|minute)', c, re.I):
                iss.append("missing reading time")

        # === Layout: div balance ===
        open_divs = len(re.findall(r'<div\b[^>]*>', c, re.I))
        close_divs = len(re.findall(r'</div>', c, re.I))
        if open_divs != close_divs:
            iss.append(f"div imbalance (open:{open_divs} close:{close_divs})")

        # === Mobile ===
        if 'viewport' not in c:
            iss.append("missing viewport meta")
        if '@media' not in c:
            iss.append("missing @media CSS")

        if iss:
            issues_all.append({'name': name, 'issues': iss})
        else:
            ok += 1

    return {'site': site_name, 'total': total, 'ok': ok, 'issues': issues_all}


def print_report(r):
    print()
    print(f"{'='*60}")
    print(f"  {r['site']} AUDIT REPORT")
    print(f"{'='*60}")
    print(f"  Pages: {r['total']} | Clean: {r['ok']} | Issues: {len(r['issues'])}")

    if not r['issues']:
        print("  All pages clean - no issues found.")
        return

    # Group by issue type
    issue_counts = {}
    for item in r['issues']:
        for iss in item['issues']:
            key = re.sub(r'\s*\(.*?\)', '', iss)  # normalize counts
            issue_counts[iss] = issue_counts.get(iss, 0) + 1

    print(f"\n  Issue Summary:")
    for iss, cnt in sorted(issue_counts.items(), key=lambda x: -x[1]):
        print(f"    {cnt:3d} x {iss}")

    print(f"\n  Problem Pages:")
    for item in r['issues']:
        print(f"    {item['name']}")
        for iss in item['issues']:
            print(f"      > {iss}")


if __name__ == '__main__':
    # Morai
    r1 = audit_site(r"C:\Users\Administrator\github\morai-website", "morai.top")
    print_report(r1)

    # Novelpick
    r2 = audit_site(r"C:\Users\Administrator\github\novelpick-website", "novelpick.top", is_novelpick=True)
    print_report(r2)

    # Fateandmethod
    fm = r"C:\Users\Administrator\github\fateandmethod-website"
    if Path(fm).exists():
        r3 = audit_site(fm, "fateandmethod.com", is_novelpick=False)
        print_report(r3)
    else:
        print(f"\n{'='*60}")
        print("  fateandmethod.com: Local repo not found - skipping")
