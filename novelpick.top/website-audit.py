# -*- coding: utf-8 -*-
"""
Website Daily Audit Script - v3
Simplified and more reliable checks
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Site configurations
SITES = {
    "morai": {
        "path": r"C:\Users\Administrator\github\morai-website",
        "baidu_analytics": True,
        "theme": "dark-blue"
    },
    "novelpick": {
        "path": r"C:\Users\Administrator\github\novelpick-website",
        "baidu_analytics": True,
        "theme": "purple"
    },
    "fateandmethod": {
        "path": r"C:\Users\Administrator\github\fateandmethod-site",
        "baidu_analytics": False,
        "theme": "gold"
    }
}

class AuditResult:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.issues: List[Tuple[str, str]] = []
        self.ok_checks: List[str] = []
        
    def add_issue(self, issue_type: str, description: str):
        self.issues.append((issue_type, description))
        
    def add_ok(self, check_name: str):
        self.ok_checks.append(check_name)
        
    @property
    def is_ok(self) -> bool:
        return len(self.issues) == 0

def read_html(file_path: str) -> str:
    """Read HTML file with proper encoding"""
    encodings = ['utf-8', 'utf-8-sig', 'gbk', 'gb2312', 'latin-1']
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    with open(file_path, 'rb') as f:
        return f.read().decode('utf-8', errors='replace')

def check_header(html: str) -> bool:
    """Check if header/nav exists with dark gradient background"""
    has_nav_tag = bool(re.search(r'<nav[^>]*>', html, re.IGNORECASE))
    has_header_tag = bool(re.search(r'<header[^>]*>', html, re.IGNORECASE))
    has_gradient = bool(re.search(r'gradient|linear-gradient', html, re.IGNORECASE))
    return (has_nav_tag or has_header_tag) and has_gradient

def check_nav(html: str) -> bool:
    """Check if nav exists with content"""
    has_nav = bool(re.search(r'<nav[^>]*>', html, re.IGNORECASE))
    if not has_nav:
        return False
    nav_match = re.search(r'<nav[^>]*>([\s\S]*?)</nav>', html, re.IGNORECASE)
    if nav_match:
        nav_content = nav_match.group(1)
        return len(re.findall(r'<a\s|nav-|nav_', nav_content, re.IGNORECASE)) > 0
    return True

def check_breadcrumb(html: str) -> bool:
    """Check if breadcrumb navigation exists"""
    return bool(re.search(r'class=["\'][^"\']*breadcrumb[^"\']*["\']', html, re.IGNORECASE))

def check_sidebar(html: str) -> bool:
    """Check if sidebar exists and has content"""
    has_sidebar = bool(re.search(r'<aside[^>]*class=["\'][^"\']*sidebar[^"\']*["\']', html, re.IGNORECASE))
    if not has_sidebar:
        has_sidebar = bool(re.search(r'class=["\'][^"\']*sidebar[^"\']*["\'][^>]*>[\s\S]*?(?:<div|<section|<aside|<ul|<ol)', html, re.IGNORECASE))
    if not has_sidebar:
        return False
    sidebar_match = re.search(r'(?:<aside[^>]*class=["\'][^"\']*sidebar[^"\']*["\'][^>]*>[\s\S]*?</aside>|class=["\'][^"\']*sidebar[^"\']*["\'][^>]*>[\s\S]*?(?:</div>|</section>))', html, re.IGNORECASE)
    if sidebar_match:
        sidebar_content = sidebar_match.group(0)
        has_links = bool(re.search(r'<a\s+href=', sidebar_content, re.IGNORECASE))
        return has_links
    return True

def check_related_articles(html: str) -> bool:
    """Check if related articles section exists with links"""
    has_related = bool(re.search(r'class=["\'][^"\']*related[^"\']*["\']', html, re.IGNORECASE))
    if not has_related:
        return False
    related_match = re.search(r'(?:class=["\'][^"\']*related[^"\']*["\'][^>]*>[\s\S]*?(?:</div>|</section>|</aside>))', html, re.IGNORECASE)
    if related_match:
        return bool(re.search(r'<a\s+href=', related_match.group(0), re.IGNORECASE))
    return True

def check_footer(html: str) -> bool:
    """Check if footer exists with copyright info"""
    has_footer_tag = bool(re.search(r'<footer[^>]*>', html, re.IGNORECASE))
    if not has_footer_tag:
        has_footer_tag = bool(re.search(r'class=["\'][^"\']*footer[^"\']*["\']', html, re.IGNORECASE))
    has_copyright = bool(re.search(r'©|copyright|&copy;|\d{4}', html, re.IGNORECASE))
    return has_footer_tag and has_copyright

def check_baidu_analytics(html: str) -> bool:
    """Check if Baidu analytics code exists"""
    return bool(re.search(r'hm\.baidu\.com|baidu\.com/hm\.js', html))

def check_article_length(html: str) -> bool:
    """Check if article body has substantial content (>200 chars)"""
    article_match = re.search(r'<div[^>]*class=["\'][^"\']*article-body[^"\']*["\'][^>]*>([\s\S]*?)</div>', html, re.IGNORECASE)
    if article_match:
        content = article_match.group(1)
        text = re.sub(r'<[^>]+>', '', content)
        text = re.sub(r'\s+', ' ', text).strip()
        return len(text) > 200
    article_match = re.search(r'<article[^>]*>([\s\S]*?)</article>', html, re.IGNORECASE)
    if article_match:
        content = article_match.group(1)
        text = re.sub(r'<[^>]+>', '', content)
        text = re.sub(r'\s+', ' ', text).strip()
        return len(text) > 200
    return True  # Not a content page, skip

def check_seo_meta(html: str) -> bool:
    """Check if SEO meta tags exist"""
    has_og_title = bool(re.search(r'<meta[^>]+property=["\']og:title["\'][^>]*>', html, re.IGNORECASE))
    has_desc = bool(re.search(r'<meta[^>]+name=["\']description["\'][^>]*>', html, re.IGNORECASE))
    has_canonical = bool(re.search(r'<link[^>]+rel=["\']canonical["\'][^>]*>', html, re.IGNORECASE))
    return has_og_title and has_desc and has_canonical

def check_reading_time(html: str) -> bool:
    """Check if reading time estimate exists"""
    return bool(re.search(r'\d+\s*(min|minute|分钟|阅读)', html, re.IGNORECASE))

def check_css_loaded(html: str) -> bool:
    """Check if CSS styles are loaded"""
    has_style_tag = bool(re.search(r'<style[^>]*>', html, re.IGNORECASE))
    has_css_link = bool(re.search(r'<link[^>]+href=["\'][^"\']*\.css[^"\']*["\']', html, re.IGNORECASE))
    has_body_style = bool(re.search(r'body\s*\{[^}]*background', html, re.IGNORECASE) or 
                          re.search(r'body\s*\{[^}]*background-color', html, re.IGNORECASE))
    return (has_style_tag or has_css_link) and has_body_style

def check_viewport(html: str) -> bool:
    """Check if viewport meta tag exists"""
    return bool(re.search(r'<meta[^>]+name=["\']viewport["\'][^>]*>', html, re.IGNORECASE))

def check_responsive_css(html: str) -> bool:
    """Check if responsive CSS exists (@media queries)"""
    # Match both @media (...) and @media (...) with optional space
    return bool(re.search(r'@media[^\{]*\{', html, re.IGNORECASE))

def check_html_structure(html: str) -> bool:
    """Basic HTML structure sanity check"""
    # Check essential tags exist
    has_html = bool(re.search(r'<html[^>]*>', html, re.IGNORECASE))
    has_head = bool(re.search(r'<head[^>]*>', html, re.IGNORECASE))
    has_body = bool(re.search(r'<body[^>]*>', html, re.IGNORECASE))
    return has_html and has_head and has_body

def audit_file(file_path: str, baidu_required: bool) -> AuditResult:
    """Audit a single HTML file"""
    result = AuditResult(file_path)
    
    try:
        html = read_html(file_path)
    except Exception as e:
        result.add_issue("READ_ERROR", f"Cannot read file: {str(e)}")
        return result
    
    # Basic HTML structure
    if check_html_structure(html):
        result.add_ok("html-structure")
    else:
        result.add_issue("HTML_STRUCTURE", "Missing essential HTML tags (html/head/body)")
    
    # Structural checks
    if check_header(html):
        result.add_ok("header")
    else:
        result.add_issue("HEADER_MISSING", "Header/nav missing or no dark gradient background")
    
    if check_nav(html):
        result.add_ok("nav")
    else:
        result.add_issue("NAV_MISSING", "Navigation missing or empty")
    
    if check_breadcrumb(html):
        result.add_ok("breadcrumb")
    else:
        result.add_issue("BREADCRUMB_MISSING", "Breadcrumb navigation missing")
    
    if check_sidebar(html):
        result.add_ok("sidebar")
    else:
        result.add_issue("SIDEBAR_EMPTY", "Sidebar missing or has no content")
    
    if check_related_articles(html):
        result.add_ok("related-articles")
    else:
        result.add_issue("RELATED_MISSING", "Related articles section missing or has no links")
    
    if check_footer(html):
        result.add_ok("footer")
    else:
        result.add_issue("FOOTER_MISSING", "Footer missing or no copyright info")
    
    # Baidu analytics only for morai and novelpick
    if baidu_required:
        if check_baidu_analytics(html):
            result.add_ok("baidu-analytics")
        else:
            result.add_issue("BAIDU_MISSING", "Baidu analytics code missing (required for morai/novelpick)")
    
    # Content quality checks
    if check_article_length(html):
        result.add_ok("article-length")
    else:
        result.add_issue("CONTENT_SHORT", "Article body less than 200 characters")
    
    if check_seo_meta(html):
        result.add_ok("seo-meta")
    else:
        result.add_issue("SEO_META_MISSING", "Missing og:title, description, or canonical tags")
    
    if check_reading_time(html):
        result.add_ok("reading-time")
    else:
        result.add_issue("READING_TIME_MISSING", "No reading time estimate")
    
    # Layout checks
    if check_css_loaded(html):
        result.add_ok("css-loaded")
    else:
        result.add_issue("CSS_ERROR", "CSS may not be loading properly")
    
    # Mobile checks
    if check_viewport(html):
        result.add_ok("viewport")
    else:
        result.add_issue("VIEWPORT_MISSING", "Missing viewport meta tag")
    
    if check_responsive_css(html):
        result.add_ok("responsive-css")
    else:
        result.add_issue("RESPONSIVE_CSS_MISSING", "No @media queries found - may not support mobile")
    
    return result

def main():
    print("=" * 60)
    print("[WEBSITE AUDIT] Site Quality Report")
    print("=" * 60)
    print("Audit time: 2026-04-21 09:00 (Asia/Shanghai)")
    print()
    
    all_results: Dict[str, List[AuditResult]] = {}
    total_pages = 0
    total_ok = 0
    total_issues = 0
    
    for site_name, config in SITES.items():
        print(f"\n{'='*60}")
        site_url = 'morai.top' if site_name=='morai' else 'novelpick.top' if site_name=='novelpick' else 'fateandmethod.com'
        print(f"[SITE] {site_name.upper()} ({site_url})")
        print(f"{'='*60}")
        
        site_path = Path(config["path"])
        html_files = list(site_path.glob("**/*.html"))
        total_pages += len(html_files)
        
        results = []
        ok_count = 0
        issue_count = 0
        
        for html_file in sorted(html_files):
            result = audit_file(str(html_file), config["baidu_analytics"])
            results.append(result)
            
            if result.is_ok:
                ok_count += 1
            else:
                issue_count += 1
        
        all_results[site_name] = results
        total_ok += ok_count
        total_issues += issue_count
        
        print(f"  Total pages: {len(html_files)}")
        print(f"  [OK] Normal: {ok_count}")
        print(f"  [ISSUE] Problematic: {issue_count}")
        print()
        
        for result in results:
            if not result.is_ok:
                rel_path = Path(result.file_path).relative_to(site_path)
                print(f"  ![ISSUE] {rel_path}")
                for issue_type, desc in result.issues:
                    print(f"     - [{issue_type}] {desc}")
                print()
    
    # Final summary
    print("\n" + "=" * 60)
    print("[SUMMARY] Statistics")
    print("=" * 60)
    print(f"  Total pages: {total_pages}")
    print(f"  [OK] Normal: {total_ok}")
    print(f"  [ISSUE] Problematic: {total_issues}")
    
    if total_issues == 0:
        print("\n[DONE] All pages passed audit, no issues found")
    else:
        print(f"\n[WARNING] Found {total_issues} issues total, see details above")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
