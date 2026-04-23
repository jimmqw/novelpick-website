const fs = require('fs');
const path = require('path');

function listPages(dir, base = '') {
  if (!fs.existsSync(dir)) return [];
  let pages = [];
  try {
    const items = fs.readdirSync(dir);
    for (const item of items) {
      const fullPath = path.join(dir, item);
      const relPath = base ? base + '/' + item : item;
      if (fs.statSync(fullPath).isDirectory()) {
        pages = pages.concat(listPages(fullPath, relPath));
      } else if (item.endsWith('.html') || item.endsWith('.md')) {
        pages.push(relPath);
      }
    }
  } catch(e) {}
  return pages;
}

const resolved = [
  { name: 'morai.top', root: 'C:/Users/Administrator/jimmqw/morai-website' },
  { name: 'novelpick.top', root: 'C:/Users/Administrator/jimmqw/novelpick-website' },
  { name: 'fateandmethod.com', root: 'C:/Users/Administrator/jimmqw/fateandmethod-website' }
];

for (const site of resolved) {
  const pages = listPages(site.root);
  console.log(site.name + ': ' + pages.length + ' pages');
  console.log(pages.slice(0, 30).join('\n'));
  console.log('---');
}
