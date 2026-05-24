# -*- coding: utf-8 -*-
import re

files = [
    r"C:\Users\Administrator\github\morai-website\best-ai-image-editors-2026.html",
    r"C:\Users\Administrator\github\fateandmethod-site\ziwei-combinations.html",
    r"C:\Users\Administrator\github\fateandmethod-site\daily-wisdom-car-sickness.html",
]

for fpath in files:
    with open(fpath, 'rb') as f:
        raw = f.read()
    
    footer_start = raw.find(b'<footer')
    footer_end = raw.find(b'</footer>')
    if footer_start >= 0 and footer_end >= 0:
        footer_raw = raw[footer_start:footer_end+9]
        pos2026 = footer_raw.find(b'2026')
        if pos2026 > 0:
            before = footer_raw[max(0,pos2026-40):pos2026]
            print(f"File: {fpath.split('\\')[-1]}")
            print(f"  Before 2026: {before}")
            print()

# Now check what my original copyright regex was checking
# I checked: ©|copyright|&copy;|版权所有
# But the footer uses Chinese character '版' which is different from '版'
print("Checking Chinese chars in footer:")
for fpath in files:
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()
    
    ft = re.search(r'<footer[^>]*>(.*?)</footer>', text, re.DOTALL | re.IGNORECASE)
    if ft:
        fh = ft.group(0)
        has_banquan = u'\u7248\u6743' in fh  # 版权
        has_banquan_suoyou = u'\u7248\u6743\u6240\u6709' in fh  # 版权所有
        has_zhuzuo = u'\u4f5c\u8005' in fh  # 作者
        print(f"File: {fpath.split('\\')[-1]}")
        print(f"  版权: {has_banquan}")
        print(f"  版权所有: {has_banquan_suoyou}")
        print(f"  作者: {has_zhuzuo}")
        # Find position of 2026 in footer text
        ft_text = re.sub(r'<[^>]+>', '', ft.group(1))
        idx = ft_text.find('2026')
        if idx >= 0:
            print(f"  Footer text around 2026: {ft_text[max(0,idx-30):idx+30]}")
        print()
