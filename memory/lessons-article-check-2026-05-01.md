# Lessons Learned - 旧文章检查优化 (2026-05-01)

## 修复记录

### 本轮处理文章（11篇）
- morai: chatgpt-vs-claude-vs-gemini-2026.html, claude-3-7-sonnet-review.html, best-ai-tools-2026.html, ai-agent-tools-2026.html
- novelpick: best-chinese-wuxia-web-novels-2026.html, books-like-solo-leveling.html, top-romance-web-novels-2026.html
- fateandmethod: feng-shui-2026-year-guide.html, bazi-beginners-complete-guide.html, chinese-zodiac-2026-fire-snake-horoscope.html, five-elements-complete-guide.html

### 修复内容
1. **Div嵌套修复** — `chinese-zodiac-2026-fire-snake-horoscope.html`
   - 羊年生肖区`<div class="dos-donts">`内有一行被截断：`<div><h4>Dodos-donts">`（缺少class属性，名为"dos-donts"的div被破坏成了无class的单独div）
   - 这导致整个文件div不平衡：212 opens vs 211 closes (+1)
   - 修复方法：删除被破坏的行即可恢复平衡
   - **教训：** 检查div平衡时用`count('<div ') + count('<div>') - count('</div>')`，不要用正则`<div[^>]*>`，后者在有`>`字符在属性值内时会误计数

2. **乱码字符修复** — `claude-3-7-sonnet-review.html`
   - `釥` (U+9225) 出现8次，应为em-dash `—` (U+2014)
   - 均为"更新 — 它..."等结构中的连接符
   - 统一替换为 `—` (U+2014)

3. **添加发布日期** — 以下文件
   - `books-like-solo-leveling.html` → March 15, 2026
   - `bazi-beginners-complete-guide.html` → January 10, 2026
   - `feng-shui-2026-year-guide.html` → January 10, 2026
   - `five-elements-complete-guide.html` → January 10, 2026

4. **添加相关文章推荐** — 以下文件添加了Keep Reading/Recommended区块
   - morai: claude-3-7-sonnet-review, best-ai-tools-2026, ai-agent-tools-2026
   - novelpick: books-like-solo-leveling, best-chinese-wuxia-web-novels, top-romance-web-novels
   - fateandmethod: bazi-beginners-complete-guide, chinese-zodiac, five-elements-complete-guide

### 已知问题（已识别但未完全修复）
1. **NO_ARTICLE_BODY** — 4个文件缺少`article-body`div包装，需要模板级结构调整：
   - morai: chatgpt-vs-claude-vs-gemini-2026
   - novelpick: books-like-solo-leveling
   - fateandmethod: feng-shui-2026, chinese-zodiac, five-elements-complete-guide
2. **OUTDATED** — 4篇fateandmethod文章90-111天，接近3个月过时阈值
3. **checker脚本改进：** 日期检测增加了`Month DD, YYYY`格式支持；h2内容检测移除了h3作为段落边界的逻辑（h3是h2的子段落）

### 教训（防止再犯）
1. **div平衡检测用`str.count`不要用正则`<div[^>]*>`** — 后者在有`>`字符在属性值内时误匹配
2. **乱码字符修复要逐条检查上下文** — 8个`釥`全部是em-dash，但其他文件可能有不同的替换模式
3. **添加相关文章时避免循环引用** — 同一站点的文章互链要形成有效导航，不要A→B→A
4. **中文日期格式要纳入日期检查** — 不能用仅ISO格式匹配

---

## 修复记录 (2026-05-22)

### 本轮处理文章（30篇）
- morai 10篇, novelpick 10篇, fateandmethod 10篇

### 修复内容
1. **`</main>` 标签损坏** — 多个morai文章
   - `chatgpt-vs-claude.html`: `</main\n<aside` 缺少 `>`
   - `best-ai-meeting-tools-2026.html`: `</main\r\n\r\n<aside` 缺少 `>`
   - `best-ai-note-taking-tools-2026.html`: 完全缺少 `</main>`（`<main>`开了没关）
   - 修复：直接用bytes替换 `b'</main\r\n'` → `b'</main>\r\n'`

2. **novelpick Keep Reading缺失** — `best-cultivation-novels-2026.html`
   - 添加了4个相关链接（reincarnation/progression/historical/harem）

3. **中文日期修复** — morai多个文章
   - 四月 7, 2026 乱码，用bytes替换 `b'\xe9\x8d\xa5\xe6\xb6\x99 7, 2026'` → `b'April 7, 2026'`

### 已知问题（未修复）
1. **morai div=+1（5个文件）** — 不是`</main>`问题，是页面头部CSS区或sidebar区的结构性div不平衡
2. **fateandmethod div嵌套** — feng-shui-fundamentals(+2), chinese-zodiac-personality-traits(-12), daily-wisdom(-5)
3. **novelpick空Keep Reading块** — best-progression-fantasy等有块但无链接

### checker教训
1. **KR检测范围要扩大** — 检查 class 中含 "related" 的所有元素，不只是 "related-articles"
2. **PowerShell处理UTF-8输出会触发GBK编码错误** — 涉及中文字符时避免在命令行echo，用文件代替
3. **git reset --hard会丢失未提交修改** — 修复前先确认文件状态
4. **rebase conflict in sitemap** — 两个人同时更新sitemap导致冲突，下次sitemap更新单独处理
