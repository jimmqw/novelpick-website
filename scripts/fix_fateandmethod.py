#!/usr/bin/env python3
"""Fix fateandmethod article pages - move scripts from head to body, add progress bar."""
import re, glob, os

PROGRESS_BAR = '''<div class="progress-bar"><div class="progress-fill" id="progressFill"></div>
'''

PROGRESS_SCRIPT = '''<script>
        window.addEventListener('scroll', function() {
            var el = document.getElementById('progressFill');
            if (!el) return;
            var pct = document.documentElement.scrollHeight > window.innerHeight
                ? (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100 : 0;
            el.style.width = pct + '%';
        });
    </script>'''

PROGRESS_CSS = '''
        .progress-bar {
            position: fixed; top: 64px; left: 0; right: 0; height: 2px; z-index: 99;
            background: var(--gold-border);
        }
        .progress-fill {
            height: 100%; background: var(--gold); width: 0%; transition: width 0.1s linear;
        }'''

BAIDU_ID = '7a310f3a5b54d3c8565e5669ffb815a5'
BAIDU_SCRIPT = f'''<script>
var _hmt = _hmt || [];
(function() {{
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?{BAIDU_ID}";
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(hm, s);
}})();
</script>'''


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

def fix_fateandmethod(fpath):
    c = _norm(_rf(fpath))

    # Check if needs fixing
    se = c.find('</style>')
    he = c.find('</head>')
    if se == -1 or he == -1:
        print(f'  SKIP (no style/head): {os.path.basename(fpath)}')
        return False
    if '<script' not in c[se:he]:
        print(f'  CLEAN: {os.path.basename(fpath)}')
        return False

    # Extract scripts from head
    scripts = re.findall(r'<script[^>]*>.*?</script>', c[se:he], re.DOTALL)

    # Extract meta block (between <head> and <style>)
    hs = c.find('<head>')
    meta_block = c[hs + 6:se].strip()

    # Build new head
    head_close = c.find('>', he) + 1
    body_content = c[head_close:]
    # Remove scripts from body_content (they were added to head)
    body_scripts = re.findall(r'<script[^>]*>.*?</script>', body_content, re.DOTALL)
    for s in body_scripts:
        body_content = body_content.replace(s, '\n__SP__\n', 1)

    # Add progress bar CSS to the CSS block
    css_end = se + len('</style>')
    new_css = c[:css_end] + PROGRESS_CSS + '\n' + c[css_end:]

    # Build new head: everything up to </style> (with progress CSS added), then </head>
    new_head_end = new_css.find('</style>') + len('</style>')
    new_head = new_css[:new_head_end] + '\n' + new_css[new_head_end:]

    # The body starts after </head>
    # Find </head> in new_head
    new_he_pos = new_head.find('</head>')
    body_start_marker = new_head[new_he_pos + len('</head>'):new_he_pos + len('</head>') + 50]
    # Find where body content starts
    body_section = body_content

    # Reconstruct
    new_html = new_head + body_section

    # Add progress bar after <body>
    new_html = new_html.replace('<body>\n', '<body>\n' + PROGRESS_BAR, 1)
    # Add progress script before </body>
    new_html = new_html.replace('</body>\n', '\n' + PROGRESS_SCRIPT + '\n</body>\n', 1)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f'  FIXED: {os.path.basename(fpath)}')
    return True


def main():
    repodir = r'C:\Users\Administrator\.openclaw\workspace\fateandmethod-fixed'
    fixed = skipped = 0

    for fpath in glob.glob(repodir + r'\*.html'):
        bn = os.path.basename(fpath)
        if bn == 'index.html':
            print(f'  SKIP index.html')
            skipped += 1
            continue
        ok = fix_fateandmethod(fpath)
        if ok: fixed += 1
        else: skipped += 1

    print(f'Result: fixed={fixed}, skipped={skipped}')


if __name__ == '__main__':
    main()
