#!/usr/bin/env python3
"""Full accurate audit of all three sites - no false positives."""
import re, os, sys, glob
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sites = {
    'morai.top': r'C:\Users\Administrator\github\morai-website',
    'novelpick.top': r'C:\Users\Administrator\github\novelpick-website',
    'fateandmethod.com': r'C:\Users\Administrator\github\fateandmethod-site'
}

for sname, sdir in sites.items():
    files = sorted(glob.glob(sdir + '/**/*.html', recursive=True))
    files = [f for f in files if 'node_modules' not in f and '.git' not in f]
    
    real_issues = {}
    for fp in files:
        fn = os.path.basename(fp)
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                c = f.read()
        except:
            real_issues[fn] = ['文件编码损坏']
            continue
        
        issues = []
        
        # Header
        if not re.search(r'<header[^>]*>', c):
            issues.append('header缺失')
        
        # Nav
        if not re.search(r'<nav[^>]*>', c):
            issues.append('nav缺失')
        
        # Breadcrumb
        if not re.search(r'breadcrumb|面包屑', c):
            issues.append('面包屑缺失')
        
        # Sidebar (aside)
        if not re.search(r'<aside[^>]*>', c):
            issues.append('侧边栏缺失')
        elif sname == 'morai.top':
            m = re.search(r'<aside[^>]*>(.*?)</aside>', c, re.DOTALL)
            if m:
                text = re.sub(r'<[^>]+>', '', m.group(1))
                text = re.sub(r'\s+', '', text)
                if len(text) < 50:
                    issues.append('侧边栏空(share-bar)')
        
        # Related articles
        if not re.search(r'相关文章|related', c):
            issues.append('相关文章缺失')
        
        # Footer
        if not re.search(r'<footer[^>]*>', c):
            issues.append('footer缺失')
        else:
            m = re.search(r'<footer[^>]*>(.*?)</footer>', c, re.DOTALL)
            if m:
                f_text = m.group(1)
                if not re.search(r'©|&copy;|copyright|Copyright|Copy', f_text):
                    issues.append('footer无版权')
        
        # Baidu analytics
        if sname != 'fateandmethod.com' and not re.search(r'hm\.baidu\.com', c):
            issues.append('百度统计缺失')
        
        # Article content length
        article = re.search(r'<article[^>]*>(.*?)</article>', c, re.DOTALL)
        if article:
            text = re.sub(r'<[^>]+>', '', article.group(1))
            text = re.sub(r'\s+', '', text)
            if len(text) < 200:
                issues.append(f'内容过短({len(text)}字)')
        
        # SEO
        if not re.search(r'og:title', c):
            issues.append('缺og:title')
        if not re.search(r'name="description"', c):
            issues.append('缺description')
        if not re.search(r'canonical', c):
            issues.append('缺canonical')
        
        # Reading time
        if not re.search(r'阅读时间|reading.?time|约.*分钟|min read|阅读时长', c):
            issues.append('缺阅读时间')
        
        # Div balance
        opend = len(re.findall(r'<div[\s>]', c))
        closed = len(re.findall(r'</div>', c))
        if opend != closed:
            issues.append(f'div不平衡({opend}开{closed}闭)')
        
        # Main tag balance
        o = len(re.findall(r'<main[\s>]', c))
        cl = len(re.findall(r'</main>', c))
        if o != cl and o > 0:
            issues.append(f'main标签不平衡')
        
        # DOCTYPE
        if not re.search(r'<!DOCTYPE', c, re.IGNORECASE):
            issues.append('缺DOCTYPE')
        if not re.search(r'</html>', c):
            issues.append('缺/html闭合')
        
        # Mobile
        if not re.search(r'viewport', c):
            issues.append('缺viewport')
        if not re.search(r'@media', c):
            issues.append('缺@media')
        
        if issues:
            real_issues[fn] = issues
    
    print()
    print(f'=== {sname} ({len(files)} files) ===')
    print(f'  正常: {len(files) - len(real_issues)}  |  有问题: {len(real_issues)}')
    print()
    
    # Issue type counts
    counts = {}
    for fn, issues in real_issues.items():
        for i in issues:
            # Normalize issue names
            k = i
            if '不平衡' in i:
                k = '标签不平衡'
            elif '过短' in i:
                k = '内容过短'
            elif '侧边栏空' in i:
                k = '侧边栏空'
            elif '编码' in i:
                k = '文件损坏'
            counts[k] = counts.get(k, 0) + 1
    
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        print(f'  {k}: {v}页')
    
    # Detailed list
    print()
    print(f'  --- 问题详情 ---')
    for fn in sorted(real_issues.keys()):
        print(f'  {fn}:')
        for i in real_issues[fn]:
            print(f'     - {i}')
