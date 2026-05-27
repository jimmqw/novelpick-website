const fs = require('fs');
const c = fs.readFileSync('C:/Users/Administrator/github/novelpick-site/fantasy.html', 'utf8');

// Find main content between <main class="page-wrap"> and </main>
const start = c.indexOf('<main class="page-wrap">');
const end = c.indexOf('</main>');

console.log('start:', start, 'end:', end);

if (start >= 0 && end > start) {
  const main = c.substring(start + 20, end);
  console.log('main content length:', main.length);
  console.log('First 300 chars:', main.substring(0, 300));
} else {
  console.log('Cannot find main content');
}