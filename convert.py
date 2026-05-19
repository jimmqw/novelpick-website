import os
os.chdir(r'C:\Users\Administrator\.openclaw\workspace\novelpick-website')

# Read the English file
with open('best-cultivation-novels-2026.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Make replacements
c = c.replace('<html lang="en">', '<html lang="zh-CN">')

old_t = '<title>Best Xianxia &amp; Cultivation Web Novels 2026 — Top Martial Arts Fantasy Reads | NovelPick</title>'
new_t = '<title>Best Xianxia Novels 2026 | NovelPick</title>'
c = c.replace(old_t, new_t)

old_d = '<meta name="description" content="The 10 best xianxia and cultivation web novels every fan needs to read in 2026. From classics like Coiling Dragon to hidden gems — handpicked and ranked.">'
new_d = '<meta name="description" content="Best Chinese xianxia and cultivation web novels of 2026:仙逆,凡人修仙传,一念永恒,大奉打更人, etc. Expert picks ranked by quality.">'
c = c.replace(old_d, new_d)

old_ogt = '<meta property="og:title" content="Best Xianxia &amp; Cultivation Web Novels 2026 — Top Martial Arts Fantasy Reads | NovelPick">'
new_ogt = '<meta property="og:title" content="Best Xianxia Novels 2026 | NovelPick">'
c = c.replace(old_ogt, new_ogt)

old_ogd = '<meta property="og:description" content="The 10 best xianxia and cultivation web novels every fan needs to read in 2026. From classics like Coiling Dragon to hidden gems — handpicked and ranked.">'
new_ogd = '<meta property="og:description" content="Best Chinese xianxia and cultivation web novels of 2026. Expert picks including Er Gen, I Eat Tomatoes and other top authors.">'
c = c.replace(old_ogd, new_ogd)

old_ogurl = '<meta property="og:url" content="https://novelpick.top/best-cultivation-novels-2026.html">'
new_ogurl = '<meta property="og:url" content="https://novelpick.top/best-xianxia-novels-2026.html">'
c = c.replace(old_ogurl, new_ogurl)

old_can = '<link rel="canonical" href="https://novelpick.top/best-cultivation-novels-2026.html">'
new_can = '<link rel="canonical" href="https://novelpick.top/best-xianxia-novels-2026.html">'
c = c.replace(old_can, new_can)

old_site = '<meta property="og:site_name" content="NovelPick">'
new_site = '<meta property="og:site_name" content="NovelPick">\n<meta name="twitter:title" content="Best Xianxia Novels 2026 | NovelPick">\n<meta name="twitter:description" content="Best Chinese xianxia and cultivation web novels of 2026. Expert picks ranked by quality.">'
c = c.replace(old_site, new_site)

old_nav = '''<li><a href="/">Home</a></li>
      <li><a href="/best-cultivation-novels-2026.html">Fantasy</a></li>
      <li><a href="/best-cultivation-novels-2026.html">LitRPG</a></li>
      <li><a href="/best-reincarnation-web-novels-2026.html">Sci-Fi</a></li>
      <li><a href="/top-romance-web-novels-2026.html">Romance</a></li>
      <li><a href="/top-romance-web-novels-2026.html">Reviews</a></li>'''
new_nav = '''<li><a href="/">Home</a></li>
      <li><a href="/best-xianxia-novels-2026.html">Xianxia</a></li>
      <li><a href="/best-reincarnation-web-novels-2026.html">Reincarnation</a></li>
      <li><a href="/best-time-travel-web-novels-2026.html">Time Travel</a></li>
      <li><a href="/top-romance-web-novels-2026.html">Romance</a></li>'''
c = c.replace(old_nav, new_nav)

old_bc = '<div class="breadcrumb"><a href="/">Home</a><span>›</span><a href="/best-cultivation-novels-2026.html">Fantasy</a><span>›</span>Best Xianxia &amp; Cultivation Web Novels 2026</div>'
new_bc = '<div class="breadcrumb"><a href="/">Home</a><span>›</span><a href="/best-xianxia-novels-2026.html">Xianxia</a><span>›</span>Best Xianxia Novels 2026</div>'
c = c.replace(old_bc, new_bc)

old_eyebrow = '  <div class="eyebrow">📈</div>'
new_eyebrow = '  <div class="eyebrow">⚔️</div>'
c = c.replace(old_eyebrow, new_eyebrow)

old_h1 = '  <h1>Best Xianxia &amp; Cultivation Web Novels 2026</h1>'
new_h1 = '  <h1>Best Xianxia Novels 2026 — Top 10 Cultivation Fantasy</h1>'
c = c.replace(old_h1, new_h1)

old_sub = '  <p class="subtitle">The mortal climbs. The heavens watch. Ten novels where the path to immortality is paved with suffering, willpower, and limitless ambition.</p>'
new_sub = '  <p class="subtitle">The path to immortality is paved with suffering. 10 best Chinese xianxia novels ranked and reviewed.</p>'
c = c.replace(old_sub, new_sub)

old_meta = '  <div class="meta"><span>📅 April 2026</span><span>⏱ 10 min read</span><span>✍ NovelPick Editorial</span></div>'
new_meta = '  <div class="meta"><span>📅 May 2026</span><span>⏱ 12 min read</span><span>✍ NovelPick Editorial</span></div>'
c = c.replace(old_meta, new_meta)

old_intro = '<p>📈 Xianxia — the genre where immortals are born from suffering, and the heavens are not to be trusted. Cultivation web novels take ancient Chinese philosophical concepts of qi, meridians, and spiritual breakthroughs and turn them into some of the most compulsive progression fiction ever written. The appeal is primal: a weak nobody decides they will become a god, and then they do, one realm at a time. Whether it is the relentless determination of a poor orphan who refuses to kneel to fate, or the cold-blooded scheming of a demon who would sacrifice the world for one more step upward, cultivation fiction delivers on the fantasy of transcending every limitation. Here are the 10 best xianxia and cultivation web novels you should be reading in 2026.</p>'
new_intro = '<p>Xianxia — the genre where immortals are born from suffering, and the heavens are not to be trusted. Cultivation web novels take ancient Chinese philosophical concepts of qi, meridians, and spiritual breakthroughs and turn them into some of the most compulsive progression fiction ever written. The appeal is primal: a weak nobody decides they will become a god, and then they do, one realm at a time. Here are the 10 best xianxia and cultivation web novels you should be reading in 2026.</p>'
c = c.replace(old_intro, new_intro)

# Add comparison table before the final verdict section
old_h2_end = '<h2>The Cultivation Universe: Why These Novels Keep Getting Better</h2>'
new_h2_end = '<h2>📊 Quick Comparison Table</h2>\n\n<table class="comp-table">\n<thead><tr><th>#</th><th>Title</th><th>Author</th><th>Status</th><th>Chapters</th><th>Tags</th></tr></thead>\n<tbody>\n<tr><td>#1</td><td>A Record of a Mortal\'s Journey to Immortality</td><td>Er Gen</td><td>Complete</td><td>~1900</td><td>Realistic, Long-term Progression</td></tr>\n<tr><td>#2</td><td>I Shall Seal the Heavens</td><td>Er Gen</td><td>Complete</td><td>~1600</td><td>Epic Scope, Comedy, Romance</td></tr>\n<tr><td>#3</td><td>Renegade Immortal</td><td>Er Gen</td><td>Complete</td><td>~1400</td><td>Dark, Antihero, Philosophical</td></tr>\n<tr><td>#4</td><td>Coiling Dragon</td><td>I Eat Tomatoes</td><td>Complete</td><td>~1200</td><td>Epic Fantasy, Bloodline</td></tr>\n<tr><td>#5</td><td>Battle Through the Heavens</td><td>Tianyi Silkworm Potato</td><td>Complete</td><td>~1600</td><td>Fallen Genius, Alchemy, Romance</td></tr>\n<tr><td>#6</td><td>Desolate Era</td><td>I Eat Tomatoes</td><td>Complete</td><td>~1100</td><td>Epic, Sword Cultivation, Fated</td></tr>\n<tr><td>#7</td><td>I Shall Suppress the Heavens</td><td>Er Gen</td><td>Ongoing</td><td>~1800</td><td>Antihero, Cosmic Injustice</td></tr>\n<tr><td>#8</td><td>World Defying God</td><td>Ao Wu Chang</td><td>Ongoing</td><td>~1200</td><td>Empire Building, Strategy</td></tr>\n<tr><td>#9</td><td>Prime Ingress</td><td>Yuan Kong</td><td>Ongoing</td><td>~800</td><td>Progression, Pagoda System</td></tr>\n<tr><td>#10</td><td>A Record of the Journey to the West</td><td>MJGenius</td><td>Complete</td><td>~600</td><td>Mythology, Adventure</td></tr>\n</tbody>\n</table>\n\n<h2>The Cultivation Universe: Why These Novels Keep Getting Better</h2>'
c = c.replace(old_h2_end, new_h2_end)

# Write to new file
with open('best-xianxia-novels-2026.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('done', len(c))