#!/usr/bin/env python3
import re

f = r'C:\Users\Administrator\.openclaw\workspace\scripts\fix_html.py'
content = open(f, encoding='utf-8').read()

# Add _normalize function after _read_file
old_rf_end = "return raw.decode('utf-8', errors='replace')"
insert_pos = content.find(old_rf_end)
if insert_pos == -1:
    print('Could not find _read_file end marker')
else:
    insert_pos += len(old_rf_end)
    new_func = '''

def _normalize(c):
    return c.replace('\\r\\n', '\\n').replace('\\r', '\\n')
'''
    content = content[:insert_pos] + new_func + content[insert_pos:]
    print('Added _normalize')

# Update fix_file to call _normalize
old = 'def fix_file(fpath, site):\n    c = _read_file(fpath)'
new = 'def fix_file(fpath, site):\n    c = _normalize(_read_file(fpath))'
if old in content:
    content = content.replace(old, new)
    print('Updated fix_file to use _normalize')
else:
    print('Could not find fix_file pattern')

# Fix .rstrip() to .strip() for meta tags
content = content.replace('.rstrip() for t in', '.strip() for t in')
print('Updated rstrip to strip')

open(f, 'w', encoding='utf-8').write(content)
print('Done')
