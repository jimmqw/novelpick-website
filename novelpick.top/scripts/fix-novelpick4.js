const fs = require('fs');
const dir = 'C:/Users/Administrator/github/novelpick-site';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html') && f !== 'index.html');

files.forEach(f => {
  let c = fs.readFileSync(dir + '/' + f, 'utf8');
  let fixed = false;
  let original = c;
  
  // 1. Fix the empty </style> - this is left over from a broken template
  // The structure is: <head>\n    </style>\n    <meta property="og:title"...
  // Should be: <head>\n    <meta property="og:title"...
  c = c.replace(/<head>\s*<\/style>\s*/g, '<head>\n    ');
  
  // 2. Remove the duplicate meta block in head (og:title, og:description, og:type, og:url, og:site_name, twitter:card, twitter:title, twitter:description)
  // These appear after first </style> but are duplicates
  const headSection = c.substring(0, c.indexOf('</head>'));
  // Count how many times og:title appears in head
  const ogTitleMatches = headSection.match(/<meta property="og:title"/g) || [];
  if (ogTitleMatches.length > 1) {
    // Find the first </style> or end of style block, then find second og:title
    const styleEnd = headSection.indexOf('</style>');
    if (styleEnd > 0) {
      const afterFirstStyle = headSection.substring(styleEnd + 8);
      const secondOgTitle = afterFirstStyle.indexOf('<meta property="og:title"');
      if (secondOgTitle > 0 && secondOgTitle < 500) {
        // Find where this block ends (before <script> or </head>)
        const blockEnd = afterFirstStyle.indexOf('<script', secondOgTitle);
        if (blockEnd > 0) {
          c = c.substring(0, c.indexOf('</head>') - (afterFirstStyle.length - blockEnd)) + c.substring(c.indexOf('</head>'));
          // This is getting complex, let's simplify
        }
      }
    }
    // Simpler: just remove everything between second og:title and </head> that contains the duplicates
    c = c.replace(/(<meta property="og:title"[^>]*>[\s\S]*?<meta name="twitter:description"[^>]*>)[\s\S]*?(<\/head>)/, '$1$2');
  }
  
  // 3. Remove duplicate <header> block that's outside the styled area
  c = c.replace(/<header>\s*<div class="container"[^>]*>[\s\S]*?<\/header>\s*/g, '');
  
  // 4. Remove the duplicate wrapper: <div class="container"><div class="article-body">
  // This creates nested article-body which breaks layout
  c = c.replace(/<div class="container"><div class="article-body">/g, '');
  
  // 5. Fix the extra </div> that closes the duplicate wrapper
  // Find the pattern: </div></div> where second closes the inner article-body
  // We need to check if there's a </div></div> pattern that leaves article-body unclosed
  
  if (c !== original) {
    fs.writeFileSync(dir + '/' + f, c);
    console.log('Fixed:', f);
  }
});
console.log('Done - processed', files.length, 'files');