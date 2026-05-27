# Fix remaining dead links in morai.top
$map = @{
    "/best-ai-coding-assistants-2026.html" = "/best-ai-agents-2026.html"
    "/best-ai-video-editing-tools-2026.html" = "/best-ai-video-generation-tools-2026.html"
    "/ai-for-small-business-guide.html" = "/best-ai-productivity-tools-2026.html"
    "/privacy.html" = "/privacy.html"
    "/contact.html" = "/contact.html"
}

$files = Get-ChildItem "C:\Users\Administrator\.openclaw\workspace\morai.top" -Filter "*.html"
foreach ($f in $files) {
    $content = Get-Content $f.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $content) { continue }
    $changed = $false
    foreach ($key in $map.Keys) {
        if ($content -match [regex]::Escape($key)) {
            $content = $content -replace [regex]::Escape($key), $map[$key]
            $changed = $true
        }
    }
    if ($changed) {
        Set-Content $f.FullName $content -NoNewline
        Write-Host "Fixed: $($f.Name)"
    }
}