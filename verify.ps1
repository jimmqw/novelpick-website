$content = Get-Content 'C:\Users\Administrator\github\novelpick-website\litrpg.html' -Raw
if ($content -match '<div[^>]*class="article-body"[^>]*>([\s\S]*?)</div>') {
    Write-Output "Article body length: $($matches[1].Length)"
}

$open = ([regex]::Matches($content, '<div')).Count
$close = ([regex]::Matches($content, '</div>')).Count
Write-Output "Open divs: $open, Close divs: $close"