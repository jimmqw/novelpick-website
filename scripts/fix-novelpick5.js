const fs = require('fs');
const dir = 'C:/Users/Administrator/github/novelpick-site';

// Read index.html as template
const indexHtml = fs.readFileSync(dir + '/index.html', 'utf8');

// Extract head section from index
const headMatch = indexHtml.match(/<head>[\s\S]*?<\/head>/);
const templateHead = headMatch ? headMatch[0] : null;

if (!templateHead) {
  console.log('Could not extract head from index.html');
  process.exit(1);
}

// Get all article pages (not index)
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html') && f !== 'index.html');

files.forEach(f => {
  let c = fs.readFileSync(dir + '/' + f, 'utf8');
  
  // Check if file has broken head structure
  if (c.includes('</style>\n    <meta property="og:title"') || c.includes('<head>\n    </style>')) {
    // Replace the broken head with template
    const bodyMatch = c.match(/<\/head>\s*<body>[\s\S]*$/);
    const bodyContent = bodyMatch ? bodyMatch[0] : c;
    
    // Build new file: doctype + head + body
    const newContent = '<!DOCTYPE html>\n<html lang="en">\n' + templateHead + '\n' + bodyContent;
    
    fs.writeFileSync(dir + '/' + f, newContent);
    console.log('Fixed:', f);
  }
});

console.log('Done - processed', files.length, 'files');