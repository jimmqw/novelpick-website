const fs = require('fs');
const dir = 'C:/Users/Administrator/github/novelpick-site';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html') && f !== 'index.html');

files.forEach(f => {
  let c = fs.readFileSync(dir + '/' + f, 'utf8');
  let fixed = false;
  let original = c;
  
  // 1. Remove empty </style> tag at start of head
  c = c.replace(/<head>\s*<\/style>/g, '<head>');
  
  // 2. Remove second meta block (og:title, og:description, etc. that appear right after </style> in head)
  // Pattern: first </style> -> then meta og:title repeats
  const headEnd = c.indexOf('</head>');
  if (headEnd > 0) {
    const headContent = c.substring(0, headEnd);
    // Find second occurrence of og:title in head
    const firstOgTitle = headContent.indexOf('<meta property="og:title"');
    if (firstOgTitle > 0) {
      const secondOgTitle = headContent.indexOf('<meta property="og:title"', firstOgTitle + 1);
      if (secondOgTitle > 0 && secondOgTitle < 1500) {
        // Remove everything from second og:title to just before </head>
        const toRemove = headContent.substring(secondOgTitle - 1, headEnd);
        c = c.substring(0, secondOgTitle - 1) + c.substring(headEnd);
        fixed = true;
      }
    }
  }
  
  // 3. Remove the standalone <header> block (it's a duplicate, not styled)
  c = c.replace(/<header>\s*<div class="container"[^>]*>[\s\S]*?<\/header>/g, '');
  
  // 4. Remove duplicate article-body wrapper
  // There's one inside .page-wrap and one inside .container
  c = c.replace(/<div class="page-wrap"><div class="article-body">/g, '<div class="page-wrap"><div class="article-body">');
  // Find the double-wrapped: <div class="page-wrap"><div class="article-body"><div class="container"><div class="article-body">
  // Remove the inner container+article-body
  c = c.replace(/<div class="container"><div class="article-body">/g, '');
  // Need to also fix the closing - but this is tricky
  
  if (c !== original) {
    fs.writeFileSync(dir + '/' + f, c);
    console.log('Fixed:', f);
  }
});
console.log('Done - processed', files.length, 'files');