const fs = require('fs');
const dir = 'C:/Users/Administrator/github/fateandmethod-site';

const files = ['ziwei-intro.html', 'ziwei-stars.html', 'ziwei-palaces.html', 'ziwei-combinations.html', 'ziwei-reading.html'];

const newLinks = `
            <li><a href="./ziwei-si-hua.html">Four Transformations</a></li>
            <li><a href="./ziwei-palaces-explained.html">12 Palaces Explained</a></li>`;

files.forEach(f => {
  let c = fs.readFileSync(dir + '/' + f, 'utf8');
  const oldText = '<li><a href="./ziwei-reading.html">How to Read a Chart</a></li>\n        </ul>';
  const newText = '<li><a href="./ziwei-reading.html">How to Read a Chart</a></li>' + newLinks + '\n        </ul>';
  
  if (c.includes(oldText.replace(/\n\s+/g, '\n'))) {
    c = c.replace(oldText, newText);
    fs.writeFileSync(dir + '/' + f, c);
    console.log('Updated:', f);
  } else if (c.includes('Four Transformations')) {
    console.log('Already has links:', f);
  } else {
    console.log('Need to update manually:', f);
  }
});

console.log('Done');