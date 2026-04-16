#!/usr/bin/env python3
import re, os

content = open(r'C:\Users\Administrator\.openclaw\workspace\fateandmethod-fixed\ziwei.html', encoding='utf-8').read()
c = content.replace('\r\n', '\n').replace('\r', '\n')
se = c.find('</style>')
he = c.find('</head>')
segment = c[se:he]
print('Segment length:', len(segment))
print('Has <script:', '<script' in segment)
# Find all script tags
scripts_found = re.findall(r'<script[^>]*>.*?</script>', segment, re.DOTALL)
print('Scripts found with DOTALL:', len(scripts_found))
# Find closing tag pattern
print('Has <" + "/script>:', '<' + ' + ' + '"' + '/script>' in segment)
print('Has </script>:', chr(60) + '/script>' in segment)
# Check raw bytes around the end of segment
print('Last 200 chars of segment:')
print(repr(segment[-200:]))
