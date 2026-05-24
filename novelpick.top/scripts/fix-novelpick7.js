const fs = require('fs');
const dir = 'C:/Users/Administrator/github/novelpick-site';

// Read index.html head template
const indexHtml = fs.readFileSync(dir + '/index.html', 'utf8');
const headMatch = indexHtml.match(/<head>[\s\S]*?<\/head>/);
const templateHead = headMatch[0];

// Get all article pages
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html') && f !== 'index.html');

files.forEach(f => {
  let c = fs.readFileSync(dir + '/' + f, 'utf8');
  
  // Check if file has broken head (with 4 spaces after newline)
  if (c.includes('<head>\r\n    </style>') || c.includes('<head>\n    </style>')) {
    // Extract body content
    const bodyMatch = c.match(/<\/head>[\s\S]*$/);
    if (bodyMatch) {
      const newContent = '<!DOCTYPE html>\n<html lang="en">\n' + templateHead + '\n' + bodyMatch[0];
      fs.writeFileSync(dir + '/' + f, newContent);
      console.log('Fixed:', f);
    }
  }
});

console.log('Done - processed', files.length, 'files');