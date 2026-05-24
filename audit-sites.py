# -*- coding: utf-8 -*-
import os, re
from pathlib import Path

DIRS = {
    'morai':         r'C:\Users\Administrator\github\morai-website',
    'novelpick':     r'C:\Users\Administrator\github\novelpick-website',
    'fateandmethod': r'C:\Users\Administrator\github\fateandmethod-site',
}

INDEX_PAGES = {
    'morai': ['index.html','search.html','deals.html','template.html',
              'ai-tools.html','ai-reviews.html','ai-comparisons.html','ai-guides.html'],
    'novelpick': ['index.html','fantasy.html','litrpg.html','romance.html','scifi.html','reviews.html'],
    'fateandmethod': ['index.html','daliuren.html','liuyao.html','meihua.html','taiyi.html',
                       'xiaoliuren.html','xuankong.html','bazi.html',
                       'feng-shui-fundamentals.html','five-elements-complete-guide.html',
                       'ziwei.html','chinese-zodiac-luck-rankings-2026.html',
                       'daliuren-index.html','liuyao-index.html','meihua-index.html',
                       'taiyi-index.html','xiaoliuren-index.html','xuankong-index.html'],
}

def get_article_body_text(html):
    """Extract text from article-body div/main, using depth-balanced tag matching.
    Supports: <main class="article-body"> (novelpick), <div class="article-body"> (morai),
    and <div class="article-content article-body"> (fateandmethod multi-class)."""
    # Try <main class="article-body"> (novelpick)
    m = re.search(r'<main[^>]*\bclass="article-body"[^>]*>', html)
    tag = 'main'
    if not m:
        # Try <div class="article-body"> or <div ... article-body ...>
        # Match both single and multi-class attributes
        m = re.search(r'<div[^>]*\bclass="[^"]*article-body[^"]*"[^>]*>', html)
        tag = 'div'
    if not m:
        return ''

    depth = 1
    start = m.start()
    open_end = html.find('>', start)
    if open_end < 0:
        return ''
    scan_from = open_end + 1

    open_pat = re.compile(r'<' + tag + r'\b')
    close_pat = re.compile(r'</' + tag + r'>')

    for m2 in re.finditer(r'<' + tag + r'\b|</' + tag + r'>', html[scan_from:]):
        rel_pos = scan_from + m2.start()
        if html[rel_pos:rel_pos+2] == '</':
            depth -= 1
            if depth == 0:
                content = html[start:rel_pos + len('</%s>' % tag)]
                text = re.sub(r'<[^>]+>', '', content)
                return text.strip()
        else:
            depth += 1
    return ''

    # Use finditer to efficiently find all open/close tags
    # Scan from the start of the tag
    depth = 1
    start = m.start()
    # Find position after the opening tag's >
    open_end = html.find('>', start)
    if open_end < 0:
        return ''
    scan_from = open_end + 1

    # Build a combined pattern for speed
    if tag == 'main':
        open_pat = re.compile(r'<main\b')
    else:
        open_pat = re.compile(r'<div\b')
    close_pat = re.compile(r'</' + tag + r'>')

    last_pos = start
    for m2 in re.finditer(r'<' + tag + r'\b|</' + tag + r'>', html[scan_from:]):
        rel_pos = scan_from + m2.start()
        if html[rel_pos:rel_pos+2] == '</':
            # close tag
            depth -= 1
            if depth == 0:
                # end found
                content = html[start:rel_pos + len('</%s>' % tag)]
                text = re.sub(r'<[^>]+>', '', content)
                return text.strip()
        else:
            # open tag
            depth += 1
    return ''

def audit(path, site):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    if len(c) < 200:
        return ['[file-too-short]']
    fname = os.path.basename(path)
    issues = []

    # 1. structure
    if not re.search(r'<header|class="[^"]*header|class="[^"]*nav[^"]*"', c):
        issues.append('[header/nav-missing]')
    if not re.search(r'<nav[^>]*>', c):
        issues.append('[nav-missing]')
    if not re.search(r'breadcrumb', c, re.IGNORECASE):
        issues.append('[breadcrumb-missing]')
    if not re.search(r'<aside|class="[^"]*sidebar', c, re.IGNORECASE):
        issues.append('[sidebar-missing]')
    if not re.search(r'related|相关文章|推荐阅读', c, re.IGNORECASE):
        issues.append('[related-posts-missing]')
    if not re.search(r'<footer', c):
        issues.append('[footer-missing]')

    # 2. baidu stat
    if site != 'fateandmethod' and fname not in INDEX_PAGES.get(site, []):
        if not re.search(r'hm\.baidu\.com', c):
            issues.append('[baidu-stat-missing]')

    # 3. content quality
    if fname not in INDEX_PAGES.get(site, []):
        ab_text = get_article_body_text(c)
        if not ab_text:
            issues.append('[article-body-missing]')
        elif len(ab_text) < 200:
            issues.append('[content-too-short:' + str(len(ab_text)) + 'chars]')

        if not re.search(r'og:title', c):
            issues.append('[og:title-missing]')
        if not re.search(r'og:description', c):
            issues.append('[og:description-missing]')
        if not re.search(r'canonical', c, re.IGNORECASE):
            issues.append('[canonical-missing]')
        if not re.search(r'阅读|分钟|min read', c):
            issues.append('[read-time-missing]')

    # 4. layout/mobile
    if not re.search(r'background', c):
        issues.append('[bg-style-missing]')
    if not re.search(r'viewport', c):
        issues.append('[viewport-missing]')
    if not re.search(r'@media', c):
        issues.append('[responsive-css-missing]')

    return issues

def main():
    total = ok = bad = 0
    problems = []
    counts = {}
    for site, base in DIRS.items():
        if not os.path.isdir(base):
            continue
        files = list(Path(base).rglob('*.html'))
        counts[site] = len(files)
        for f in files:
            total += 1
            issues = audit(str(f), site)
            if not issues:
                ok += 1
            else:
                bad += 1
                problems.append((site, str(f.relative_to(base)), issues))

    import datetime
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    print('=== Daily Site Audit Report ' + now + ' ===')
    print()
    print('Stats:')
    print('Total pages: ' + str(total))
    for s, n in counts.items():
        print('  ' + s + ': ' + str(n) + ' files')
    print('OK: ' + str(ok))
    print('Problems: ' + str(bad))
    print()

    if problems:
        print('PROBLEMS:')
        for site, rel, issues in problems:
            print('[' + site + '] ' + rel)
            print('  ' + ' '.join(issues))
    else:
        print('ALL CLEAR - No issues found')

    with open(r'C:\Users\Administrator\.openclaw\workspace\audit-report.txt', 'w', encoding='utf-8') as out:
        out.write('=== Daily Site Audit Report ' + now + ' ===\n\n')
        out.write('Stats:\n- Total: ' + str(total) + '\n- OK: ' + str(ok) + '\n- Problems: ' + str(bad) + '\n\n')
        if problems:
            out.write('PROBLEMS:\n')
            for site, rel, issues in problems:
                out.write('[' + site + '] ' + rel + '\n')
                out.write('  ' + ' '.join(issues) + '\n')
        else:
            out.write('ALL CLEAR\n')

if __name__ == '__main__':
    main()