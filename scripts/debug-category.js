const fs = require('fs');
const c = fs.readFileSync('C:/Users/Administrator/github/novelpick-site/fantasy.html', 'utf8');

// Find article-body content
const bodyMatch = c.match(/<div class="article-body"[^>]*>([\s\S]*?)<\/div>\s*<footer/);
if (bodyMatch) {
  console.log('Content preview (first 500 chars):');
  console.log(bodyMatch[1].substring(0, 500));
}