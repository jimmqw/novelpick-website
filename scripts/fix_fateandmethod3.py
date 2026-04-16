#!/usr/bin/env python3
"""Fix fateandmethod article pages - simple string replacements."""
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

    # Check if fix needed
    se = c.find('</style>')
    he = c.find('</head>')
    if se == -1 or he == -1 or '<script' not in c[se:he]:
        print(f'  CLEAN: {os.path.basename(fpath)}')
        return False

    # Extract scripts from head
    scripts = re.findall(r'<script[^>]*>.*?</script>', c[se:he], re.DOTALL)

    # 1. Remove scripts from head
    c2 = c[:se+8]  # up to and including </style>
    for s in scripts:
        c2 += c[c2.find('</head>'):]  # append rest (from </head> onwards)
    # Actually: rebuild
    c2 = c[:se+8]
    tail = c[se+8:]  # everything after </style>
    for s in scripts:
        tail = tail.replace(s, '')
    c2 += tail

    # 2. Add progress CSS after </style>
    c2 = c2.replace('</style>', '</style>\n' + PROGRESS_CSS, 1)

    # 3. Add progress bar after <body>
    c2 = c2.replace('<body>\n', '<body>\n' + PROGRESS_BAR, 1)

    # 4. Add scripts before </body>
    c2 = c2.replace('</body>\n', PROGRESS_SCRIPT + '</body>\n', 1)
    # Handle case where there's no \n before </body>
    if c2.count('</body>') == 1 and '\n</body>' not in c2:
        c2 = c2.replace('</body>', PROGRESS_SCRIPT + '</body>', 1)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(c2)

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
