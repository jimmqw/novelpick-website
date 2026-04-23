const fs = require('fs');
const dir = 'C:/Users/Administrator/github/novelpick-site';

// Read template
const template = fs.readFileSync('C:/Users/Administrator/.openclaw/workspace/scripts/novelpick-article-template.html', 'utf8');

// Get all files
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html') && f !== 'index.html');

// Category mapping
const categoryMap = {
  fantasy: { name: 'Fantasy', link: '/fantasy.html', icon: '☁️' },
  litrpg: { name: 'LitRPG', link: '/litrpg.html', icon: '⚔️' },
  scifi: { name: 'Sci-Fi', link: '/scifi.html', icon: '🚀' },
  romance: { name: 'Romance', link: '/romance.html', icon: '❤️' },
  reviews: { name: 'Reviews', link: '/reviews.html', icon: '⭐' }
};

files.forEach(f => {
  if (['fantasy.html', 'litrpg.html', 'scifi.html', 'romance.html', 'reviews.html'].includes(f)) return;
  
  try {
    const originalContent = fs.readFileSync(dir + '/' + f, 'utf8');
    
    let content = '';
    let title = '';
    let subtitle = '';
    let date = 'April 7, 2026';
    let readTime = '8 min read';
    
    // Get title from h1
    const h1Match = originalContent.match(/<h1[^>]*>([^<]+)<\/h1>/);
    if (h1Match) title = h1Match[1].replace(/🎮|☁️|⚔️|🚀|❤️|⭐/g, '').trim();
    
    // Try multiple patterns to get full article content
    // Pattern 1: <div class="article-body" ... > ... </div> followed by sidebar/footer
    const abMatch = originalContent.match(/<div class="article-body"[^>]*>([\s\S]*?)<\/div>\s*<(?:aside|footer|div class="sidebar)/);
    if (abMatch) content = abMatch[1];
    
    // If empty, try article-body without strict ending
    if (!content || content.length < 500) {
      const abMatch2 = originalContent.match(/<div class="article-body"[^>]*>([\s\S]*)/);
      if (abMatch2) {
        // Take everything until we hit the sidebar
        let partial = abMatch2[1];
        const sidebarIdx = partial.indexOf('<aside');
        if (sidebarIdx > 500) content = partial.substring(0, sidebarIdx);
        else content = partial;
      }
    }
    
    // If still empty, try article tag
    if (!content || content.length < 500) {
      const articleMatch = originalContent.match(/<article[^>]*>([\s\S]*?)<\/article>/);
      if (articleMatch) content = articleMatch[1];
    }
    
    // Final fallback: just get everything in .article-body
    if (!content || content.length < 500) {
      const containerMatch = originalContent.match(/<div class="container"[^>]*>([\s\S]*?)<\/div>\s*<(?:div|aside|footer)/);
      if (containerMatch) content = containerMatch[1];
    }
    
    if (!content || content.length < 100) {
      console.log('Skipping (no content):', f, 'len:', content ? content.length : 0);
      return;
    }
    
    // Extract meta
    const dateMatch = originalContent.match(/📅\s*([^<\n]+)/);
    if (dateMatch) date = dateMatch[1].trim();
    
    const readTimeMatch = originalContent.match(/⏱️?\s*(\d+\s*min)/);
    if (readTimeMatch) readTime = readTimeMatch[1].trim();
    
    // Determine category
    let category = 'fantasy';
    if (f.includes('litrpg') || f.includes('system-apocalypse') || f.includes('progression')) category = 'litrpg';
    else if (f.includes('scifi') || f.includes('cyberpunk') || f.includes('space-opera')) category = 'scifi';
    else if (f.includes('romance') || f.includes('enemies-to-lovers')) category = 'romance';
    else if (f.includes('review')) category = 'reviews';
    
    const cat = categoryMap[category] || categoryMap.fantasy;
    
    // Get subtitle from first paragraph
    const pMatch = content.match(/<p[^>]*>([^<]+)<\/p>/);
    if (pMatch && pMatch[1].length > 20) {
      subtitle = pMatch[1].substring(0, 150);
    } else {
      subtitle = 'Curated recommendations for ' + cat.name.toLowerCase() + ' fans';
    }
    
    let newContent = template
      .replace(/{{TITLE}}/g, title || f.replace('.html', '').replace(/-/g, ' '))
      .replace(/{{DESCRIPTION}}/g, subtitle)
      .replace(/{{KEYWORDS}}/g, (title || '').toLowerCase().replace(/[^a-z0-9\s]/g, '').replace(/\s+/g, ', '))
      .replace(/{{CANONICAL}}/g, `https://novelpick.top/${f}`)
      .replace(/{{OG_TITLE}}/g, `${title} | NovelPick`)
      .replace(/{{OG_DESCRIPTION}}/g, subtitle)
      .replace(/{{OG_URL}}/g, `https://novelpick.top/${f}`)
      .replace(/{{TWITTER_TITLE}}/g, `${title} | NovelPick`)
      .replace(/{{TWITTER_DESCRIPTION}}/g, subtitle)
      .replace(/{{CATEGORY}}/g, cat.name)
      .replace(/{{CATEGORY_LINK}}/g, cat.link)
      .replace(/{{CATEGORY_ICON}}/g, cat.icon)
      .replace(/{{SUBTITLE}}/g, subtitle)
      .replace(/{{DATE}}/g, date)
      .replace(/{{READ_TIME}}/g, readTime)
      .replace(/{{CONTENT}}/g, content)
      .replace(/{{RELATED_ARTICLES}}/g, '')
      .replace(/{{PREV_LINK}}/g, '#')
      .replace(/{{PREV_TITLE}}/g, 'Previous')
      .replace(/{{NEXT_LINK}}/g, '#')
      .replace(/{{NEXT_TITLE}}/g, 'Next');
    
    fs.writeFileSync(dir + '/' + f, newContent);
    console.log('Regenerated:', f, '- content:', content.length, 'chars');
  } catch (e) {
    console.log('Error:', f, e.message);
  }
});

console.log('Done');