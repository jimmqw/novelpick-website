Get-ChildItem "C:\Users\Administrator\github\novelpick-website\*.html" -Recurse | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    if ($content -match '<div[^>]*class="article-body"[^>]*>([\s\S]*?)</div>') {
        $body = $matches[1]
        $len = $body.Length
        if ($len -lt 500) {
            Write-Output "$($_.FullName)|$len"
        }
    }
}