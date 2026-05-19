$files = Get-ChildItem "C:\Users\Administrator\github\novelpick-website" -Filter "*.html"
$results = @()
foreach ($f in $files) {
    $html = Get-Content $f.FullName -Raw -Encoding UTF8
    if ($html -match '<div class="article-body">(.*?)</div>\s*<(?:aside|main)') {
        $body = $matches[1]
        $text = $body -replace '<[^>]+>', ' ' -replace '\s+', ' ' -replace '&nbsp;', ' ' -replace '&amp;', '&'
        $len = $text.Trim().Length
        $results += [PSCustomObject]@{Name=$f.Name; TextLen=$len; Preview=$text.Substring(0,[Math]::Min(80,$text.Length))}
    }
}
$results | Sort-Object TextLen | Format-Table -AutoSize