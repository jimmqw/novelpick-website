#!/usr/bin/env python3
"""Daily website quality audit for morai.top, novelpick.top, fateandmethod.com"""
import os, re, glob, json, sys
from datetime import datetime

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SITES = [
    {"name": "morai.top", "dir": r"C:\Users\Administrator\github\morai-website", "baidu": True},
    {"name": "novelpick.top", "dir": r"C:\Users\Administrator\github\novelpick-website", "baidu": True},
    {"name": "fateandmethod.com", "dir": r"C:\Users\Administrator\github\fateandmethod-site", "baidu": False},
]

def check_file(filepath, site_info):
    """Return list of issue strings for a single HTML file."""
    base = os.path.basename(filepath)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return [f"读取失败: {e}"]
    
    issues = []
    
    # ── 1. Structural checks ──
    if not re.search(r'<header[^>]*>', content):
        issues.append("header缺失")
    
    if not re.search(r'<nav[^>]*>', content):
        issues.append("nav缺失")
    
    if not re.search(r'breadcrumb|面包屑|class="breadcrumb', content):
        issues.append("面包屑导航缺失")
    
    sidebar_match = re.search(r'<aside[^>]*>(.*?)</aside>', content, re.DOTALL)
    if not sidebar_match:
        issues.append("侧边栏缺失")
    else:
        sidebar_text = re.sub(r'<[^>]+>', '', sidebar_match.group(1))
        sidebar_text = re.sub(r'\s+', '', sidebar_text)
        if len(sidebar_text) < 30:
            issues.append("侧边栏内容不足")
    
    if not re.search(r'相关文章|related|class="related', content):
        issues.append("相关文章区块缺失")
    
    if not re.search(r'<footer[^>]*>', content):
        issues.append("footer缺失")
    elif not re.search(r'&copy;|copyright|版权|Copy', content):
        issues.append("footer无版权信息")
    
    if site_info["baidu"] and not re.search(r'hm\.baidu\.com', content):
        issues.append("百度统计缺失")
    
    # ── 2. Content quality ──
    article_match = re.search(r'<article[^>]*>(.*?)</article>', content, re.DOTALL)
    if not article_match:
        article_match = re.search(r'class="article-content"[^>]*>(.*?)</div>', content, re.DOTALL)
    
    if article_match:
        article_text = re.sub(r'<[^>]+>', '', article_match.group(1))
        article_text = re.sub(r'\s+', '', article_text)
        if len(article_text) < 200:
            issues.append(f"文章内容过短 ({len(article_text)}字符)")
    
    if not re.search(r'og:title', content):
        issues.append("缺少og:title")
    if not re.search(r'<meta[^>]*name="description"', content):
        issues.append("缺少meta description")
    if not re.search(r'canonical', content):
        issues.append("缺少canonical标签")
    if not re.search(r'阅读时间|reading.?time|约.*分钟|min read|阅读时长', content):
        issues.append("缺少阅读时间估算")
    
    # ── 3. Layout checks ──
    open_divs = len(re.findall(r'<div[\s>]', content))
    close_divs = len(re.findall(r'</div>', content))
    if open_divs != close_divs:
        diff = open_divs - close_divs
        issues.append(f"div标签不平衡 (开:{open_divs} 闭:{close_divs} 差:{diff})")
    
    # Check other structural tags
    for tag in ['article', 'section', 'aside', 'nav', 'header', 'footer', 'main']:
        opens = len(re.findall(f'<{tag}[\\s>]', content))
        closes = len(re.findall(f'</{tag}>', content))
        if opens != closes and opens > 0:
            issues.append(f"{tag}标签不平衡 (开:{opens} 闭:{closes})")
            break
    
    if not re.search(r'<!DOCTYPE\s+html', content, re.IGNORECASE):
        issues.append("缺少DOCTYPE声明")
    if not re.search(r'</html>', content):
        issues.append("缺少</html>闭合标签")
    
    # ── 4. Mobile checks ──
    if not re.search(r'viewport', content):
        issues.append("缺少viewport meta标签")
    if not re.search(r'@media', content):
        issues.append("缺少响应式CSS (@media)")
    
    return issues


def main():
    all_ok = []
    all_issues = []
    total_files = 0
    
    for site in SITES:
        if not os.path.isdir(site["dir"]):
            print(f"[WARN] Directory not found: {site['dir']}")
            continue
        
        html_files = glob.glob(os.path.join(site["dir"], "**", "*.html"), recursive=True)
        html_files = [f for f in html_files if "node_modules" not in f and ".git" not in f]
        total_files += len(html_files)
        
        for filepath in html_files:
            issues = check_file(filepath, site)
            if issues:
                all_issues.append({
                    "site": site["name"],
                    "file": os.path.basename(filepath),
                    "path": filepath,
                    "issues": issues
                })
            else:
                all_ok.append({
                    "site": site["name"],
                    "file": os.path.basename(filepath)
                })
    
    # ── Report ──
    print("=" * 70)
    print(f"  DAILY SITE AUDIT REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    
    print(f"\n✅ Normal Pages: {len(all_ok)}")
    
    if all_issues:
        print(f"\n⚠️  Pages with Issues: {len(all_issues)}")
        
        by_site = {}
        for item in all_issues:
            by_site.setdefault(item["site"], []).append(item)
        
        for site_name, items in by_site.items():
            print(f"\n--- {site_name} ({len(items)} pages) ---")
            for item in items:
                print(f"  📄 {item['file']}")
                for issue in item["issues"]:
                    print(f"     ⚡ {issue}")
    else:
        print("\n🎉 今日巡检完成，所有页面无异常！")
    
    print(f"\n📊 Statistics")
    print(f"  Total pages scanned: {total_files}")
    print(f"  Normal: {len(all_ok)}")
    print(f"  With issues: {len(all_issues)}")
    
    if all_issues:
        # Issue type breakdown
        issue_counts = {}
        for item in all_issues:
            for issue in item["issues"]:
                key = issue.split("(")[0].strip() if "(" in issue else issue
                # normalize keys
                if "不平衡" in key:
                    key = key.split()[0] + "标签不平衡"
                issue_counts[key] = issue_counts.get(key, 0) + 1
        
        print(f"\n  Issue breakdown:")
        for k, v in sorted(issue_counts.items(), key=lambda x: -x[1]):
            print(f"    {k}: {v}")
        
        # Critical issues
        critical = [item for item in all_issues 
                    if any("不平衡" in i or "缺失DOCTYPE" in i or "缺失</html>" in i 
                           or i.startswith("div标签") or i.startswith("article标签")
                           or i == "header缺失" or i == "footer缺失" or i == "nav缺失"
                           for i in item["issues"])]
        if critical:
            print(f"\n🔴 Critical Issues ({len(critical)} pages):")
            for item in critical:
                for issue in item["issues"]:
                    if any(k in issue for k in ["不平衡", "缺失DOCTYPE", "缺失</html>", "header缺失", "footer缺失", "nav缺失"]):
                        print(f"  {item['site']}/{item['file']}: {issue}")
    
    print("\n" + "=" * 70)
    print("  END OF REPORT")
    print("=" * 70)
    
    # Return for programmatic use
    return {"ok": len(all_ok), "issues": len(all_issues), "total": total_files, "details": all_issues}


if __name__ == "__main__":
    main()
