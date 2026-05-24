const fs = require('fs');
const c = fs.readFileSync('C:/Users/Administrator/github/novelpick-site/fantasy.html', 'utf8');

console.log('Has article-body class:', c.includes('class="article-body"'));
console.log('Total length:', c.length);

// Check for question marks specifically
const hasQuestionMarks = c.includes('??');
console.log('Has ?? chars:', hasQuestionMarks);

if (hasQuestionMarks) {
  // Find where
  const idx = c.indexOf('??');
  console.log('Context around ??:', c.substring(idx - 20, idx + 20));
}