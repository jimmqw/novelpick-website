# -*- coding: utf-8 -*-
"""Site Quality Audit - 2026-04-15"""
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
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return [f"文件读取失败: {e}"]

    filename = os.path.basename(filepath)

    # 1. Structural
    if "<header" not in content:
        issues.append("header缺失")
    elif not re.search(r'<header[^>]*style=["\'][^"\']*gradient', content, re.IGNORECASE) and \
         not re.search(r'header\s*\{[^}]*background[^}]*gradient', content, re.IGNORECASE) and \
         not re.search(r'\.header[^{]*\{[^}]*gradient', content, re.IGNORECASE):
        # header exists but no gradient detected - just note, not critical
        pass

    if "<nav" not in content:
        issues.append("nav缺失")
    if "breadcrumb" not in content.lower():
        issues.append("面包屑缺失")
    if not re.search(r'<aside|<div[^>]*id=["\']?sidebar', content, re.IGNORECASE):
        issues.append("侧边栏缺失")
    if not re.search(r'<footer', content, re.IGNORECASE):
        issues.append("footer缺失")

    # 2. Baidu stats
    if has_baidu:
        if not re.search(r'hm\.baidu\.com|hm\.js', content):
            issues.append("百度统计缺失")

    # 3. Content quality
    article_body = re.search(r'<div[^>]*id=["\']?article-body["\']?[^>]*>(.*?)</div>', content, re.DOTALL | re.IGNORECASE)
    if article_body:
        text = re.sub(r'<[^>]+>', '', article_body.group(1))
        if len(text.strip()) < 200:
            issues.append(f"内容过短({len(text.strip())}字符)")
    else:
        # only flag for article-like pages
        if not filename.startswith(('index', 'search', 'deals', 'template', 'category')) and \
           not re.match(r'^[a-z]+-.*\.html$', filename) is None and \
           (re.search(r'\d{4}\.html$', filename) or '-' in filename):
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
        open_divs = len(re.findall(r'<div[^/>]*>', article_body.group(1)))
        close_divs = len(re.findall(r'</div>', article_body.group(1)))
        if open_divs != close_divs:
            issues.append(f"div嵌套不平衡(open={open_divs} close={close_divs})")

    return issues

def main():
    all_results = []
    for site in SITES:
        site_path = Path(site["path"])
        html_files = list(site_path.glob("*.html"))
        for filepath in sorted(html_files):
            issues = audit_file(str(filepath), site["name"], site["baidu"])
            all_results.append({
                "path": str(filepath),
                "filename": filepath.name,
                "site": site["name"],
                "issues": issues
            })

    problems = [r for r in all_results if r["issues"]]
    normal = [r for r in all_results if not r["issues"]]

    total = len(all_results)
    print(f"=== AUDIT RESULTS ===")
    print(f"Total: {total} pages | Normal: {len(normal)} | Problems: {len(problems)}")
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
