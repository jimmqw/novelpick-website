# -*- coding: utf-8 -*-
import re
from pathlib import Path

def audit_file(filepath, site_name, needs_baidu_stats=False):
    issues = []
    status = "normal"

    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception:
        return {"status": "problem", "issues": ["文件读取失败"], "filepath": filepath, "site": site_name}

    if not content or not content.strip():
        return {"status": "problem", "issues": ["文件为空"], "filepath": filepath, "site": site_name}

    # 1. Structural checks - more flexible detection
    # header: <header> tag OR div with class/id containing "header" OR <nav class="nav">
    has_header_tag = re.search(r'<header[^>]*>.*?</header>', content, re.DOTALL | re.IGNORECASE)
    has_header_div = re.search(r'<div[^>]*\b(id|class)=["\'][^"\']*header[^"\']*["\'][^>]*>', content, re.IGNORECASE)
    has_nav = re.search(r'<nav[^>]*>.*?</nav>', content, re.DOTALL | re.IGNORECASE)
    if not (has_header_tag or has_header_div or has_nav):
        issues.append("header/nav缺失")

    # breadcrumb
    breadcrumb = re.search(r'breadcrumb|面包屑', content, re.IGNORECASE)
    if not breadcrumb:
        issues.append("面包屑导航缺失")

    # sidebar
    sidebar = re.search(r'sidebar|侧边栏|aside', content, re.IGNORECASE)
    if not sidebar:
        issues.append("侧边栏缺失")

    # related articles
    related = re.search(r'related|相关文章|recommended', content, re.IGNORECASE)
    if not related:
        issues.append("相关文章区块缺失")
    else:
        links = re.findall(r'<a[^>]+href=["\']([^"\']+)["\']', content)
        if len(links) == 0:
            issues.append("相关文章无有效链接")

    # footer
    footer_match = re.search(r'<footer[^>]*>.*?</footer>', content, re.DOTALL | re.IGNORECASE)
    if not footer_match:
        issues.append("footer缺失")
    else:
        copyright_match = re.search(r'©|copyright|&copy;|版权所有', footer_match.group(0), re.IGNORECASE)
        if not copyright_match:
            issues.append("footer无版权信息")

    # baidu stats
    if needs_baidu_stats:
        baidu = re.search(r'hm\.baidu\.com', content)
        if not baidu:
            issues.append("百度统计代码缺失")

    # 2. Content quality
    # article content - check multiple patterns
    article_body_text = ""
    found_content = False

    # Pattern 1: <article> tag
    article_tag = re.search(r'<article[^>]*>(.*?)</article>', content, re.DOTALL | re.IGNORECASE)
    if article_tag:
        article_body_text = re.sub(r'<[^>]+>', '', article_tag.group(1))
        article_body_text = re.sub(r'\s+', '', article_body_text)
        if len(article_body_text) >= 200:
            found_content = True

    # Pattern 2: div with class="article-body"
    if not found_content:
        ab_match = re.search(r'<div[^>]*class=["\']article-body["\'][^>]*>', content, re.IGNORECASE)
        if ab_match:
            start = ab_match.end()
            depth = 1
            i = start
            while i < len(content) and depth > 0:
                if content[i:i+5] in ['<div ', '<div>']:
                    depth += 1
                elif content[i:i+6] == '</div>':
                    depth -= 1
                i += 1
            article_body_text = re.sub(r'<[^>]+>', '', content[start:i-6])
            article_body_text = re.sub(r'\s+', '', article_body_text)
            if len(article_body_text) >= 200:
                found_content = True

    # Pattern 3: div with id="article-body"
    if not found_content:
        ab_match = re.search(r'<div[^>]*id=["\']article-body["\'][^>]*>', content, re.IGNORECASE)
        if ab_match:
            start = ab_match.end()
            depth = 1
            i = start
            while i < len(content) and depth > 0:
                if content[i:i+5] in ['<div ', '<div>']:
                    depth += 1
                elif content[i:i+6] == '</div>':
                    depth -= 1
                i += 1
            article_body_text = re.sub(r'<[^>]+>', '', content[start:i-6])
            article_body_text = re.sub(r'\s+', '', article_body_text)
            if len(article_body_text) >= 200:
                found_content = True

    if not found_content:
        issues.append(f"文章正文过短或缺失({len(article_body_text)}字符)")
    elif len(article_body_text) < 200:
        issues.append(f"文章正文过短({len(article_body_text)}字符)")

    # SEO meta - use full patterns
    og_title = re.search(r'property=["\']og:title["\']', content, re.IGNORECASE)
    if not og_title:
        issues.append("og:title缺失")

    desc = re.search(r'<meta[^>]+name=["\']description["\']', content, re.IGNORECASE)
    if not desc:
        issues.append("description meta缺失")

    canonical = re.search(r'<link[^>]+rel=["\']canonical["\']', content, re.IGNORECASE)
    if not canonical:
        issues.append("canonical链接缺失")

    # reading time
    read_time = re.search(r'阅读|分钟|min|read', content, re.IGNORECASE)
    if not read_time:
        issues.append("无阅读时间估算")

    # 3. Layout
    # body style
    body_style = re.search(r'body[^}]*\{[^}]*background', content, re.IGNORECASE)
    if not body_style:
        issues.append("body无背景样式")

    # sidebar content not empty
    sidebar_div = re.search(r'<div[^>]*\bid=["\']sidebar["\'][^>]*>(.*?)</div>', content, re.DOTALL | re.IGNORECASE)
    if not sidebar_div:
        sidebar_div = re.search(r'<aside[^>]*>(.*?)</aside>', content, re.DOTALL | re.IGNORECASE)
    if sidebar_div:
        sidebar_text = re.sub(r'<[^>]+>', '', sidebar_div.group(1))
        sidebar_text = re.sub(r'\s+', '', sidebar_text)
        if len(sidebar_text) < 10:
            issues.append("侧边栏内容为空或过少")

    # 4. Mobile
    viewport = re.search(r'<meta[^>]+name=["\']viewport["\']', content, re.IGNORECASE)
    if not viewport:
        issues.append("viewport meta缺失")

    responsive = re.search(r'@media\s*\(', content)
    if not responsive:
        issues.append("无响应式CSS(@media)")

    if issues:
        status = "problem"

    return {"status": status, "issues": issues, "filepath": filepath, "site": site_name}


def main():
    sites = [
        {"name": "morai.top", "path": r"C:\Users\Administrator\github\morai-website", "baidu": True},
        {"name": "novelpick.top", "path": r"C:\Users\Administrator\github\novelpick-website", "baidu": True},
        {"name": "fateandmethod.com", "path": r"C:\Users\Administrator\github\fateandmethod-site", "baidu": False},
    ]

    all_results = []
    total_normal = 0
    total_problem = 0

    for site in sites:
        html_files = list(Path(site["path"]).rglob("*.html"))
        print(f"\n=== {site['name']} === (共 {len(html_files)} 个文件)")

        for f in html_files:
            res = audit_file(str(f), site["name"], site["baidu"])
            all_results.append(res)
            fname = f.name
            if res["status"] == "problem":
                total_problem += 1
                print(f"  [PROBLEM] {fname}")
                for issue in res["issues"]:
                    print(f"           - {issue}")
            else:
                total_normal += 1
                print(f"  [OK] {fname}")

    print("\n" + "=" * 50)
    print("汇总")
    print("=" * 50)
    total = total_normal + total_problem
    print(f"总页面数: {total}")
    print(f"正常: {total_normal}")
    print(f"有问题: {total_problem}")

    problem_files = [r for r in all_results if r["status"] == "problem"]
    if problem_files:
        print("\n=== 问题文件列表 ===")
        for f in problem_files:
            print(f"\n文件: {f['filepath']}")
            for issue in f["issues"]:
                print(f"  问题: {issue}")

    # Write to file
    with open(r"C:\Users\Administrator\.openclaw\workspace\audit-report-v2.txt", "w", encoding="utf-8") as out:
        out.write("网站巡检报告 v2\n")
        out.write("=" * 50 + "\n\n")
        out.write(f"巡检时间: 2026-04-25 09:00\n\n")
        out.write(f"总页面数: {total}\n")
        out.write(f"正常: {total_normal}\n")
        out.write(f"有问题: {total_problem}\n\n")

        if problem_files:
            out.write("=== 问题文件 ===\n\n")
            for f in problem_files:
                out.write(f"文件: {f['filepath']}\n")
                for issue in f["issues"]:
                    out.write(f"  - {issue}\n")
                out.write("\n")

if __name__ == "__main__":
    main()
