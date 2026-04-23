const fs = require('fs');
const c = fs.readFileSync('C:/Users/Administrator/github/novelpick-site/best-litrpg-novels.html', 'utf8');

// Check main.article-body content
const start = c.indexOf('<main class="article-body">');
if (start >= 0) {
  const end = c.indexOf('</main>', start);
  const content = c.substring(start + 23, end);
  console.log('main.article-body content length:', content.length);
  console.log('First 300 chars:', content.substring(0, 300));
} else {
  console.log('No main.article-body found');
}