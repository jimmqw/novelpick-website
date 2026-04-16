const fs = require('fs');
const dir = 'C:/Users/Administrator/github/novelpick-site';

// Read template
const template = fs.readFileSync('C:/Users/Administrator/.openclaw/workspace/scripts/novelpick-article-template.html', 'utf8');

// Read a sample current file to understand its structure
const sampleFile = 'best-cyberpunk-novels.html';
const sampleContent = fs.readFileSync(dir + '/' + sampleFile, 'utf8');

// Extract content from current pages
function extractContent(html, category) {
  // Extract article body content
  const bodyMatch = html.match(/<div class="article-body">([\s\S]*?)<\/div>\s*<\/main>/);
  const content = bodyMatch ? bodyMatch[1] : '';
  
  // Extract title
  const titleMatch = html.match(/<h1[^>]*>([^<]+)<\/h1>/);
  const title = titleMatch ? titleMatch[1] : 'Article Title';
  
  // Extract meta info
  const dateMatch = html.match(/📅\s*([^<]+)/);
  const date = dateMatch ? dateMatch[1].trim() : 'April 7, 2026';
  
  const readTimeMatch = html.match(/⏱️\s*(\d+\s*min)/);
  const readTime = readTimeMatch ? readTimeMatch[1].trim() : '8 min read';
  
  // Extract subtitle
  const subtitleMatch = html.match(/<p[^>]*>([^\n<]+)<\/p>/);
  const subtitle = subtitleMatch ? subtitleMatch[1].trim().substring(0, 150) : 'Curated recommendations';
  
  return { title, content, date, readTime, subtitle, category };
}

// Category mapping
const categoryMap = {
  'fantasy': { name: 'Fantasy', link: '/fantasy.html', icon: '☁️' },
  'litrpg': { name: 'LitRPG', link: '/litrpg.html', icon: '⚔️' },
  'scifi': { name: 'Sci-Fi', link: '/scifi.html', icon: '🚀' },
  'romance': { name: 'Romance', link: '/romance.html', icon: '❤️' },
  'reviews': { name: 'Reviews', link: '/reviews.html', icon: '⭐' }
};

// Get all article files (not index or category pages)
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html') && f !== 'index.html');

files.forEach(f => {
  // Skip category pages for now
  if (['fantasy.html', 'litrpg.html', 'scifi.html', 'romance.html', 'reviews.html'].includes(f)) {
    return;
  }
  
  try {
    const oldContent = fs.readFileSync(dir + '/' + f, 'utf8');
    const extracted = extractContent(oldContent, 'fantasy');
    
    // Determine category from file or URL
    let category = 'fantasy';
    if (f.includes('litrpg') || f.includes('system-apocalypse') || f.includes('progression')) category = 'litrpg';
    else if (f.includes('scifi') || f.includes('cyberpunk') || f.includes('space-opera')) category = 'scifi';
    else if (f.includes('romance') || f.includes('enemies-to-lovers')) category = 'romance';
    else if (f.includes('review')) category = 'reviews';
    
    const cat = categoryMap[category] || categoryMap.fantasy;
    
    // Replace template placeholders
    let newContent = template
      .replace(/{{TITLE}}/g, extracted.title)
      .replace(/{{DESCRIPTION}}/g, extracted.subtitle)
      .replace(/{{KEYWORDS}}/g, extracted.title.toLowerCase().replace(/[^a-z0-9\s]/g, '').replace(/\s+/g, ', '))
      .replace(/{{CANONICAL}}/g, `https://novelpick.top/${f}`)
      .replace(/{{OG_TITLE}}/g, `${extracted.title} | NovelPick`)
      .replace(/{{OG_DESCRIPTION}}/g, extracted.subtitle)
      .replace(/{{OG_URL}}/g, `https://novelpick.top/${f}`)
      .replace(/{{TWITTER_TITLE}}/g, `${extracted.title} | NovelPick`)
      .replace(/{{TWITTER_DESCRIPTION}}/g, extracted.subtitle)
      .replace(/{{CATEGORY}}/g, cat.name)
      .replace(/{{CATEGORY_LINK}}/g, cat.link)
      .replace(/{{CATEGORY_ICON}}/g, cat.icon)
      .replace(/{{SUBTITLE}}/g, extracted.subtitle)
      .replace(/{{DATE}}/g, extracted.date)
      .replace(/{{READ_TIME}}/g, extracted.readTime)
      .replace(/{{CONTENT}}/g, extracted.content)
      .replace(/{{RELATED_ARTICLES}}/g, '')
      .replace(/{{PREV_LINK}}/g, '#')
      .replace(/{{PREV_TITLE}}/g, 'Previous Article')
      .replace(/{{NEXT_LINK}}/g, '#')
      .replace(/{{NEXT_TITLE}}/g, 'Next Article');
    
    fs.writeFileSync(dir + '/' + f, newContent);
    console.log('Regenerated:', f);
  } catch (e) {
    console.log('Error:', f, e.message);
  }
});

console.log('Done - processed', files.length, 'files');