#!/usr/bin/env python3
"""Website quality audit - accurate for actual HTML structure of morai/novelpick"""
import re, sys
from pathlib import Path

HEADER_COLORS = {
    'morai': ['#060b14', '#0d1520', '#00d4ff', 'rgba(6,11,20,0.93)', 'rgba(6,11,20,0.95)'],
    'novelpick': ['#0d0a14', '#1a0d28', '#c9a0dc', 'rgba(13,10,20,0.93)', 'rgba(13,10,20,0.95)'],
}

def audit_site(site_dir, site_name, is_novelpick=False):
    issues_all = []
    total = ok = 0
    bg_refs = HEADER_COLORS['novelpick'] if is_novelpick else HEADER_COLORS['morai']

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

        # === Nav (replaces header) ===
        if 'nav' not in c.lower():
            iss.append("nav section missing")
        elif not re.search(r'class="[^"]*nav[^"]*"', c):
            iss.append("nav class missing")

        # Breadcrumb
        if 'breadcrumb' not in c.lower():
            # Skip for index/search pages
            if name not in ('index.html', 'search.html'):
                iss.append("breadcrumb missing")

        # Sidebar
        if 'sidebar' in c.lower():
            m = re.search(r'<aside[^>]*class="[^"]*sidebar[^"]*"[^>]*>(.*?)</aside>', c, re.I | re.DOTALL)
            if m:
                stext = re.sub(r'<[^>]+>', '', m.group(1)).strip()
                if len(stext) < 20:
                    iss.append("sidebar effectively empty")
        else:
            # Some pages don't have sidebar (e.g. github-copilot-review style)
            # Only flag if it's a regular article layout page
            if 'class="layout"' in c and 'sidebar' not in c.lower():
                iss.append("sidebar missing in layout page")

        # Related articles
        if not re.search(r'(related|推荐|popular|recommended)', c, re.I):
            iss.append("related/popular articles section missing")

        # Footer
        if '<footer' not in c.lower():
            iss.append("footer missing")
        else:
            if not re.search(r'(©|' + chr(169) + r'|copyright)', c, re.I):
                iss.append("footer lacks copyright")

        # === Baidu analytics ===
        if 'hm.baidu.com' not in c:
            iss.append("Baidu analytics missing")

        # === Article body ===
        if 'article-body' in c.lower():
            m = re.search(r'class="[^"]*article-body[^"]*"[^>]*>', c)
            if m:
                # Extract content after article-body
                start = m.end()
                segment = c[start:]
                # Find where the article-body div closes
                depth = 1
                pos = 0
                for pos in range(len(segment)):
                    # Check for opening <div
                    if segment[pos:pos+4] == '<div' and segment[pos+4:pos+5] in (' ', '>', 'c'):
                        # Make sure it's not a closing tag
                        if pos+5 < len(segment) and segment[pos+5] != '/':
                            # Check it's a real tag, not just text
                            if segment[pos+4] != 'c':  # not a class content
                                depth += 1
                    if segment[pos:pos+6] == '</div>':
                        depth -= 1
                        if depth == 0:
                            break
                article_text = re.sub(r'<[^>]+>', '', segment[:pos]).strip()
                if len(article_text) < 200:
                    iss.append(f"article too short ({len(article_text)} chars)")
        elif name not in ('index.html', 'search.html'):
            iss.append("article-body section missing")

        # === SEO meta ===
        if 'og:title' not in c:
            iss.append("missing og:title")
        if 'name="description"' not in c:
            iss.append("missing meta description")
        if 'canonical' not in c:
            iss.append("missing canonical link")

        # Reading time
        if name not in ('index.html', 'search.html'):
            if not re.search(r'(read(ing)?[\-\s]?time|min read|minute)', c, re.I):
                iss.append("missing reading time estimate")

        # === Layout ===
        # Has background color
        has_bg = False
        for ref in bg_refs:
            if ref in c:
                has_bg = True
                break
        if not has_bg:
            if re.search(r'background[-:]', c, re.I):
                pass  # has some background, probably fine
            else:
                iss.append("no visible background color")

        # div balance
        open_divs = len(re.findall(r'<div[ >]', c))
        close_divs = len(re.findall(r'</div>', c))
        if open_divs != close_divs:
            iss.append(f"div imbalance (open:{open_divs} close:{close_divs})")

        # === Mobile ===
        if 'viewport' not in c:
            iss.append("missing viewport meta")
        if '@media' not in c:
            iss.append("missing responsive CSS (@media)")

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
    print(f"  Pages: {r['total']} | OK: {r['ok']} | Issues: {len(r['issues'])}")

    if not r['issues']:
        print("  All pages clean - no issues found.")
        return

    # Group issues by type
    issue_counts = {}
    for item in r['issues']:
        for iss in item['issues']:
            issue_counts[iss] = issue_counts.get(iss, 0) + 1

    print(f"\n  Issue Summary:")
    for iss, cnt in sorted(issue_counts.items(), key=lambda x: -x[1]):
        print(f"    {cnt:3d} x {iss}")

    print(f"\n  Problem Pages:")
    for item in r['issues']:
        print(f"    {item['name']}:")
        for iss in item['issues']:
            print(f"        - {iss}")


if __name__ == '__main__':
    import os
    
    # Morai
    morai_dir = r"C:\Users\Administrator\github\morai-website"
    if Path(morai_dir).exists():
        r1 = audit_site(morai_dir, "morai.top")
        print_report(r1)

    # Novelpick
    novel_dir = r"C:\Users\Administrator\github\novelpick-website"
    if Path(novel_dir).exists():
        r2 = audit_site(novel_dir, "novelpick.top", is_novelpick=True)
        print_report(r2)

    # Fateandmethod
    fate_dir = r"C:\Users\Administrator\github\fateandmethod-website"
    if Path(fate_dir).exists():
        print(f"\n{'='*60}")
        print(f"  Scanning fateandmethod.com...")
        files = list(Path(fate_dir).rglob("*.html"))
        print(f"  Found {len(files)} HTML files.")
    else:
        print(f"\n{'='*60}")
        print("  fateandmethod.com: Local repo not found (only 1 page, index.html)")
        print("  Not included in this audit.")
