const fs = require('fs');
const path = require('path');

// Check for article subdirs
for (const dir of [
  'C:/Users/Administrator/.openclaw/workspace/novelpick.top/articles',
  'C:/Users/Administrator/.openclaw/workspace/articles',
  'C:/Users/Administrator/.openclaw/workspace/morai.top/articles'
]) {
  if (fs.existsSync(dir)) {
    console.log(`\n${dir}:`);
    const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));
    files.forEach(f => console.log(`  ${f}`));
  } else {
    console.log(`\n${dir}: not found`);
  }
}
