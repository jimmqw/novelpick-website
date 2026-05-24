const fs = require('fs');
const path = 'C:/Users/Administrator/.openclaw/workspace/morai.top/best-ai-video-generation-tools-2026.html';
const ending = `<a href="#" class="back-to-top" onclick="window.scrollTo({top:0,behavior:'smooth'});return false;">Back to top</a>
</div>
</div>
</main>

<aside class="sidebar">
<div class="widget">
<h4>Categories</h4>
<div class="widget-nav">
<a href="/ai-tools.html">AI Tools</a>
<a href="/ai-reviews.html">Reviews</a>
<a href="/ai-comparisons.html">Comparisons</a>
<a href="/ai-guides.html">Guides</a>
<a href="/deals.html">Deals</a>
</div>
</div>
<div class="widget">
<h4>Popular Articles</h4>
<ul class="widget-links">
<li><a href="/best-ai-agents-2026.html">Best AI Agents 2026</a></li>
<li><a href="/best-ai-image-generators-2026-comparison.html">Best AI Image Generators 2026</a></li>
<li><a href="/claude-3-7-sonnet-review.html">Claude 3.7 Sonnet Review</a></li>
<li><a href="/best-ai-coding-tools-2026.html">Best AI Coding Tools 2026</a></li>
<li><a href="/chatgpt-vs-claude.html">ChatGPT vs Claude 3.7</a></li>
</ul>
</div>
<div class="widget">
<h4>Latest</h4>
<ul class="widget-links">
<li><a href="/best-ai-video-generation-tools-2026.html">Best AI Video Generation Tools 2026</a></li>
<li><a href="/best-ai-agents-2026.html">Best AI Agents 2026</a></li>
<li><a href="/best-ai-image-generators-2026-comparison.html">Best AI Image Generators 2026</a></li>
</ul>
</div>
</aside>
</div>

<footer class="footer">
<a href="/">Home</a>
<a href="/ai-tools.html">AI Tools</a>
<a href="/ai-reviews.html">Reviews</a>
<a href="/ai-comparisons.html">Comparisons</a>
<a href="/ai-guides.html">Guides</a>
<a href="/deals.html">Deals</a>
<br><br>
&copy; 2026 Morai.top — AI Tools Reviewed. All rights reserved.
</footer>
</body>
</html>
`;
fs.appendFileSync(path, ending);
const final = fs.readFileSync(path, 'utf8');
console.log('Total length:', final.length);
// Verify it ends properly
console.log('Last 300 chars:', final.slice(-300));
