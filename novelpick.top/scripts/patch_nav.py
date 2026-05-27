#!/usr/bin/env python3
"""Patch fix_html.py to strip nav/breadcrumb from body content."""
import re

f = r'C:\Users\Administrator\.openclaw\workspace\scripts\fix_html.py'
content = open(f, encoding='utf-8').read()

# Update both parse functions to strip nav and breadcrumb
# In both parse_dup_head and parse_scripts_in_head, after scripts are extracted:
# Strip <nav> and <div class="breadcrumb"> that appear AFTER </header>

old1 = """    for s in scripts:
        body = body.replace(s, '\\n__SP__\\n')
    return {'meta_tags': meta_tags, 'css': css, 'body': body.strip(), 'scripts': scripts}


def parse_scripts_in_head"""

new1 = """    for s in scripts:
        body = body.replace(s, '\\n__SP__\\n')
    # Strip nav and breadcrumb that appear after </header> (duplicate site nav in article)
    header_end = body.find('</header>')
    if header_end != -1:
        body_after_header = body[header_end:]
        nav_in_after = body_after_header.find('<nav>')
        if nav_in_after != -1:
            nav_end = body_after_header.find('</nav>', nav_in_after) + len('</nav>')
            body = body[:header_end] + body_after_header[nav_end:]
        breadcrumb_in_after = body.find('<div class="breadcrumb">')
        if breadcrumb_in_after != -1:
            breadcrumb_end = body.find('</div>', breadcrumb_in_after) + len('</div>')
            body = body[:breadcrumb_in_after] + body[breadcrumb_end:]
    return {'meta_tags': meta_tags, 'css': css, 'body': body.strip(), 'scripts': scripts}


def parse_scripts_in_head"""

if old1 in content:
    content = content.replace(old1, new1)
    print('Patched parse_dup_head')
else:
    print('parse_dup_head pattern not found')

# Patch parse_scripts_in_head
old2 = """    scripts = re.findall(r'<script[^>]*>.*?</script>', c[se:hc], re.DOTALL)
    bs = c.find('<body>', hc)
    be_tag = c.find('>', bs) + 1
    be = c.rfind('</body>')
    if be == -1:
        be = len(c)
    body = c[be_tag:be].strip()
    # Strip original nav and breadcrumb from body (we add our own nav)
    body = re.sub(r'<nav>.*?</nav>', '', body, flags=re.DOTALL)
    body = re.sub(r'<div class="breadcrumb">.*?</div>', '', body, flags=re.DOTALL)
    return {'meta_tags': meta_tags, 'css': css, 'body': body.strip(), 'scripts': scripts}


def dedup_meta"""

new2 = """    scripts = re.findall(r'<script[^>]*>.*?</script>', c[se:hc], re.DOTALL)
    bs = c.find('<body>', hc)
    be_tag = c.find('>', bs) + 1
    be = c.rfind('</body>')
    if be == -1:
        be = len(c)
    body = c[be_tag:be].strip()
    # Strip nav and breadcrumb that appear after </header> (duplicate site nav in article)
    header_end = body.find('</header>')
    if header_end != -1:
        body_after_header = body[header_end:]
        nav_in_after = body_after_header.find('<nav>')
        if nav_in_after != -1:
            nav_end = body_after_header.find('</nav>', nav_in_after) + len('</nav>')
            body = body[:header_end] + body_after_header[nav_end:]
        breadcrumb_in_after = body.find('<div class="breadcrumb">')
        if breadcrumb_in_after != -1:
            breadcrumb_end = body.find('</div>', breadcrumb_in_after) + len('</div>')
            body = body[:breadcrumb_in_after] + body[breadcrumb_end:]
    return {'meta_tags': meta_tags, 'css': css, 'body': body.strip(), 'scripts': scripts}


def dedup_meta"""

if old2 in content:
    content = content.replace(old2, new2)
    print('Patched parse_scripts_in_head')
else:
    print('parse_scripts_in_head pattern not found')

open(f, 'w', encoding='utf-8').write(content)
print('File written')
