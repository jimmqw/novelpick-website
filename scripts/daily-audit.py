#!/usr/bin/env python3
"""Daily website quality audit for morai.top, novelpick.top, fateandmethod.com"""
import os, re, sys
from datetime import datetime

SITES = {
    'morai.top': {
        'dir': r'C:\Users\Administrator\github\morai-website',
        'baidu': True
    },
    'novelpick.top': {
        'dir': r'C:\Users\Administrator\github\novelpick-website',
        'baidu': True
    },
    'fateandmethod.com': {
        'dir': r'C:\Users\Administrator\github\fateandmethod-site',
        'baidu': False
    }
}


def extract_text(html):
    text = re.sub(r'<[^>]+>', '', html)
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<')
    text = text.replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'")
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_article_body(content):
    """Extract article body content, returning (text, length)"""
    # Try <article> tag first
    m = re.search(r'<article[^>]*>(.*?)</article>', content, re.DOTALL)
    if m:
        return extract_text(m.group(1)), len(extract_text(m.group(1)))

    # Try class="article-body" div with balanced nesting
    m = re.search(r'class="article-body"[^>]*>', content)
    if m:
        start = m.end()
        # Find the matching closing </div> with balanced div counting
        depth = 1
        i = start
        while i < len(content) and depth > 0:
            open_tag = content.find('<div', i)
            close_tag = content.find('</div>', i)
            if close_tag == -1:
                break  # malformed HTML
            if open_tag != -1 and open_tag < close_tag:
                depth += 1
                i = open_tag + 4
            else:
                depth -= 1
                i = close_tag + 6
        body_html = content[start:i-6] if depth == 0 else content[start:]
        return extract_text(body_html), len(extract_text(body_html))

    # Try class="article-content" div
    m = re.search(r'class="article-content"[^>]*>', content)
    if m:
        start = m.end()
        depth = 1
        i = start
        while i < len(content) and depth > 0:
            open_tag = content.find('<div', i)
            close_tag = content.find('</div>', i)
            if close_tag == -1:
                break
            if open_tag != -1 and open_tag < close_tag:
                depth += 1
                i = open_tag + 4
            else:
                depth -= 1
                i = close_tag + 6
        body_html = content[start:i-6] if depth == 0 else content[start:]
        return extract_text(body_html), len(extract_text(body_html))

    return '', 0


def check_file(filepath, site_name, config):
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return ['文件读取失败(编码)'] if os.path.getsize(filepath) > 0 else ['文件读取失败']

    name = os.path.basename(filepath)

    # === 1. Structural checks ===
    # Header: may use <header> or <nav> as page header
    if not re.search(r'<header\b', content) and not re.search(r'<nav\b', content):
        issues.append('header/nav缺失')

    # Breadcrumb
    if not re.search(r'breadcrumb', content, re.IGNORECASE):
        issues.append('面包屑导航缺失')

    # Sidebar (class="sidebar" or <aside>)
    if not re.search(r'sidebar', content, re.IGNORECASE):
        issues.append('侧边栏缺失')

    # Related articles
    if not re.search(r'related.?[Aa]rticles|相关文章|relacionados', content):
        issues.append('相关文章区块缺失')

    # Footer
    if not re.search(r'<footer\b', content):
        issues.append('footer缺失')

    # Baidu analytics (only for morai and novelpick)
    if config['baidu'] and not re.search(r'hm\.baidu\.com', content):
        issues.append('百度统计缺失')

    # === 2. Content quality ===
    body_text, body_len = extract_article_body(content)
    is_stub = bool(re.search(r'noindex|stub|placeholder', content, re.IGNORECASE))
    is_nav_page = name in ('index.html', 'deals.html', 'search.html') or bool(re.search(r'generated-index', content))
    
    if not is_stub and not is_nav_page and body_len < 200:
        issues.append(f'内容过短({body_len}字符)')

    if not re.search(r'og:title', content):
        issues.append('og:title缺失')
    if not re.search(r'og:description', content):
        issues.append('og:description缺失')
    if not re.search(r'canonical', content):
        issues.append('canonical缺失')
    if not re.search(r'read[_-]time|阅读时间|min read|分钟阅读', content, re.IGNORECASE):
        issues.append('阅读时间估算缺失')

    # === 3. Layout checks ===
    # CSS: check for background (shorthand or specific)
    if not re.search(r'background[:\s-]', content) and not re.search(r'body\s*\{', content):
        issues.append('body背景色缺失')
    elif not re.search(r'background[:\s-]', content) and not re.search(r'background-color', content):
        # If body has CSS, but no background property at all
        pass  # This is OK - most sites use `background` shorthand not `background-color`

    # Sidebar empty
    if re.search(r'class="sidebar"[^>]*>\s*</aside>|class="sidebar"[^>]*>\s*</div>', content):
        issues.append('侧边栏为空')

    # Footer empty  
    if re.search(r'<footer[^>]*>\s*</footer>', content):
        issues.append('footer内容为空')

    # === 4. Mobile checks ===
    if not re.search(r'viewport', content):
        issues.append('viewport缺失')
    if not re.search(r'@media', content):
        issues.append('@media响应式CSS缺失')

    return issues


def main():
    report = []
    stats = {'total': 0, 'ok': 0, 'issues': 0}

    for site_name, config in SITES.items():
        d = config['dir']
        if not os.path.isdir(d):
            print(f'SKIP: {d} not found')
            continue

        for root, dirs, files in os.walk(d):
            dirs[:] = [d for d in dirs if d not in ('node_modules', '.git')]
            for f in files:
                if not f.endswith('.html'):
                    continue
                fpath = os.path.join(root, f)
                stats['total'] += 1
                fissues = check_file(fpath, site_name, config)
                rel = os.path.relpath(fpath, d)
                if fissues:
                    stats['issues'] += 1
                    report.append({'site': site_name, 'file': rel, 'status': 'ISSUE', 'issues': fissues})
                else:
                    stats['ok'] += 1
                    report.append({'site': site_name, 'file': rel, 'status': 'OK', 'issues': []})

    # Output
    print()
    print('=' * 60)
    print('  网站每日巡检报告')
    print('  巡检时间:', datetime.now().strftime('%Y-%m-%d %H:%M'))
    print('=' * 60)
    print()

    issue_pages = [p for p in report if p['status'] == 'ISSUE']
    ok_pages = [p for p in report if p['status'] == 'OK']

    if issue_pages:
        print('=== 有问题的页面 ===')
        current_site = None
        for p in issue_pages:
            if p['site'] != current_site:
                current_site = p['site']
                print(f'\n[{current_site}]')
            print(f'  {p["file"]}:', ', '.join(p['issues']))

    if ok_pages:
        print('\n=== 所有正常页面 ===')
        current_site = None
        for p in ok_pages:
            if p['site'] != current_site:
                current_site = p['site']
                print(f'  [{current_site}]')
            print(f'    - {p["file"]}')
    
    print()
    print('=== 统计 ===')
    print(f'  总页面数: {stats["total"]}')
    print(f'  正常: {stats["ok"]}个')
    print(f'  有问题: {stats["issues"]}个')

    # Per-site
    print()
    for site_name, config in SITES.items():
        if not os.path.isdir(config['dir']):
            continue
        site_total = len([p for p in report if p['site'] == site_name])
        site_ok = len([p for p in report if p['site'] == site_name and p['status'] == 'OK'])
        site_issue = len([p for p in report if p['site'] == site_name and p['status'] == 'ISSUE'])
        print(f'  {site_name}: 共{site_total}页, 正常{site_ok}, 问题{site_issue}')

    return 0


if __name__ == '__main__':
    sys.exit(main())
