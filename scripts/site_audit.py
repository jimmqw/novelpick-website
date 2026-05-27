import re
import os

def analyze_file(filepath, site_name, check_baidu=False):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    issues = []
    rel_path = os.path.relpath(filepath, site_name)

    # Div balance
    open_divs = len(re.findall(r'<div\b(?!/)', content))
    close_divs = len(re.findall(r'</div>', content))
    if open_divs != close_divs:
        issues.append(f"div嵌套不平衡(开{open_divs}/关{close_divs})")

    # Find article content - class names vary across sites
    # Order matters - try more specific matches first
    article_match = None
    patterns = [
        (r'<article[^>]*class="[^"]*article-content[^"]*"[^>]*>(.*?)</article>', re.DOTALL),
        (r'<div[^>]*class="[^"]*article-body[^"]*"[^>]*>(.*?)</div>', re.DOTALL),
        (r'<article[^>]*class="[^"]*article-body[^"]*"[^>]*>(.*?)</article>', re.DOTALL),
        (r'<div[^>]*class="[^"]*article-main[^"]*"[^>]*>(.*?)</div>', re.DOTALL),
        (r'<article[^>]*class="[^"]*article[^"]*"[^>]*>(.*?)</article>', re.DOTALL),
        (r'<article[^>]*>(.*?)</article>', re.DOTALL),
        (r'<main[^>]*>(.*?)</main>', re.DOTALL),
        (r'<div[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</div>', re.DOTALL),
    ]
    
    for pattern, flags in patterns:
        m = re.search(pattern, content, flags)
        if m:
            text = re.sub(r'<[^>]+>', '', m.group(1))
            if len(text.strip()) >= 200:
                article_match = m
                break
            elif article_match is None:
                # remember first match even if short
                pass
    
    if article_match:
        text = re.sub(r'<[^>]+>', '', article_match.group(1))
        if len(text.strip()) < 200:
            issues.append(f"内容过短({len(text)}字符)")
    else:
        # No content block found - check body as last resort
        body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
        if body_match:
            text = re.sub(r'<[^>]+>', '', body_match.group(1))
            if len(text.strip()) < 200:
                issues.append(f"内容过短({len(text)}字符)")
        else:
            issues.append("内容过短(0字符)")

    # Baidu stats
    if check_baidu and 'hm.baidu.com' not in content:
        issues.append("百度统计缺失")

    return issues, open_divs, close_divs

def scan_site(site_path, site_name, check_baidu=False):
    results = []
    for root, dirs, files in os.walk(site_path):
        for fname in files:
            if fname.endswith('.html'):
                fpath = os.path.join(root, fname)
                issues, od, cd = analyze_file(fpath, site_name, check_baidu)
                results.append({
                    'site': site_name,
                    'file': os.path.relpath(fpath, site_path),
                    'issues': issues,
                    'open_divs': od,
                    'close_divs': cd,
                    'status': 'ISSUE' if issues else 'OK'
                })
    return results

sites = [
    ('C:\\Users\\Administrator\\github\\morai-website', 'morai.top', True),
    ('C:\\Users\\Administrator\\github\\novelpick-website', 'novelpick.top', True),
    ('C:\\Users\\Administrator\\github\\fateandmethod-site', 'fateandmethod.com', False),
]

all_results = []
for site_path, site_name, check_baidu in sites:
    results = scan_site(site_path, site_name, check_baidu)
    all_results.extend(results)
    print(f"[{site_name}] Scanned {len(results)} files, {sum(1 for r in results if r['status']=='ISSUE')} issues")

# Print issues
ok = [r for r in all_results if r['status'] == 'OK']
issues = [r for r in all_results if r['status'] == 'ISSUE']

print(f"\n========== AUDIT SUMMARY ==========")
print(f"Total: {len(all_results)} files")
print(f"OK: {len(ok)}")
print(f"Issues: {len(issues)}")

print(f"\n========== ISSUES ==========")
for r in issues:
    print(f"{r['site']} | {r['file']} | {'; '.join(r['issues'])}")