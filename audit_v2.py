# -*- coding: utf-8 -*-
import os
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

SITES = [
    {"name": "morai", "path": r"C:\Users\Administrator\github\morai-website"},
    {"name": "novelpick", "path": r"C:\Users\Administrator\github\novelpick-website"},
    {"name": "fateandmethod", "path": r"C:\Users\Administrator\github\fateandmethod-website"},
]

def check_header(content):
    # header存在：<header>标签 OR class="header" OR .nav固定栏（morai/novelpick用.nav代替header）
    has_header_tag = '<header' in content
    has_header_class = 'class="header"' in content or "class='header'" in content
    has_nav_fixed = re.search(r'\.nav\s*\{[^}]*position:\s*fixed', content) is not None
    has_gradient = 'gradient' in content
    # nav栏本身有背景色即可
    has_nav_bg = re.search(r'\.nav\s*\{[^}]*background', content) is not None
    return (has_header_tag or has_header_class or (has_nav_fixed and has_nav_bg)) and has_gradient

def check_nav(content):
    return '<nav' in content

def check_breadcrumb(content):
    return 'breadcrumb' in content.lower()

def check_sidebar(content):
    return 'sidebar' in content.lower()

def check_footer(content):
    has_footer = 'footer' in content.lower()
    has_copyright = 'copyright' in content.lower() or '\u00a9' in content or '2026' in content
    return has_footer and has_copyright

def check_baidu(content):
    return 'hm.baidu.com' in content

def check_viewport(content):
    return 'viewport' in content

def check_responsive(content):
    return '@media' in content

def check_seo_meta(content):
    return 'og:title' in content and 'description' in content and 'canonical' in content

def check_reading_time(content):
    return bool(re.search(r'min read|\d+\s*min|read time|\u5206\u949F|\u9605\u8BFB', content, re.I))

def check_article_length(content):
    match = re.search(r'(?s)article-body.*?<div[^>]*>(.+?)</div>\s*</article', content)
    if match:
        return len(match.group(1).strip()) > 200
    return True

def check_div_balance(content):
    match = re.search(r'(?s)<div[^>]*id=["\']article-body["\'][^>]*>(.+)', content)
    if not match:
        return True
    body = match.group(1)
    opens = body.count('<div')
    closes = body.count('</div>')
    return abs(opens - closes) <= 1

results = []

for site in SITES:
    site_path = Path(site["path"])
    if not site_path.exists():
        continue
    html_files = list(site_path.rglob("*.html"))
    for f in html_files:
        try:
            content = f.read_text(encoding='utf-8')
        except:
            try:
                content = f.read_text(encoding='gbk', errors='ignore')
            except:
                continue
        
        rel_path = str(f.relative_to(site_path))
        issues = []
        
        if not check_header(content):
            issues.append("header渐变背景缺失")
        if not check_nav(content):
            issues.append("nav缺失")
        if not check_breadcrumb(content):
            issues.append("面包屑缺失")
        if not check_sidebar(content):
            issues.append("侧边栏缺失")
        if not check_footer(content):
            issues.append("footer缺失")
        if site["name"] != "fateandmethod" and not check_baidu(content):
            issues.append("百度统计缺失")
        if not check_viewport(content):
            issues.append("viewport缺失")
        if not check_responsive(content):
            issues.append("响应式CSS缺失")
        if not check_seo_meta(content):
            issues.append("SEO meta标签缺失")
        if not check_reading_time(content):
            issues.append("阅读时间缺失")
        if not check_article_length(content):
            issues.append("文章正文过短")
        if not check_div_balance(content):
            issues.append("div嵌套不平衡")
        
        results.append({
            "site": site["name"],
            "path": rel_path,
            "status": "OK" if not issues else "ISSUE",
            "issues": issues
        })

ok_count = sum(1 for r in results if r["status"] == "OK")
issue_count = sum(1 for r in results if r["status"] == "ISSUE")
issue_pages = [r for r in results if r["status"] == "ISSUE"]

print("=" * 60)
print("WEB AUDIT REPORT")
print("=" * 60)
print(f"\nTotal pages: {len(results)}")
print(f"OK: {ok_count}")
print(f"Issues: {issue_count}")

if issue_pages:
    print(f"\n--- Pages with issues ---")
    for p in issue_pages:
        print(f"\n[{p['site']}] {p['path']}")
        for iss in p['issues']:
            print(f"  - {iss}")
else:
    print(f"\nAll clear - no issues found")
