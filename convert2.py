import os
os.chdir(r'C:\Users\Administrator\.openclaw\workspace\novelpick-website')

with open('best-cultivation-novels-2026.html', 'rb') as f:
    src = f.read()

# Title: em dash in bytes is \xe2\x80\x94
old_title = b'<title>Best Xianxia & Cultivation Web Novels 2026 \xe2\x80\x94 Top Martial Arts Fantasy Reads | NovelPick</title>'
new_title = b'<title>Best Xianxia Novels 2026 \xe2\x80\x94 Top 10 Cultivation Fantasy Reads | NovelPick</title>'
data = src.replace(old_title, new_title, 1)

# OG title
old_og = b'<meta property="og:title" content="Best Xianxia & Cultivation Web Novels 2026 \xe2\x80\x94 Top Martial Arts Fantasy Reads | NovelPick">'
new_og = b'<meta property="og:title" content="Best Xianxia Novels 2026 \xe2\x80\x94 Top 10 Cultivation Fantasy Reads | NovelPick">'
data = data.replace(old_og, new_og, 1)

# OG description
old_ogd = b'<meta property="og:description" content="The 10 best xianxia and cultivation web novels every fan needs to read in 2026. From classics like Coiling Dragon to hidden gems \xe2\x80\x94 handpicked and ranked.">'
new_ogd = b'<meta property="og:description" content="Best Chinese xianxia and cultivation web novels of 2026 ranked by quality. Er Gen, I Eat Tomatoes and other top authors.">'
data = data.replace(old_ogd, new_ogd, 1)

# OG URL
data = data.replace(b'<meta property="og:url" content="https://novelpick.top/best-cultivation-novels-2026.html">',
    b'<meta property="og:url" content="https://novelpick.top/best-xianxia-novels-2026.html">', 1)

# Canonical
data = data.replace(b'<link rel="canonical" href="https://novelpick.top/best-cultivation-novels-2026.html">',
    b'<link rel="canonical" href="https://novelpick.top/best-xianxia-novels-2026.html">', 1)

# Twitter meta (add after og:site_name)
data = data.replace(b'<meta property="og:site_name" content="NovelPick">',
    b'<meta property="og:site_name" content="NovelPick">\n<meta name="twitter:title" content="Best Xianxia Novels 2026 \xe2\x80\x94 Top 10 Cultivation Fantasy Reads | NovelPick">\n<meta name="twitter:description" content="Best Chinese xianxia and cultivation web novels of 2026 ranked by quality. Er Gen, I Eat Tomatoes and other top authors.">', 1)

# Nav
data = data.replace(b'''<li><a href="/">Home</a></li>
      <li><a href="/best-cultivation-novels-2026.html">Fantasy</a></li>
      <li><a href="/best-cultivation-novels-2026.html">LitRPG</a></li>
      <li><a href="/best-reincarnation-web-novels-2026.html">Sci-Fi</a></li>
      <li><a href="/top-romance-web-novels-2026.html">Romance</a></li>
      <li><a href="/top-romance-web-novels-2026.html">Reviews</a></li>''',
b'''<li><a href="/">Home</a></li>
      <li><a href="/best-xianxia-novels-2026.html">Xianxia</a></li>
      <li><a href="/best-reincarnation-web-novels-2026.html">Reincarnation</a></li>
      <li><a href="/best-time-travel-web-novels-2026.html">Time Travel</a></li>
      <li><a href="/top-romance-web-novels-2026.html">Romance</a></li>''', 1)

# Breadcrumb
data = data.replace(b'<div class="breadcrumb"><a href="/">Home</a><span>\xe2\x80\xb9</span><a href="/best-cultivation-novels-2026.html">Fantasy</a><span>\xe2\x80\xb9</span>Best Xianxia &amp; Cultivation Web Novels 2026</div>',
b'<div class="breadcrumb"><a href="/">Home</a><span>\xe2\x80\xb9</span><a href="/best-xianxia-novels-2026.html">Xianxia</a><span>\xe2\x80\xb9</span>Best Xianxia Novels 2026</div>', 1)

# Eyebrow emoji
data = data.replace(b'  <div class="eyebrow">\xf0\x9f\x93\x88</div>', b'  <div class="eyebrow">\xe2\x9a\x94\xef\xb8\x8f</div>', 1)

# H1
data = data.replace(b'  <h1>Best Xianxia &amp; Cultivation Web Novels 2026</h1>',
b'  <h1>Best Xianxia Novels 2026 \xe2\x80\x94 Top 10 Cultivation Fantasy</h1>', 1)

# Subtitle
data = data.replace(b'  <p class="subtitle">The mortal climbs. The heavens watch. Ten novels where the path to immortality is paved with suffering, willpower, and limitless ambition.</p>',
b'  <p class="subtitle">The path to immortality is paved with suffering. 10 best Chinese xianxia novels ranked and reviewed.</p>', 1)

# Meta
data = data.replace(b'  <div class="meta"><span>\xf0\x9f\x93\x85 April 2026</span><span>\xe2\x98\x8b 10 min read</span><span>\xe2\x9c\x8d NovelPick Editorial</span></div>',
b'  <div class="meta"><span>\xf0\x9f\x93\x85 May 2026</span><span>\xe2\x98\x8b 12 min read</span><span>\xe2\x9c\x8d NovelPick Editorial</span></div>', 1)

# Update the intro box paragraph - keep emoji but update text
data = data.replace(b'<p>\xf0\x9f\x93\x88 Xianxia',
b'<p>Xianxia', 1)

# Add comparison table before "The Cultivation Universe" h2
# Find the h2 and insert table before it
old_h2 = b'<h2>The Cultivation Universe: Why These Novels Keep Getting Better</h2>'
new_h2 = b'''<h2>\xf0\x9f\x93\x8a Quick Comparison Table</h2>

<table class="comp-table">
<thead><tr><th>#</th><th>Title</th><th>Author</th><th>Status</th><th>Chapters</th><th>Tags</th></tr></thead>
<tbody>
<tr><td>#1</td><td>A Record of a Mortal\'s Journey to Immortality</td><td>Er Gen</td><td>Complete</td><td>~1900</td><td>Realistic, Long-term Progression</td></tr>
<tr><td>#2</td><td>I Shall Seal the Heavens</td><td>Er Gen</td><td>Complete</td><td>~1600</td><td>Epic Scope, Comedy, Romance</td></tr>
<tr><td>#3</td><td>Renegade Immortal</td><td>Er Gen</td><td>Complete</td><td>~1400</td><td>Dark, Antihero, Philosophical</td></tr>
<tr><td>#4</td><td>Coiling Dragon</td><td>I Eat Tomatoes</td><td>Complete</td><td>~1200</td><td>Epic Fantasy, Bloodline</td></tr>
<tr><td>#5</td><td>Battle Through the Heavens</td><td>Tianyi Silkworm Potato</td><td>Complete</td><td>~1600</td><td>Fallen Genius, Alchemy, Romance</td></tr>
<tr><td>#6</td><td>Desolate Era</td><td>I Eat Tomatoes</td><td>Complete</td><td>~1100</td><td>Epic, Sword Cultivation, Fated</td></tr>
<tr><td>#7</td><td>I Shall Suppress the Heavens</td><td>Er Gen</td><td>Ongoing</td><td>~1800</td><td>Antihero, Cosmic Injustice</td></tr>
<tr><td>#8</td><td>World Defying God</td><td>Ao Wu Chang</td><td>Ongoing</td><td>~1200</td><td>Empire Building, Strategy</td></tr>
<tr><td>#9</td><td>Prime Ingress</td><td>Yuan Kong</td><td>Ongoing</td><td>~800</td><td>Progression, Pagoda System</td></tr>
<tr><td>#10</td><td>A Record of the Journey to the West</td><td>MJGenius</td><td>Complete</td><td>~600</td><td>Mythology, Adventure</td></tr>
</tbody>
</table>

<h2>The Cultivation Universe: Why These Novels Keep Getting Better</h2>'''

data = data.replace(old_h2, new_h2, 1)

with open('best-xianxia-novels-2026.html', 'wb') as f:
    f.write(data)

print('done, size:', len(data))