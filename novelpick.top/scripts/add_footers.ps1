$footer = @"
<footer>
<a href="/">Morai</a> | <a href="/ai-tools.html">AI Tools</a> | <a href="/ai-reviews.html">Reviews</a> | <a href="/ai-comparisons.html">Comparisons</a> | <a href="/ai-guides.html">Guides</a>
<p style="margin-top:0.5rem">© 2026 Morai.top — Your Trusted AI Companion</p>
</footer>
"@

$files = @(
    "C:\Users\Administrator\github\morai-website\ai-comparisons.html",
    "C:\Users\Administrator\github\morai-website\ai-guides.html",
    "C:\Users\Administrator\github\morai-website\ai-reviews.html",
    "C:\Users\Administrator\github\morai-website\ai-tools.html",
    "C:\Users\Administrator\github\morai-website\deals.html",
    "C:\Users\Administrator\github\morai-website\index.html",
    "C:\Users\Administrator\github\morai-website\search.html",
    "C:\Users\Administrator\github\morai-website\template.html"
)

foreach ($f in $files) {
    $content = Get-Content $f -Raw -Encoding UTF8
    if ($content -match '<footer>') {
        Write-Host "[SKIP] $f already has footer"
    } else {
        $newContent = $content -replace '(\s*)(</body>)', "`$1$footer`$1`$2"
        Set-Content -Path $f -Value $newContent -Encoding UTF8 -NoNewline
        Write-Host "[ADDED] $f"
    }
}
