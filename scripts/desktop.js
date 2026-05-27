const fs = require('fs');
const path = require('path');

const desktop = 'C:/Users/Administrator/Desktop';
const items = fs.readdirSync(desktop);
items.forEach(f => console.log(f));
