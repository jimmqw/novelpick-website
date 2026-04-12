import os

base = r"C:\Users\Administrator\github\novelpick-site"

baidu_code = """<!-- Baidu Analytics -->
<script>
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?7a310f3a5b54d3c8565e5669ffb815a5";
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(hm, s);
})();
</script>
"""

html_files = [f for f in os.listdir(base) if f.endswith('.html')]

added = 0
for fn in html_files:
    fp = os.path.join(base, fn)
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        continue

    if 'hm.baidu.com' in content:
        print(f"SKIP: {fn}")
        continue

    if '</head>' not in content:
        print(f"NO HEAD: {fn}")
        continue

    content = content.replace('</head>', baidu_code + '</head>')

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"ADDED: {fn}")
    added += 1

print(f"\nDone! Added to {added} files.")
