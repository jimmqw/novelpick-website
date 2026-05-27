const fs = require('fs');
const dir = 'C:/Users/Administrator/github/novelpick-site';

// Read template
const template = fs.readFileSync('C:/Users/Administrator/.openclaw/workspace/scripts/novelpick-category-template.html', 'utf8');

// Fix garbled chars
function fixGarbledChars(str) {
  return str.replace(/\?\?/g, '⭐');
}

// Category page config
const categoryPages = {
  'fantasy.html': {
    title: 'Best Fantasy Novels 2026 - Epic Fantasy & Dark Fantasy | NovelPick',
    description: 'Discover the best fantasy novels of 2026. From epic fantasy to dark fantasy, find your next magical adventure.',
    keywords: 'fantasy novels, epic fantasy, dark fantasy, sword and sorcery',
    category: 'Fantasy',
    subtitle: 'From epic quest to dark intrigue — discover your next magical adventure',
    date: 'April 2026',
    readTime: '5 min read'
  },
  'litrpg.html': {
    title: 'Best LitRPG Novels 2026 - Progression Fantasy | NovelPick',
    description: 'Top LitRPG and progression fantasy novels. Stats, levels, skills — the best gaming-inspired stories.',
    keywords: 'litrpg, progression fantasy, gaming novels',
    category: 'LitRPG',
    subtitle: 'Level up your reading list with these gaming-inspired stories',
    date: 'April 2026',
    readTime: '6 min read'
  },
  'scifi.html': {
    title: 'Best Sci-Fi Novels 2026 - Space Opera & Cyberpunk | NovelPick',
    description: 'Best science fiction novels. Space opera, cyberpunk, dystopian futures.',
    keywords: 'scifi, science fiction, space opera, cyberpunk',
    category: 'Sci-Fi',
    subtitle: 'Explore the final frontier and beyond',
    date: 'April 2026',
    readTime: '5 min read'
  },
  'romance.html': {
    title: 'Best Romance Novels 2026 - Love Stories | NovelPick',
    description: 'Best romance novels and love stories. From enemies to lovers to happily ever after.',
    keywords: 'romance, love stories, ya romance',
    category: 'Romance',
    subtitle: 'Find your next great love story',
    date: 'April 2026',
    readTime: '4 min read'
  },
  'reviews.html': {
    title: 'Book Reviews 2026 - Honest Novel Reviews | NovelPick',
    description: 'Honest book reviews. Find your next favorite read.',
    keywords: 'book reviews, novel reviews',
    category: 'Reviews',
    subtitle: 'Honest reviews to help you find your next favorite book',
    date: 'April 2026',
    readTime: '3 min read'
  }
};

Object.keys(categoryPages).forEach(f => {
  try {
    const originalContent = fs.readFileSync(dir + '/' + f, 'utf8');
    
    // Extract content between <main class="page-wrap"> and </main>
    let content = '';
    const mainMatch = originalContent.match(/<main class="page-wrap">([\s\S]*?)<\/main>/);
    if (mainMatch) {
      // Extract article-body div content
      const abMatch = mainMatch[1].match(/<div class="article-body">([\s\S]*?)<\/div>\s*<aside/);
      if (abMatch) {
        content = abMatch[1];
        // Fix garbled chars
        content = fixGarbledChars(content);
      }
    }
    
    if (!content || content.length < 100) {
      console.log('Skipping', f, '- no content');
      return;
    }
    
    const cfg = categoryPages[f];
    
    let newContent = template
      .replace(/{{TITLE}}/g, cfg.title)
      .replace(/{{DESCRIPTION}}/g, cfg.description)
      .replace(/{{KEYWORDS}}/g, cfg.keywords)
      .replace(/{{CANONICAL}}/g, `https://novelpick.top/${f}`)
      .replace(/{{OG_TITLE}}/g, cfg.title)
      .replace(/{{OG_DESCRIPTION}}/g, cfg.description)
      .replace(/{{OG_URL}}/g, `https://novelpick.top/${f}`)
      .replace(/{{TWITTER_TITLE}}/g, cfg.title)
      .replace(/{{TWITTER_DESCRIPTION}}/g, cfg.description)
      .replace(/{{CATEGORY}}/g, cfg.category)
      .replace(/{{SUBTITLE}}/g, cfg.subtitle)
      .replace(/{{DATE}}/g, cfg.date)
      .replace(/{{READ_TIME}}/g, cfg.readTime)
      .replace(/{{CONTENT}}/g, content);
    
    fs.writeFileSync(dir + '/' + f, newContent);
    console.log('Regenerated:', f, '- content:', content.length, 'chars');
  } catch (e) {
    console.log('Error:', f, e.message);
  }
});

console.log('\nCategory pages done!');