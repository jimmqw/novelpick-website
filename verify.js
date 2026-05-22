const fs = require('fs');
const c = fs.readFileSync('C:\\Users\\Administrator\\github\\novelpick-website\\reviews.html', 'utf8');
const bodyIdx = c.indexOf('<body');
const afterBody = c.substring(bodyIdx);
let m = afterBody.match(/<div[^>]*class="article-body"[^>]*>([\s\S]*?)<aside/);
if (!m) m = afterBody.match(/<main[^>]*class="[^"]*article-body[^"]*"[^>]*>([\s\S]*?)<\/main>/);
if (!m) m = afterBody.match(/<div[^>]*class="[^"]*article-body[^"]*"[^>]*>([\s\S]*?)<footer/);
if (m) {
    let t = m[1].replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
    console.log('article-body len: ' + t.length);
} else {
    console.log('no match');
}
const opens = (c.match(/<div/g) || []).length;
const closes = (c.match(/<\/div>/g) || []).length;
console.log('div opens: ' + opens + ' closes: ' + closes);
const hasGarbled = /\uFFFD/.test(c);
console.log('Has garbled chars: ' + hasGarbled);