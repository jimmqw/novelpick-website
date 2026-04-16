#!/usr/bin/env python3
"""Fix fateandmethod article pages - clean reconstruction."""
import re, glob, os

PROGRESS_BAR = '<div class="progress-bar"><div class="progress-fill" id="progressFill"></div>\n'
PROGRESS_SCRIPT = '<script>\nwindow.addEventListener("scroll",function(){var e=document.getElementById("progressFill");if(!e)return;var pct=document.documentElement.scrollHeight>window.innerHeight?(window.scrollY/(document.documentElement.scrollHeight-window.innerHeight))*100:0;e.style.width=pct+"%";});\n</script>\n'
PROGRESS_CSS = '\n        .progress-bar{position:fixed;top:64px;left:0;right:0;height:2px;z-index:99;background:var(--gold-border)}.progress-fill{height:100%;background:var(--gold);width:0%;transition:width .1s linear}\n'


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
    bs = c.find('<body>', he)
    be = c.rfind('</body>')
    if -1 in [se, he, bs, be]:
        print(f'  SKIP: {os.path.basename(fpath)}')
        return False

    # Check for script between </style> and </head>
    script_segment = c[se+8:he]
    has_script = '<script>' in script_segment or '<script ' in script_segment
    if not has_script:
        print(f'  CLEAN: {os.path.basename(fpath)}')
        return False

    # Find the actual script block (may have JS-stringified closing tag)
    script_start_in_seg = script_segment.find('<script')
    if script_start_in_seg == -1:
        print(f'  ERROR: script start not found: {os.path.basename(fpath)}')
        return False

    # Find script end in segment
    ss_abs = se + 8 + script_start_in_seg  # absolute position of <script>
    # Try </script> first
    se_abs = c.find('</script>', ss_abs)
    if se_abs != -1 and se_abs < he:
        script_end_abs = se_abs + len('</script>')
        script = c[ss_abs:script_end_abs]
    else:
        # JS-stringified: look for /script>
        slash_abs = c.find('/script>', ss_abs)
        if slash_abs != -1 and slash_abs < he:
            script_end_abs = slash_abs + len('/script>')
            script = c[ss_abs:script_end_abs]
        else:
            print(f'  ERROR: script end not found: {os.path.basename(fpath)}')
            return False

    # part1: DOCTYPE/html/head up to and including </style>
    part1 = c[:se + 8]  # up to and including </style>
    # Remove script from the tail (between </style> and </head>)
    seg = c[se+8:he]
    seg = seg.replace(script, '', 1)
    part1 += seg
    # part1 += </head>\n<body> + progress bar
    part1 += c[he:bs+7] + '\n' + PROGRESS_BAR
    body_content = c[bs+7:be]
    # Remove any scripts from body
    for s in re.findall(r'<script[^>]*>.*?</script>', body_content, re.DOTALL):
        body_content = body_content.replace(s, '')
    # part1 += progress bar + body content
    part1 += PROGRESS_BAR + body_content.strip() + '\n'
    # part1 += progress script + original script + </body></html>
    part1 += PROGRESS_SCRIPT + script.replace('" + "/script>', '</script>') + '\n</body>\n</html>'

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(part1)

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
