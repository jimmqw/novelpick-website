# -*- coding: utf-8 -*-
"""
Website Quality Audit Script v4
"""
import os
import re
from pathlib import Path

def p(msg):
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode('ascii', 'replace').decode('ascii'))

SITES = {
    "morai": {
        "path": r"C:\Users\Administrator\github\morai-website",
        "baidu": True,
        "name": "morai.top"
    },
    "novelpick": {
        "path": r"C:\Users\Administrator\github\novelpick-website",
        "baidu": True,
        "name": "novelpick.top"
    },
    "fateandmethod": {
        "path": r"C:\Users\Administrator\github\fateandmethod-site",
        "baidu": False,
        "name": "fateandmethod.com"
    }
}

INDEX_KEYWORDS = ['index.html', 'search.html', 'deals.html', 'template.html']
CATEGORY_PAGES = ['ai-tools.html', 'ai-guides.html', 'ai-reviews.html', 'ai-comparisons.html',
                  'fantasy.html', 'litrpg.html', 'reviews.html', 'romance.html', 'scifi.html',
                  'daliuren-index.html', 'liuyao-index.html', 'meihua-index.html',
                  'taiyi-index.html', 'xiaoliuren-index.html', 'xuankong-index.html',
                  'bazi.html', 'chinese-zodiac-luck-rankings-2026.html', 'daily-wisdom.html',
                  'feng-shui-complete-guide-2026.html', 'feng-shui-fundamentals.html',
                  'five-elements-complete-guide.html', 'ziwei.html', 'ziwei-intro.html']

def load_html(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except:
        return ""

def is_index_or_category(filename):
    name = os.path.basename(filename).lower()
    if name in INDEX_KEYWORDS or name in CATEGORY_PAGES:
        return True
    return False

def check_header(html):
    """Check for header - accepts <header>, <nav>, or div with header-like role"""
    # <header> HTML5 tag
    if re.search(r'<header[^>]*>', html, re.IGNORECASE):
        return True
    # <nav> element (common site header pattern)
    if re.search(r'<nav\b', html, re.IGNORECASE):
        return True
    # div with role=header or aria-role
    if re.search(r'<div[^>]*role=["\']header["\']', html, re.IGNORECASE):
        return True
    return False

def check_nav(html):
    has_nav = bool(re.search(r'<nav\b', html, re.IGNORECASE))
    if not has_nav:
        has_nav = bool(re.search(r'class=["\'][^"\']*nav\b', html, re.IGNORECASE))
    return has_nav, has_nav

def check_breadcrumb(html):
    return bool(re.search(r'breadcrumb', html, re.IGNORECASE))

def check_sidebar(html):
    has_sidebar = bool(re.search(r'<aside|<aside\s|class=["\']sidebar["\']|id=["\']sidebar["\']', html, re.IGNORECASE))
    sidebar_content = False
    if has_sidebar:
        m = re.search(r'<aside[^>]*>(.*?)</aside>', html, re.IGNORECASE | re.DOTALL)
        if m:
            sidebar_html = m.group(1)
            sidebar_content = bool(re.search(r'<a\s+href=|<ul|<ol|<li|<div|<p[^>]*>', sidebar_html, re.IGNORECASE))
        else:
            sidebar_content = True  # assume if aside tag found, it has content
    return has_sidebar, sidebar_content

def check_related_articles(html):
    has_related = bool(re.search(r'related|continue\s+exploring|prev-next', html, re.IGNORECASE))
    return has_related, has_related

def check_footer(html):
    has_footer = bool(re.search(r'<footer', html, re.IGNORECASE))
    # Check for copyright symbol, entity, or word
    has_copyright = bool(re.search(r'copyright|&copy;|\xa9|©', html, re.IGNORECASE))
    return has_footer, has_footer and has_copyright

def check_baidu(html):
    return bool(re.search(r'hm\.baidu\.com', html))

def check_article_body_length(html, filename):
    if is_index_or_category(filename):
        return True, 999
    # Try class="article-body" or id="article-body"
    for attr in [r'class=["\']article[-_]?body["\']', r'id=["\']article[-_]?body["\']']:
        match = re.search(attr + r'[^>]*>(.*?)(?=<div\s+class=["\']footer|<div\s+class=["\']related|<div\s+class=["\']utterances|</main>|<aside)', html, re.IGNORECASE | re.DOTALL)
        if match:
            text = re.sub(r'<[^>]+>', '', match.group(1))
            return len(text.strip()) > 200, len(text.strip())
    # Try <article> tag
    match = re.search(r'<article[^>]*>(.*?)</article>', html, re.IGNORECASE | re.DOTALL)
    if match:
        text = re.sub(r'<[^>]+>', '', match.group(1))
        return len(text.strip()) > 200, len(text.strip())
    return True, 0

def check_seo_meta(html):
    has_og_title = bool(re.search(r'<meta\s+property=["\']og:title["\']', html, re.IGNORECASE))
    has_desc = bool(re.search(r'<meta\s+(?:property=["\']og:description["\']|name=["\']description["\'])', html, re.IGNORECASE))
    has_canonical = bool(re.search(r'<link\s+rel=["\']canonical["\']', html, re.IGNORECASE))
    return has_og_title, has_desc, has_canonical

def check_reading_time(html):
    return bool(re.search(r'\d+\s*(?:min|minute)|read.*?time', html, re.IGNORECASE))

def check_viewport(html):
    return bool(re.search(r'<meta\s+name=["\']viewport["\']', html, re.IGNORECASE))

def check_responsive_css(html):
    return bool(re.search(r'@media\s*\(', html, re.IGNORECASE))

def check_div_balance(html):
    match = re.search(r'(?:class|id)=["\']article[-_]?body["\']', html, re.IGNORECASE)
    if not match:
        return None
    region_start = match.start()
    region = html[region_start:region_start+15000]
    opens = len(re.findall(r'<div\b', region, re.IGNORECASE))
    closes = len(re.findall(r'</div>', region, re.IGNORECASE))
    balance = opens - closes
    return balance

def audit_file(filepath, site_key, site_info):
    html = load_html(filepath)
    filename = os.path.basename(filepath)
    if not html:
        return {"file": filepath, "filename": filename, "errors": ["Cannot read file"], "warnings": [], "ok": False}

    errors = []
    warnings = []

    if not check_header(html):
        errors.append("Header element missing (no <header> or <nav>)")

    nav_ok, _ = check_nav(html)
    if not nav_ok:
        errors.append("Navigation missing")

    breadcrumb = check_breadcrumb(html)
    if not breadcrumb:
        warnings.append("Breadcrumb navigation missing")

    sidebar, sidebar_content = check_sidebar(html)
    if not sidebar:
        warnings.append("Sidebar missing")
    elif not sidebar_content:
        warnings.append("Sidebar exists but appears empty")

    related, _ = check_related_articles(html)
    if not related:
        warnings.append("Related articles section missing")

    footer, copyright_ok = check_footer(html)
    if not footer:
        errors.append("Footer missing")
    elif not copyright_ok:
        warnings.append("Footer exists but missing copyright symbol/word")

    if site_info["baidu"]:
        if not check_baidu(html):
            errors.append("Baidu analytics code missing")

    is_idx = is_index_or_category(filename)
    body_ok, body_len = check_article_body_length(html, filename)
    if not is_idx and not body_ok:
        errors.append("Article body too short ({} chars, expected >200)".format(body_len))

    og_title, og_desc, canonical = check_seo_meta(html)
    if not og_title:
        warnings.append("og:title meta missing")
    if not og_desc:
        warnings.append("description meta missing")
    if not canonical:
        warnings.append("canonical link missing")

    if not is_idx:
        if not check_reading_time(html):
            warnings.append("Reading time estimate missing")

    if not check_viewport(html):
        warnings.append("viewport meta missing")

    if not check_responsive_css(html):
        warnings.append("Responsive CSS (@media) missing")

    div_balance = check_div_balance(html)
    if div_balance is not None and div_balance < -1:
        errors.append("div nesting unbalanced in article-body ({} extra closes)".format(abs(div_balance)))

    return {
        "file": filepath,
        "filename": filename,
        "errors": errors,
        "warnings": warnings,
        "ok": len(errors) == 0
    }

def main():
    all_results = []

    for site_key, site_info in SITES.items():
        site_path = Path(site_info["path"])
        if not site_path.exists():
            p("[!] Directory not found: {}".format(site_info['path']))
            continue

        html_files = list(site_path.glob("**/*.html"))
        p("\n[DIR] {}: {} HTML files".format(site_info['name'], len(html_files)))

        for f in sorted(html_files):
            result = audit_file(str(f), site_key, site_info)
            result["site"] = site_info["name"]
            all_results.append(result)

    p("\n" + "="*60)
    p("[REPORT] Site Quality Audit Report - {}".format("Monday May 4, 2026"))
    p("="*60)

    ok_pages = [r for r in all_results if r.get("ok", False)]
    error_pages = [r for r in all_results if not r.get("ok", True)]

    p("\n[STAT] Total pages scanned: {}".format(len(all_results)))
    p("[STAT] Normal pages (no errors): {}".format(len(ok_pages)))
    p("[STAT] Pages with errors: {}".format(len(error_pages)))
    p("[STAT] Pages with warnings only: {}".format(len([r for r in all_results if r.get("warnings") and r.get("ok", False) and r not in error_pages])))

    if error_pages:
        p("\n" + "="*60)
        p("[ERRORS] Pages with ERRORS (need fixing)")
        p("="*60)
        for r in sorted(error_pages, key=lambda x: (x.get('site',''), x.get('filename',''))):
            p("\n[FILE] {} ({})".format(r.get('filename',''), r.get('site','')))
            for e in r.get("errors", []):
                p("  [ERR] {}".format(e))
            for w in r.get("warnings", []):
                p("  [WARN] {}".format(w))

    warning_only = [r for r in all_results if r.get("warnings") and r.get("ok", False) and r not in error_pages]
    if warning_only:
        p("\n" + "="*60)
        p("[WARNINGS] Pages with WARNINGS only ({} pages)".format(len(warning_only)))
        p("="*60)
        for r in sorted(warning_only, key=lambda x: (x.get('site',''), x.get('filename','')))[:20]:
            p("\n[FILE] {} ({})".format(r['filename'], r['site']))
            for w in r.get("warnings", []):
                p("  [WARN] {}".format(w))
        if len(warning_only) > 20:
            p("\n  ... and {} more pages".format(len(warning_only) - 20))

    if not error_pages and not warning_only:
        p("\n[OK] Audit complete - no issues found!")
    elif not error_pages:
        p("\n[OK] No errors. {} pages with minor warnings.".format(len(warning_only)))
    else:
        p("\n[INFO] {} pages require attention.".format(len(error_pages)))

    return error_pages

if __name__ == "__main__":
    main()
