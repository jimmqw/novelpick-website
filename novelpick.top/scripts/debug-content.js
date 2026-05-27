const fs = require('fs');
const c = fs.readFileSync('C:/Users/Administrator/github/novelpick-site/best-litrpg-novels.html', 'utf8');

// Try to find article content
const patterns = [
  /<div class="article-body"[^>]*>([\s\S]*?)<\/div>\s*<(?:div|main|aside|footer)/,
  /<article-body[^>]*>([\s\S]*?)<\/article-body>/,
  /<main[^>]*>([\s\S]*?)<\/main>/
];

patterns.forEach((p, i) => {
  const m = c.match(p);
  if (m) {
    console.log('Pattern', i+1, 'matched, length:', m[1].length);
    console.log('First 200 chars:', m[1].substring(0, 200));
  } else {
    console.log('Pattern', i+1, 'no match');
  }
});

// Also check what's in the file
console.log('\nFile stats:');
console.log('Has article-body class:', c.includes('class="article-body"'));
console.log('Has article-body tag:', c.includes('<article-body'));
console.log('Total length:', c.length);