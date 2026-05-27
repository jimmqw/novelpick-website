#!/usr/bin/env python3
"""Verify audit results - check real status of header/footer/nav etc."""
import re, glob, os, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sites = {
    'morai': r'C:\Users\Administrator\github\morai-website',
    'novelpick': r'C:\Users\Administrator\github\novelpick-website',
    'fateandmethod': r'C:\Users\Administrator\github\fateandmethod-site'
}

for sname, sdir in sites.items():
    files = glob.glob(sdir + '/**/*.html', recursive=True)
    files = [f for f in files if 'node_modules' not in f and '.git' not in f]
    has_header = []
    no_header = []
    for fp in sorted(files):
        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            c = f.read()
        if re.search(r'<header[^>]*>', c):
            has_header.append(fp)
        else:
            no_header.append(fp)
    
    print(f'\n=== {sname} ({len(files)} files) ===')
    print(f'Has <header>: {len(has_header)}')
    print(f'No <header>: {len(no_header)}')
    
    if has_header:
        for h in has_header[:3]:
            with open(h, 'r', encoding='utf-8', errors='replace') as f:
                c = f.read()
            hdrs = re.findall(r'<header[^>]*>', c)
            navs = re.findall(r'<nav[^>]*>', c)
            footers = re.findall(r'<footer[^>]*>', c)
            baidu = bool(re.search(r'hm\.baidu\.com', c))
            breadcrumb = bool(re.search(r'breadcrumb|面包屑', c))
            sidebar = bool(re.search(r'<aside[^>]*>', c))
            related = bool(re.search(r'相关文章|related', c))
            print(f'  OK: {os.path.basename(h)} header={len(hdrs)} nav={len(navs)} footer={len(footers)} baidu={baidu} breadcrumb={breadcrumb} sidebar={sidebar} related={related}')
    
    if no_header:
        for h in no_header[:3]:
            with open(h, 'r', encoding='utf-8', errors='replace') as f:
                c = f.read()
            navs = re.findall(r'<nav[^>]*>', c)
            footers = re.findall(r'<footer[^>]*>', c)
            baidu = bool(re.search(r'hm\.baidu\.com', c))
            breadcrumb = bool(re.search(r'breadcrumb|面包屑', c))
            sidebar = bool(re.search(r'<aside[^>]*>', c))
            related = bool(re.search(r'相关文章|related', c))
            print(f'  NO-HDR: {os.path.basename(h)} nav={len(navs)} footer={len(footers)} baidu={baidu} breadcrumb={breadcrumb} sidebar={sidebar} related={related}')
    
    # Check for sidebar issue - pages that have sidebar but content too short
    sidebar_short = []
    for fp in files:
        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            c = f.read()
        m = re.search(r'<aside[^>]*>(.*?)</aside>', c, re.DOTALL)
        if m:
            text = re.sub(r'<[^>]+>', '', m.group(1))
            text = re.sub(r'\s+', '', text)
            if len(text) < 50:
                sidebar_short.append(os.path.basename(fp))
    print(f'  Sidebar exists but content under 50 chars: {len(sidebar_short)}')
    if sidebar_short[:5]:
        print(f'    e.g. {sidebar_short[:3]}')
    print()
