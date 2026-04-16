const fs = require('fs');
const dir = 'C:/Users/Administrator/github/novelpick-site';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html') && f !== 'index.html');

files.forEach(f => {
  let c = fs.readFileSync(dir + '/' + f, 'utf8');
  let fixed = false;
  
  // 1. Remove empty style tags left by previous fix
  c = c.replace(/<style>\s*<\/style>/g, '');
  
  // 2. Remove the second meta block more aggressively
  // Find the position of </style> and look for duplicate meta after
  const firstStyleEnd = c.indexOf('</style>');
  if (firstStyleEnd > 0) {
    const afterFirstStyle = c.substring(firstStyleEnd + 8);
    // Check if there's a second <meta property="og:title" within 500 chars
    const secondMetaMatch = afterFirstStyle.substring(0, 800).match(/<meta property="og:title"/);
    if (secondMetaMatch) {
      // Find where this second meta block starts and where the next </style> is
      const secondMetaStart = afterFirstStyle.indexOf('<meta property="og:title"');
      const nextStyleStart = afterFirstStyle.indexOf('<style>', secondMetaStart);
      if (nextStyleStart > secondMetaStart) {
        const toRemove = afterFirstStyle.substring(secondMetaStart, nextStyleStart + 8);
        c = c.substring(0, firstStyleEnd + 8) + afterFirstStyle.substring(nextStyleStart + 8);
        fixed = true;
      }
    }
  }
  
  // 3. Fix garbled date - find the pattern and replace
  c = c.replace(/&#128197;\s*<span[^>]*>[\s\S]*?<\/span>/g, '📅 <span>April 7, 2026</span>');
  c = c.replace(/&#9200;\s*<span[^>]*>[\s\S]*?<\/span>/g, '⏱️ <span>8 min read</span>');
  
  if (fixed || c.includes('</style></style>') || c.includes('&#128197;')) {
    fs.writeFileSync(dir + '/' + f, c);
    console.log('Fixed:', f);
  }
});
console.log('Done - processed', files.length, 'files');