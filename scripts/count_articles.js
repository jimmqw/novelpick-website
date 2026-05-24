const fs = require('fs');
const path = require('path');

const sites = {
  'morai.top': 'C:/Users/Administrator/.openclaw/workspace/morai.top',
  'novelpick.top': 'C:/Users/Administrator/.openclaw/workspace/novelpick.top',
  'fateandmethod.com': 'C:/Users/Administrator/.openclaw/workspace/fateandmethod.com',
};

for (const [site, dir] of Object.entries(sites)) {
  console.log(`\n=== ${site} ===`);
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.html') && !['index.html','sitemap.xml'].includes(f));
  const counts = [];
  for (const f of files.sort()) {
    const html = fs.readFileSync(path.join(dir, f), 'utf8');
    const text = html.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
    counts.push(text.length);
    console.log(`  ${f}: ${text.length} 字符`);
  }
  if (counts.length) {
    const avg = Math.round(counts.reduce((a,b)=>a+b,0)/counts.length);
    console.log(`  共${counts.length}篇 | 平均${avg} | 最小${Math.min(...counts)} | 最大${Math.max(...counts)}`);
  }
}
