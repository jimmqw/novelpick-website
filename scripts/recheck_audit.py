"""Re-audit with correct article-body detection"""
import re
import os

def find_article_body_precise(content):
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

def audit_site(site_path, site_name):
    issues = []
    for f in sorted(os.listdir(site_path)):
        if not f.endswith('.html'):
            continue
        filepath = os.path.join(site_path, f)
        try:
            content = open(filepath, encoding='utf-8').read()
        except:
            continue
        
        file_issues = []
        ab = find_article_body_precise(content)
        if ab:
            text = re.sub(r'<[^>]+>', '', ab)
            text_len = len(text.strip())
            if text_len < 200:
                file_issues.append(f"内容过短({text_len}字符)")
        else:
            # Also check if there's article-layout without article-body class/id
            if 'article-layout' not in content and 'article-body' not in content:
                file_issues.append("无article-body结构")
        
        # Header
        if not re.search(r'<header|<nav', content, re.IGNORECASE):
            file_issues.append("header缺失")
        
        # Footer
        if not re.search(r'<footer', content, re.IGNORECASE):
            file_issues.append("footer缺失")
        
        if file_issues:
            issues.append(f"  {f}: {', '.join(file_issues)}")
    
    print(f"\n=== {site_name.upper()} ===")
    if issues:
        for i in issues:
            print(i)
        print(f"有问题页面: {len(issues)}")
    else:
        print("所有页面正常")

audit_site(r'C:\Users\Administrator\github\morai-website', 'morai')
audit_site(r'C:\Users\Administrator\github\novelpick-website', 'novelpick')
audit_site(r'C:\Users\Administrator\github\fateandmethod-site', 'fateandmethod')
