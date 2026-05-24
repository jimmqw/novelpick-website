# -*- coding: utf-8 -*-
from pathlib import Path
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Get Baidu code from morai as reference
morai_files = list(Path(r'C:\Users\Administrator\github\morai-website').rglob('*.html'))
baidu_code = None
for f in morai_files:
    try:
        c = f.read_text(encoding='utf-8', errors='ignore')
        if 'hm.baidu.com' in c:
            idx = c.find('hm.baidu.com')
            baidu_code = c[idx-10:idx+80]
            print('MORAI BAIDU:', baidu_code)
            break
    except:
        pass

# Check which novelpick pages have baidu vs which don't
novel_files = list(Path(r'C:\Users\Administrator\github\novelpick-website').rglob('*.html'))
with_baidu = []
without_baidu = []
for f in novel_files:
    try:
        c = f.read_text(encoding='utf-8', errors='ignore')
        if 'hm.baidu.com' in c:
            with_baidu.append(f.name)
        else:
            without_baidu.append(f.name)
    except:
        pass

print(f'\nNovelPick with Baidu: {len(with_baidu)}')
print(f'NovelPick without Baidu: {len(without_baidu)}')
print('Files WITH baidu:', with_baidu[:5] if with_baidu else 'none')
print('Files WITHOUT baidu (first 10):', without_baidu[:10])
