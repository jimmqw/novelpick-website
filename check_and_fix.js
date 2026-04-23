const fs = require('fs');
const c = fs.readFileSync('C:/Users/Administrator/.openclaw/workspace/morai.top/best-ai-video-generation-tools-2026.html', 'utf8');
const marker = '<a href="#" class="back-to-top"';
const idx = c.indexOf(marker);
console.log('Marker found at:', idx, 'total len:', c.length);
if (idx > 0) {
    const good = c.substring(0, idx);
    fs.writeFileSync('C:/Users/Administrator/.openclaw/workspace/morai.top/best-ai-video-generation-tools-2026.html', good);
    console.log('Truncated to', good.length, 'chars');
}
