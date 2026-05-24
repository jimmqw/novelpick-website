$html = Get-Content 'C:\Users\Administrator\github\novelpick-website\litrpg.html' -Raw

$articleBody = [regex]::Match($html, '(?<=<div class="article-body"[^>]*>).*?(?=</div>\s*<div class="related")', [System.Text.RegularExpressions.RegexOptions]::Singleline).Value
Write-Output "Article body length: $($articleBody.Length)"

$open = ([regex]::Matches($html, '<div\b')).Count
$close = ([regex]::Matches($html, '</div>')).Count
Write-Output "Open divs: $open, Close divs: $close"

if ($open -eq $close) {
    Write-Output "✓ DIV BALANCED"
} else {
    Write-Output "✗ DIV IMBALANCED by $($close - $open)"
}

# check for emoji corruption
if ($html -match '\?\?|\?\?|\?\?|\?\?') {
    Write-Output "⚠ Emoji corruption detected"
} else {
    Write-Output "✓ No emoji corruption"
}