# -*- coding: utf-8 -*-
"""Site Quality Audit - CORRECTED 2026-04-15
Fixed: article-body detection uses nesting-aware parsing instead of non-greedy regex
"""
import os
import re
from pathlib import Path

SITES = [
    {"path": r"C:\Users\Administrator\github\morai-website", "name": "morai", "baidu": True},
    {"path": r"C:\Users\Administrator\github\novelpick-website", "name": "novelpick", "baidu": True},
    {"path": r"C:\Users\Administrator\github\fateandmethod-site", "name": "fateandmethod", "baidu": False},
]

def find_article_body_precise(content):
    """Find article-body region by tracking nesting depth - CORRECT method"""
    m = re.search(r'<div[^>]*id=["\']?article-body["\']?[^>]*>', content, re.IGNORECASE)
    if not m:
        m = re.search(r'<div[^>]*class=["\']?[^"\']*article-body[^"\']*["\'][^>]*>', content, re.IGNORECASE)
    if not m:
        return None
    
    ab_start = m.end()
    depth = 1
    pos = ab_start
    
    while pos < len(content) and depth > 0:
        next_open = content.find('<div', pos)
        next_close = content.find('</div>', pos)
        
        if next_close < 0:
            break
        
        if next_open >= 0 and next_open < next_close:
            depth += 1
            pos = next_open + 5
        else:
            depth -= 1
            if depth == 0:
                return content[m.start():next_close+6]
            pos = next_close + 6
    
    return None

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

    # === 1. Structural checks ===
    has_header_tag = bool(re.search(r'<header', content, re.IGNORECASE))
    has_nav_hero = bool(re.search(r'<nav', content, re.IGNORECASE)) and \
                   bool(re.search(r'<div class="hero|<section class="hero', content))
    if not has_header_tag and not has_nav_hero:
        issues.append("header缺失")
    elif has_header_tag:
        has_grad = bool(re.search(r'<header[^>]*style=["\'][^"\']*gradient', content, re.IGNORECASE)) or \
                   bool(re.search(r'header\s*\{[^}]*background[^}]*gradient', content, re.IGNORECASE))
        if not has_grad:
            issues.append("header无渐变背景")

    if not re.search(r'<nav', content, re.IGNORECASE):
        issues.append("nav缺失")

    has_breadcrumb = bool(re.search(r'breadcrumb|<nav[^>]*breadcrumb', content, re.IGNORECASE))
    if not has_breadcrumb and (is_article or (is_category and site_name != "fateandmethod")):
        issues.append("面包屑缺失")

    has_sidebar = bool(re.search(r'<aside|<div[^>]*id=["\']?sidebar|<div[^>]*class=["\']?sidebar', content, re.IGNORECASE))
    if not has_sidebar and is_article:
        issues.append("侧边栏缺失")

    if not re.search(r'<footer', content, re.IGNORECASE):
        issues.append("footer缺失")

    # === 2. Baidu stats (morai + novelpick only) ===
    if has_baidu:
        if not re.search(r'hm\.baidu\.com|hm\.js', content):
            issues.append("百度统计缺失")

    # === 3. Content quality (using CORRECTED detection) ===
    article_body = find_article_body_precise(content)
    if is_article:
        if article_body:
            text = re.sub(r'<[^>]+>', '', article_body)
            if len(text.strip()) < 200:
                issues.append(f"内容过短({len(text.strip())}字符)")
        else:
            issues.append("未找到article-body")

    # === 4. SEO checks ===
    if not re.search(r'og:title', content):
        issues.append("og:title缺失")
    if not re.search(r'rel=["\']canonical["\']', content):
        issues.append("canonical缺失")
    if not re.search(r'name=["\']description["\']', content) and is_article:
        issues.append("description缺失")

    return issues

def main():
    total_pages = 0
    total_issues = 0
    
    for site in SITES:
        path = Path(site["path"])
        print(f"\n{'='*50}")
        print(f"  {site['name'].upper()} - {path}")
        print(f"{'='*50}")
        
        files = sorted(path.glob("*.html"))
        site_issue_files = []
        
        for f in files:
            issues = audit_file(str(f), site["name"], site["baidu"])
            if issues:
                total_issues += len(issues)
                for issue in issues:
                    site_issue_files.append(f"  {f.name}: {issue}")
        
        total_pages += len(files)
        
        if site_issue_files:
            seen = set()
            for line in site_issue_files:
                if line not in seen:
                    seen.add(line)
                    print(line)
            print(f"\n有问题文件: {len(set(l.split(':')[0].strip() for l in site_issue_files))} / {len(files)}")
        else:
            print("  ✅ 所有页面正常")
    
    print(f"\n{'='*50}")
    print(f"总计: {total_pages}页, {total_issues}个问题")

if __name__ == "__main__":
    main()
