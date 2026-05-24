const fs = require('fs');
const path = require('path');

const dirs = {
  'fateandmethod': 'C:\\Users\\Administrator\\.openclaw\\workspace\\fateandmethod.com',
  'novelpick': 'C:\\Users\\Administrator\\.openclaw\\workspace\\novelpick.top',
  'morai': 'C:\\Users\\Administrator\\.openclaw\\workspace\\morai.top',
};

let total = 0;
let fixed = 0;

Object.entries(dirs).forEach(([site, dir]) => {
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));
  console.log(`\n=== ${site}.top (${files.length} HTML files) ===`);
  files.forEach(f => {
    const fp = path.join(dir, f);
    const c = fs.readFileSync(fp, 'utf8');
    const issues = [];
    if (!c.includes('rel="canonical"') && !c.includes("rel='canonical'")) issues.push('noCanonical');
    if (!c.includes('<header') && !c.includes('<Header')) issues.push('noHeader');
    if (!c.includes('hm.baidu.com') && !c.includes('hm.js')) issues.push('noBaidu');
    if (!c.includes('og:site_name') && !c.includes('og:site')) issues.push('noOGsite');
    if (issues.length > 0) {
      total += issues.length;
      fixed++;
      console.log(`  ⚠️ ${f}: ${issues.join(', ')}`);
    }
  });
});

console.log(`\nTotal files with issues: ${fixed} files, ${total} issues`);