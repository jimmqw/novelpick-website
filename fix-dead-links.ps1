# Fix dead links in morai.top
$map = @{
    "/best-ai-coding-tools-2026.html" = "/github-copilot-review-2026.html"
    "/ai-for-summarization-notes-2026.html" = "/best-ai-note-taking-tools-2026.html"
    "/ai-productivity-tools-2026.html" = "/best-ai-productivity-tools-2026.html"
    "/best-ai-tools-2026.html" = "/ai-tools.html"
    "/best-ai-image-generators-2026-comparison.html" = "/ai-image-generators.html"
    "/chatgpt-vs-claude-vs-gemini-2026.html" = "/chatgpt-vs-claude.html"
    "/claude-3-7-sonnet-review.html" = "/best-ai-chatbots-2026.html"
    "/cursor-ai-review.html" = "/best-ai-agents-2026.html"
    "/best-ai-image-editors-2026.html" = "/ai-image-generators.html"
    "/privacy.html" = "/privacy.html"
    "/contact.html" = "/contact.html"
}

$files = Get-ChildItem "C:\Users\Administrator\.openclaw\workspace\morai.top" -Filter "*.html"
$deadFiles = @()
$missing = @()

foreach ($f in $files) {
    $content = Get-Content $f.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $content) { continue }
    $changed = $false
    foreach ($key in $map.Keys) {
        $replacement = $map[$key]
        # Check if the target file actually exists
        if ($key -ne $replacement) {
            $targetExists = Test-Path "C:\Users\Administrator\.openclaw\workspace\morai.top\$($replacement -replace '/', '\')"
            if (-not $targetExists) {
                $missing += "$($f.Name): target $($replacement) does not exist"
                continue
            }
        }
        if ($content -match [regex]::Escape($key)) {
            $content = $content -replace [regex]::Escape($key), $replacement
            $changed = $true
        }
    }
    if ($changed) {
        Set-Content $f.FullName $content -NoNewline
        Write-Host "Fixed: $($f.Name)" -ForegroundColor Green
    }
}

if ($missing.Count -gt 0) {
    Write-Host "Missing targets:" -ForegroundColor Yellow
    $missing | ForEach-Object { Write-Host "  $_" }
}