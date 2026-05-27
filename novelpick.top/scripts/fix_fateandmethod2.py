#!/usr/bin/env python3
"""Fix fateandmethod article pages - simpler approach."""
import re, glob, os

PROGRESS_BAR = '<div class="progress-bar"><div class="progress-fill" id="progressFill"></div>\n'
PROGRESS_SCRIPT = '''<script>
window.addEventListener("scroll", function() {
    var el = document.getElementById("progressFill");
    if (!el) return;
    var pct = document.documentElement.scrollHeight > window.innerHeight
        ? (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100 : 0;
    el.style.width = pct + "%";
});
</script>'''
PROGRESS_CSS = '''
        .progress-bar { position: fixed; top: 64px; left: 0; right: 0; height: 2px; z-index: 99; background: var(--gold-border); }
        .progress-fill { height: 100%; background: var(--gold); width: 0%; transition: width 0.1s linear; }
'''


def _rf(p):
    with open(p, 'rb') as f:
        raw = f.read()
    if raw.startswith(b'\xff\xfe') or raw.startswith(b'\xfe\xff'):
        return raw.decode('utf-16').encode('utf-8').decode('utf-8')
    for enc in ['utf-8-sig', 'utf-8', 'cp1252']:
        try: return raw.decode(enc)
        except: continue
    return raw.decode('utf-8', errors='replace')

def _norm(c):
    return c.replace('\r\n', '\n').replace('\r', '\n')


def fix_file(fpath):
    c = _norm(_rf(fpath))

    # Check if needs fixing
    se = c.find('</style>')
    he = c.find('</head>')
    bs = c.find('<body>', he)
    if se == -1 or he == -1 or bs == -1:
        print(f'  SKIP (malformed): {os.path.basename(fpath)}')
        return False
    if '<script' not in c[se:he]:
        print(f'  CLEAN: {os.path.basename(fpath)}')
        return False

    # 1. Extract head content: from <head> to </style> (inclusive)
    head_start = c.find('<head>')
    head_content = c[head_start:se + len('</style>')]
    # 2. Add progress CSS before </style>
    head_content = head_content.replace('</style>', PROGRESS_CSS + '\n    </style>')
    # 3. Extract scripts from between </style> and </head>
    scripts_in_head = re.findall(r'<script[^>]*>.*?</script>', c[se:he], re.DOTALL)
    # 4. Extract body content from after <body> to before </body>
    body_tag_end = c.find('>', bs) + 1
    body_end = c.rfind('</body>')
    if body_end == -1:
        print(f'  SKIP (no </body>): {os.path.basename(fpath)}')
        return False
    body_content = c[body_tag_end:body_end]
    # Remove any existing script tags from body content
    for s in re.findall(r'<script[^>]*>.*?</script>', body_content, re.DOTALL):
        body_content = body_content.replace(s, '')
    # Add scripts to end of body
    body_content = body_content.strip() + '\n' + '\n'.join(scripts_in_head)

    # 5. Reconstruct
    new_html = (
        head_content +
        '\n</head>\n' +
        '<body>\n' +
        PROGRESS_BAR +
        body_content +
        '\n' +
        PROGRESS_SCRIPT +
        '\n</body>\n</html>'
    )

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f'  FIXED: {os.path.basename(fpath)}')
    return True


def main():
    repodir = r'C:\Users\Administrator\.openclaw\workspace\fateandmethod-fixed'
    fixed = skipped = 0
    for fpath in sorted(glob.glob(repodir + r'\*.html')):
        bn = os.path.basename(fpath)
        if bn == 'index.html':
            print(f'  SKIP index.html')
            skipped += 1
            continue
        ok = fix_file(fpath)
        if ok: fixed += 1
        else: skipped += 1
    print(f'Result: fixed={fixed}, skipped={skipped}')


if __name__ == '__main__':
    main()
