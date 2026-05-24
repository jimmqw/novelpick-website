## Article Check & Fix Lessons (2026-04-29)

### Batch: 10 articles across 3 sites

### Issues Found & Fixed

**1. Missing Keep Reading sections (9/10 articles)**
- Root cause: articles had no related post recommendation module
- Fix strategy: inject `<div class="keep-reading-section">` with 4-6 related article links before the prev-next section
- **Lesson for check scripts:** Check for Keep Reading div in the BODY (after `</style>`), not in the whole file. CSS injection of `.keep-reading-section {...}` causes false positives.

**2. Div nesting imbalance (3/10 articles)**
- Files affected: best-ai-agents-2026.html, top-litrpg-web-novels-2026.html
- Pattern: extra `</div>` between article-body content close and prev-next section
- Fix: remove the orphan `</div>` tag
- **Lesson for check scripts:** Track `<div>` open/close balance from the article-body element's opening tag to its matching closing tag (not to EOF). The batch_article_check.py has a bug here.

**3. No article-body class (1/10)**
- File: chinese-zodiac-compatibility-guide.html
- This file uses unquoted HTML attributes (`class=article-body` instead of `class="article-body"`)
- Fix: already has the class, just in unquoted form; check scripts need to handle both formats

**4. Keep Reading CSS added but HTML body skipped (4/10)**
- Files: bazi-ten-gods-guide.html, feng-shui-2026-year-guide.html (inserted before `</main>`), 3 novelpick files (inserted before `<nav class="prev-next">` or `<div class="prev-next">`)
- Root cause: fix_articles.py checks `"keep-reading-section" in content` which finds it in CSS even when absent from HTML body
- Fix: CSS-only files got KR div manually injected

**5. BLUF violations fixed (5/10)**
- Converted h2 question headings ("What Is X?") to declarative statements ("Why X Matters" / "Understanding X")

**6. Batch check script false positives**
- Script reports DIV_NESTING issues for morai.top articles but actual balance is 0
- Script reports article-body class missing for files using unquoted attributes
- Root cause: checker doesn't handle unquoted attrs and tracks divs to EOF instead of to matching close tag

### Prevention Patterns
1. When adding Keep Reading, check BODY only (post-`</style>`)
2. `<nav class="prev-next">` is valid HTML5; don't assume `<div class="prev-next">`
3. CSS injection ≠ HTML body injection - verify both
4. Unquoted HTML attributes (`class=article-body`) are valid HTML5 and should be handled
