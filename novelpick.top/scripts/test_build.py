#!/usr/bin/env python3
"""Patch fix_html.py to strip original nav and breadcrumb from body."""
import re

f = r'C:\Users\Administrator\.openclaw\workspace\scripts\fix_html.py'
content = open(f, encoding='utf-8').read()

# In both parse_dup_head and parse_scripts_in_head, strip nav/breadcrumb from body
# Add after "body_raw = body_raw.replace(s, '\n__SP__\n')" or similar

old_pattern = '''    body_raw = body_raw.replace(s, '\\n__SP__\\n')
    return {'meta_tags': meta_tags, 'css': css, 'body': body_raw.strip(), 'scripts': scripts}


def parse_scripts_in_head'''

new_code = '''    body_raw = body_raw.replace(s, '\\n__SP__\\n')
    # Remove original nav and breadcrumb from body (we add our own nav)
    body_raw = re.sub(r'<nav>.*?</nav>', '', body_raw, flags=re.DOTALL)
    body_raw = re.sub(r'<div class="breadcrumb">.*?</div>', '', body_raw, flags=re.DOTALL)
    return {'meta_tags': meta_tags, 'css': css, 'body': body_raw.strip(), 'scripts': scripts}


def parse_scripts_in_head'''

if old_pattern in content:
    content = content.replace(old_pattern, new_code)
    print('Patched parse_dup_head')
else:
    print('Could not find parse_dup_head pattern')

# Also patch parse_scripts_in_head body_raw handling
old2 = '''    scripts = re.findall(r'<script[^>]*>.*?</script>', c[se:hc], re.DOTALL)
    bs = c.find('<body>', hc)
    be_tag = c.find('>', bs) + 1
    be = c.rfind('</body>')
    if be == -1:
        be = len(c)
    body_raw = c[be_tag:be].strip()
    return {'meta_tags': meta_tags, 'css': css, 'body': body_raw.strip(), 'scripts': scripts}


def dedup_meta'''

new2 = '''    scripts = re.findall(r'<script[^>]*>.*?</script>', c[se:hc], re.DOTALL)
    bs = c.find('<body>', hc)
    be_tag = c.find('>', bs) + 1
    be = c.rfind('</body>')
    if be == -1:
        be = len(c)
    body_raw = c[be_tag:be].strip()
    # Remove original nav and breadcrumb from body (we add our own nav)
    body_raw = re.sub(r'<nav>.*?</nav>', '', body_raw, flags=re.DOTALL)
    body_raw = re.sub(r'<div class="breadcrumb">.*?</div>', '', body_raw, flags=re.DOTALL)
    return {'meta_tags': meta_tags, 'css': css, 'body': body_raw.strip(), 'scripts': scripts}


def dedup_meta'''

if old2 in content:
    content = content.replace(old2, new2)
    print('Patched parse_scripts_in_head')
else:
    print('Could not find parse_scripts_in_head pattern')

open(f, 'w', encoding='utf-8').write(content)
print('File written')
