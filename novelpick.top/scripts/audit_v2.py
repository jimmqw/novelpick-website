# -*- coding: utf-8 -*-
"""Site Quality Audit - 2026-04-15 v2"""
import os
import re
from pathlib import Path

SITES = [
    {"path": r"C:\Users\Administrator\github\morai-website", "name": "morai", "baidu": True},
    {"path": r"C:\Users\Administrator\github\novelpick-website", "name": "novelpick", "baidu": True},
    {"path": r"C:\Users\Administrator\github\fateandmethod-site", "name": "fateandmethod", "baidu": False},
]

def audit_file(filepath, site_name, has_baidu):
    issues = []
    filename = os.path.basename(filepath)
    is_homepage = filename == "index.html"
    is_category = bool(re.search(r'(category|index|search|deals|template)\.html$', filename))
    is_article = not is_homepage and not is_category

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return [f"file_read_error: {e}"]

    # 1. Structural - header: use flexible detection
    has_header_tag = bool(re.search(r'<header', content, re.IGNORECASE))
    has_header_like = bool(re.search(r'<nav class="nav"|class="nav-logo"|id="header"', content))  # nav-based sites
    has_hero = bool(re.search(r'<div class="hero"|<section class="hero"', content))

    if not has_header_tag and not has_header_like and not has_hero:
        # check if site uses a different structure
        issues.append("header缺失")
    # header gradient: only check if header tag exists
    if has_header_tag:
        has_grad = bool(re.search(r'<header[^>]*style=["\'][^"\']*gradient', content, re.IGNORECASE)) or \
                   bool(re.search(r'header\s*\{[^}]*background[^}]*gradient', content, re.IGNORECASE))
        if not has_grad:
            issues.append("header无渐变")

    # nav
    if not re.search(r'<nav', content, re.IGNORECASE):
        issues.append("nav缺失")

    # breadcrumb: more flexible - check for breadcrumb OR .breadcrumb in class/id
    has_breadcrumb = bool(re.search(r'breadcrumb|<nav[^>]*breadcrumb', content, re.IGNORECASE))
    if not has_breadcrumb and is_article:
        issues.append("面包屑缺失")

    # sidebar
    has_sidebar = bool(re.search(r'<aside|<div[^>]*id=["\']?sidebar|<div[^>]*class=["\']?sidebar', content, re.IGNORECASE))
    if not has_sidebar and is_article:
        issues.append("侧边栏缺失")

    # footer
    if not re.search(r'<footer', content, re.IGNORECASE):
        issues.append("footer缺失")

    # 2. Baidu stats
    if has_baidu:
        if not re.search(r'hm\.baidu\.com|hm\.js', content):
            issues.append("百度统计缺失")

    # 3. Content quality
    article_body = re.search(r'<div[^>]*id=["\']?article-body["\']?[^>]*>(.*?)</div>', content, re.DOTALL | re.IGNORECASE)
    if is_article:
        if article_body:
            text = re.sub(r'<[^>]+>', '', article_body.group(1))
            if len(text.strip()) < 200:
                issues.append(f"内容过短({len(text.strip())}字符)")
        else:
            issues.append("未找到article-body")

    # SEO meta
    if not re.search(r'og:title', content):
        issues.append("og:title缺失")
    if not re.search(r'<meta[^>]+name=["\']description["\']', content, re.IGNORECASE):
        issues.append("description缺失")
    if not re.search(r'canonical', content, re.IGNORECASE):
        issues.append("canonical缺失")

    # 4. Layout
    if not re.search(r'viewport', content, re.IGNORECASE):
        issues.append("viewport缺失")
    if not re.search(r'@media', content):
        issues.append("无响应式CSS")

    # div nesting
    if article_body:
        body_content = article_body.group(1)
        open_divs = len(re.findall(r'<div[^/>]*>', body_content))
        close_divs = len(re.findall(r'</div>', body_content))
        if open_divs != close_divs:
            issues.append(f"div嵌套不平衡(open={open_divs} close={close_divs})")

    return issues

def main():
    all_results = []
    for site in SITES:
        site_path = Path(site["path"])
        html_files = sorted(site_path.glob("*.html"))
        for filepath in html_files:
            issues = audit_file(str(filepath), site["name"], site["baidu"])
            all_results.append({
                "filename": filepath.name,
                "site": site["name"],
                "issues": issues
            })

    problems = [r for r in all_results if r["issues"]]
    normal = [r for r in all_results if not r["issues"]]

    total = len(all_results)
    print(f"=== AUDIT RESULTS (2026-04-15) ===")
    print(f"Total: {total} | Normal: {len(normal)} | Problems: {len(problems)}")
    print()

    if problems:
        print("### PROBLEM PAGES ###")
        for p in problems:
            print(f"FILE: {p['filename']} [{p['site']}]")
            for issue in p["issues"]:
                print(f"  - {issue}")
            print()
    else:
        print("All pages OK!")

    print()
    print("### NORMAL FILES ###")
    for n in normal:
        print(f"  {n['filename']} [{n['site']}]")

if __name__ == "__main__":
    main()
