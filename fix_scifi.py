with open(r'C:\Users\Administrator\github\novelpick-website\scifi.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''                <p>End of the world scenarios, survival stories, and post-apocalyptic adventures.</p>
                <div class="tags"><span class="tag">Apocalypse</span><span class="tag">Survival</span></div>
            </div>
        </div>
    </div>
    <div class="related">'''

new = '''                <p>End of the world scenarios, survival stories, and post-apocalyptic adventures.</p>
                <div class="tags"><span class="tag">Apocalypse</span><span class="tag">Survival</span></div>
            </div>
        </div>

        <div class="verdict-box">
            <h3>The NovelPick Verdict — Sci-Fi 2026</h3>
            <p>Sci-fi web fiction in 2026 is in exceptional health. The genre has matured beyond simple power fantasies and space operas, with authors now exploring genuinely complex ideas about consciousness, identity, and the ethics of technological progress. Whether you are here for the <strong>galactic-scale drama of space opera</strong>, the <strong>anxiously relevant surveillance themes of cyberpunk</strong>, or the <strong>temporal head-scratching of time travel fiction</strong>, the ecosystem has never been richer.</p>
            <p>Start with whichever subgenre resonates with your current mood — but know that once you go deep in one, you will find yourself curious about the others. Sci-fi greatest gift is perspective: it shows us where we are going by imagining who we might become.</p>
        </div>
    </div>
    <div class="related">'''

if old in content:
    content = content.replace(old, new, 1)
    with open(r'C:\Users\Administrator\github\novelpick-website\scifi.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('SUCCESS: replacement done')
else:
    print('ERROR: old content not found')
    idx = content.find('End of the world scenarios')
    if idx >= 0:
        print('Found at idx:', idx)
        print(repr(content[idx-50:idx+200]))
    else:
        print('Could not find "End of the world scenarios"')