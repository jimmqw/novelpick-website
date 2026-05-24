# SEO Technical Audit Script - 3 sites
# Checks: dead links, meta completeness, H-tag hierarchy, mobile viewport, image alt texts

$results = @()

function audit-file {
    param($path, $site)
    $content = Get-Content $path -Raw -ErrorAction SilentlyContinue
    if (-not $content) { return }

    $filename = Split-Path $path -Leaf
    $issues = @()

    # Mobile viewport
    if ($content -notmatch 'viewport') {
        $issues += "MISSING viewport meta"
    }

    # Canonical
    if ($content -notmatch 'rel=["\']canonical["\']') {
        $issues += "MISSING canonical"
    }

    # OG tags
    if ($content -notmatch 'og:title') {
        $issues += "MISSING og:title"
    }
    if ($content -notmatch 'og:description') {
        $issues += "MISSING og:description"
    }

    # H1 count
    $h1count = ([regex]::Matches($content, '<h1[^>]*>')).Count
    if ($h1count -eq 0) {
        $issues += "NO H1"
    } elseif ($h1count -gt 1) {
        $issues += "MULTIPLE H1s ($h1count)"
    }

    # Image alt texts
    $imgWithoutAlt = ([regex]::Matches($content, '<img(?![^>]*alt=)[^>]*>')).Count
    if ($imgWithoutAlt -gt 0) {
        $issues += "IMAGES without alt: $imgWithoutAlt"
    }

    # Dead internal links (basic check)
    $links = [regex]::Matches($content, 'href="([^"]+)"') | ForEach-Object { $_.Groups[1].Value }
    foreach ($link in $links) {
        if ($link -match '^\/' -and $link -notmatch '^\/\/') {
            $linkedPage = Join-Path (Split-Path $path -Parent) $link.Replace('/', '\')
            if ($link -match '\.html') {
                $checkPath = Join-Path (Split-Path $path -Parent) $link.Replace('/', '\')
                if (-not (Test-Path $checkPath)) {
                    $issues += "DEAD LINK: $link"
                }
            }
        }
    }

    return [PSCustomObject]@{
        Site = $site
        File = $filename
        Issues = ($issues -join '; ')
        H1Count = $h1count
    }
}

$sites = @{
    "morai.top" = "C:\Users\Administrator\.openclaw\workspace\morai.top"
    "novelpick.top" = "C:\Users\Administrator\.openclaw\workspace\novelpick.top"
    "fateandmethod.com" = "C:\Users\Administrator\.openclaw\workspace\fateandmethod.com"
}

foreach ($site in $sites.Keys) {
    $dir = $sites[$site]
    $files = Get-ChildItem $dir -File -Filter "*.html" -ErrorAction SilentlyContinue
    foreach ($file in $files) {
        $result = audit-file $file.FullName $site
        if ($result) { $results += $result }
    }
}

# Output summary
Write-Host "=== AUDIT RESULTS ===" -ForegroundColor Cyan
Write-Host ""
$results | Where-Object { $_.Issues -ne '' } | Format-Table Site, File, Issues -AutoSize
Write-Host ""
Write-Host "Files with issues: $(($results | Where-Object { $_.Issues -ne '' }).Count)" -ForegroundColor Yellow
Write-Host "Total files checked: $($results.Count)" -ForegroundColor Yellow