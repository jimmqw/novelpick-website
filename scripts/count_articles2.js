const fs = require('fs');
const path = require('path');

// Count articles in subdirs
const artdirs = [
  'C:/Users/Administrator/.openclaw/workspace/novelpick.top/articles',
  'C:/Users/Administrator/.openclaw/workspace/articles',
];

for (const dir of artdirs) {
  console.log(`\n=== ${dir} ===`);
  if (!fs.existsSync(dir)) { console.log('  not found'); continue; }
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));
  for (const f of files.sort()) {
    const html = fs.readFileSync(path.join(dir, f), 'utf8');
    const text = html.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
    console.log(`  ${f}: ${text.length} 字符`);
  }
}
