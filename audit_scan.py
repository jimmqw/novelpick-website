# -*- coding: utf-8 -*-
import os, re, json
from pathlib import Path

base_paths = [
    r'C:\Users\Administrator\github\morai-website',
    r'C:\Users\Administrator\github\novelpick-website',
    r'C:\Users\Administrator\github\fateandmethod-website',
]

results = []
for base in base_paths:
    site = Path(base).name
    htmls = list(Path(base).rglob('*.html'))
    for f in htmls:
        try:
            content = open(f, encoding='utf-8').read()
        except:
            try:
                content = open(f, encoding='gbk', errors='ignore').read()
            except:
                continue
        rel = f.as_posix().replace(Path(base).as_posix(), '').lstrip('/')
        rel = rel.replace('\\', '/')
        issues = []

        # structural
        if not re.search(r'<header', content): issues.append('header缺失')
        if not re.search(r'<nav', content): issues.append('nav缺失')
        if not re.search(r'breadcrumb', content): issues.append('面包屑缺失')
        if not re.search(r'<aside|sidebar', content, re.IGNORECASE): issues.append('侧边栏缺失')
        if not re.search(r'相关|related|推荐文章', content): issues.append('相关文章缺失')
        if not re.search(r'<footer', content): issues.append('footer缺失')
        if site in ['morai-website', 'novelpick-website'] and not re.search(r'hm\.baidu\.com', content): issues.append('百度统计缺失')

        # content
        body = re.search(r'(?s)<div[^>]*class="[^"]*article-body[^"]*"[^>]*>(.*?)(?=</article|</div>\s*</main|<footer)', content)
        if body:
            clean = re.sub(r'<[^>]+>', '', body.group(1))
            if len(clean.strip()) < 200: issues.append('内容过短')
        if not re.search(r'og:title', content): issues.append('og:title缺失')
        if not re.search(r'og:description|<meta[^>]*name=["\']description["\']', content): issues.append('description缺失')
        if not re.search(r'canonical', content): issues.append('canonical缺失')
        if not re.search(r'阅读|分钟|min|read', content): issues.append('阅读时间缺失')

        # layout
        if not re.search(r'background-color|background:', content): issues.append('CSS样式异常')
        sb = re.search(r'(?s)<aside[^>]*>(.*?)</aside>', content) or re.search(r'(?s)<div[^>]*sidebar[^>]*>(.*?)</div>', content, re.IGNORECASE)
        if sb:
            clean_sb = re.sub(r'<[^>]+>', '', sb.group(0))
            if len(clean_sb.strip()) < 50: issues.append('侧边栏内容空')
        op = len(re.findall(r'<div[^>]*>', content))
        cl = len(re.findall(r'</div>', content))
        if op != cl: issues.append(f'div嵌套不平衡(开{op}/关{cl})')

        # mobile
        if not re.search(r'viewport', content): issues.append('viewport缺失')
        if not re.search(r'@media', content): issues.append('响应式CSS缺失')

        results.append({'site': site, 'file': rel, 'issues': issues, 'ok': len(issues) == 0})

ok_list = [r for r in results if r['ok']]
bad_list = [r for r in results if not r['ok']]

# Write to file with UTF-8
with open(r'C:\Users\Administrator\.openclaw\workspace\audit_results.json', 'w', encoding='utf-8') as out:
    out.write(json.dumps({'ok': ok_list, 'bad': bad_list, 'summary': {
        'total': len(results), 'ok': len(ok_list), 'bad': len(bad_list)
    }}, ensure_ascii=False, indent=2))

print('Done. Total:', len(results), 'Bad:', len(bad_list), 'OK:', len(ok_list))
