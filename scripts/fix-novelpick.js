const fs = require('fs');
const dir = 'C:/Users/Administrator/github/novelpick-site';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html') && f !== 'index.html');

files.forEach(f => {
  let c = fs.readFileSync(dir + '/' + f, 'utf8');
  let fixed = false;
  
  // 1. Remove duplicate meta tags (second og:title block after first </style>)
  const metaPattern = /<meta property="og:title" content="[^"]+"[\s\S]*?<\/style>/;
  if (c.match(metaPattern)) {
    c = c.replace(metaPattern, '</style>');
    fixed = true;
  }
  
  // 2. Fix garbled date (Chinese chars to English)
  c = c.replace(/&#128197;[\s\S]*?\d{4}/g, '📅 April 7, 2026');
  c = c.replace(/&#9200;[\s\S]*?min read/g, '⏱️ 8 min read');
  
  // 3. Remove duplicate style block (.article-layout)
  if (c.includes('.article-layout')) {
    const idx = c.indexOf('.article-layout');
    const styleStart = c.lastIndexOf('<style>', idx);
    const styleEnd = c.indexOf('</style>', styleStart) + 8;
    if (styleStart > 0 && styleEnd > 8) {
      c = c.substring(0, styleStart) + c.substring(styleEnd);
      fixed = true;
    }
  }
  
  if (fixed) {
    fs.writeFileSync(dir + '/' + f, c);
    console.log('Fixed:', f);
  }
});
console.log('Done - processed', files.length, 'files');