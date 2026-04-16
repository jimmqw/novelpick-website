#!/usr/bin/env python3
"""Fix fateandmethod article pages - handle broken </script> closing tags."""
import re, glob, os

PROGRESS_BAR = '<div class="progress-bar"><div class="progress-fill" id="progressFill"></div>\n'
PROGRESS_SCRIPT = '<script>\nwindow.addEventListener("scroll",function(){var e=document.getElementById("progressFill");if(!e)return;var p=document.documentElement.scrollHeight>window.innerHeight?(window.scrollY/(document.documentElement.scrollHeight-window.innerHeight))*100:0;e.style.width=p+"%";});\n</script>\n'
PROGRESS_CSS = '        .progress-bar{position:fixed;top:64px;left:0;right:0;height:2px;z-index:99;background:var(--gold-border)}.progress-fill{height:100%;background:var(--gold);width:0%;transition:width .1s linear}\n'


def _rf(p):
    with open(p, 'rb') as f:
        raw = f.read()
    if raw.startswith(b'\xff\xfe') or raw.startswith(b'\xfe\xff'):
        return raw.decode('utf-16').encode('utf-8').decode('utf-8')
    for enc in ['utf-8-sig', 'utf-8', 'cp1252']:
        try: return raw.decode(enc)
        except: continue
    return raw.decode('utf-8', errors='replace')


def fix_file(fpath):
    c = _rf(fpath)
    c = c.replace('\r\n', '\n').replace('\r', '\n')

    se = c.find('</style>')
    he = c.find('</head>')
    bs = c.find('<body>', he)

    if se == -1 or he == -1 or bs == -1:
        print(f'  SKIP (malformed): {os.path.basename(fpath)}')
        return False

    # Extract scripts from between </style> and </head>
    # Handle broken closing tags like <" + "/script>
    segment = c[se:he]
    # Fix broken </script> tags (JavaScript string concatenation)
    segment = re.sub(r'<"\s*\+\s*"/script\s*>', '</script>', segment)
    scripts = re.findall(r'<script[^>]*>.*?</script>', segment, re.DOTALL)

    if not scripts:
        print(f'  CLEAN (no scripts in head): {os.path.basename(fpath)}')
        return False

    # 1. Add progress CSS after </style>
    c = c.replace('</style>', '</style>\n' + PROGRESS_CSS, 1)

    # 2. Remove scripts from between </style> and </head>
    # Find the current positions after adding progress CSS
    se_new = c.find('</style>')
    he_new = c.find('</head>')
    # Remove scripts from that segment
    head_segment = c[se_new:he_new]
    for s in scripts:
        head_segment = head_segment.replace(s, '')
    c = c[:se_new] + head_segment + c[he_new:]

    # 3. Add progress bar after <body>
    c = c.replace('<body>\n', '<body>\n' + PROGRESS_BAR, 1)

    # 4. Add scripts before </body>
    c = c.replace('</body>\n', PROGRESS_SCRIPT + '</body>\n', 1)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(c)

    print(f'  FIXED: {os.path.basename(fpath)}')
    return True


def main():
    repodir = r'C:\Users\Administrator\.openclaw\workspace\fateandmethod-fixed'
    fixed = skipped = 0
    for bn in ['bazi.html', 'daily-wisdom.html', 'daliuren.html', 'liuyao.html',
               'meihua.html', 'taiyi.html', 'xiaoliuren.html', 'xuankong.html', 'ziwei.html']:
        fpath = os.path.join(repodir, bn)
        ok = fix_file(fpath)
        if ok: fixed += 1
        else: skipped += 1
    print(f'Result: fixed={fixed}, skipped={skipped}')


if __name__ == '__main__':
    main()
