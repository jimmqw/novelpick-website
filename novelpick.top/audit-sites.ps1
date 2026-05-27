# Site Audit Script - ASCII safe

$sites = @(
    @{ Name = "morai"; Path = "C:\Users\Administrator\github\morai-website\"; NeedsBaidu = $true },
    @{ Name = "novelpick"; Path = "C:\Users\Administrator\github\novelpick-website\"; NeedsBaidu = $true },
    @{ Name = "fateandmethod"; Path = "C:\Users\Administrator\github\fateandmethod-site\"; NeedsBaidu = $false }
)

$problems = @()
$normal = @()
$total = 0

foreach ($site in $sites) {
    $files = Get-ChildItem $site.Path -Recurse -Filter "*.html"
    foreach ($file in $files) {
        $total++
        $content = Get-Content $file.FullName -Raw -Encoding UTF8
        $filename = $file.Name
        $relPath = $file.FullName.Replace($site.Path, "")

        $issues = @()

        # 1. Structural checks
        # header
        if ($content -notmatch '<header') {
            $issues += "header-missing"
        }

        # nav exists
        if ($content -notmatch '<nav') {
            $issues += "nav-missing"
        }

        # breadcrumb
        if ($content -notmatch '(?i)breadcrumb') {
            $issues += "breadcrumb-missing"
        }

        # sidebar
        if ($content -notmatch '(?i)(sidebar|aside)') {
            $issues += "sidebar-missing"
        }

        # sidebar not empty
        $sidebarMatch = [regex]::Match($content, '(?i)<aside[^>]*>(.*?)</aside>', [System.Text.RegularExpressions.RegexOptions]::Singleline)
        if ($sidebarMatch.Success -and $sidebarMatch.Groups[1].Value.Length -lt 50) {
            $issues += "sidebar-empty"
        }

        # related articles
        if ($content -notmatch '(?i)(related|recommended)') {
            $issues += "related-articles-missing"
        }

        # footer
        if ($content -notmatch '<footer') {
            $issues += "footer-missing"
        }
        if ($content -match '<footer' -and $content -notmatch '(?i)(copyright|©|&copy;)') {
            $issues += "footer-no-copyright"
        }

        # Baidu stats
        if ($site.NeedsBaidu -and $content -notmatch 'hm\.baidu\.com') {
            $issues += "baidu-stats-missing"
        }

        # 2. Content quality
        $bodyMatch = [regex]::Match($content, '(?i)<div[^>]*id=["\''].*article[-_]?body[^"\''>]*>(.*?)</div>', [System.Text.RegularExpressions.RegexOptions]::Singleline)
        if (-not $bodyMatch.Success) {
            $bodyMatch = [regex]::Match($content, '(?i)<article[^>]*>(.*?)</article>', [System.Text.RegularExpressions.RegexOptions]::Singleline)
        }
        if ($bodyMatch.Success) {
            $bodyText = $bodyMatch.Groups[1].Value -replace '<[^>]+>', ''
            if ($bodyText.Length -lt 200) {
                $issues += "body-too-short-$($bodyText.Length)-chars"
            }
        } else {
            $issues += "no-article-body-found"
        }

        # SEO meta tags
        if ($content -notmatch 'og:title') { $issues += "og-title-missing" }
        if ($content -notmatch 'og:description') { $issues += "og-desc-missing" }
        if ($content -notmatch 'canonical') { $issues += "canonical-missing" }

        # reading time
        if ($content -notmatch '(?i)(min|minute|read|阅读)') {
            $issues += "reading-time-missing"
        }

        # 3. Layout checks
        if ($content -notmatch 'background-color' -and $content -notmatch '<style') {
            $issues += "css-missing"
        }

        # div nesting balance
        $abMatch = [regex]::Match($content, '(?i)<div[^>]*id=["\''].*article[-_]?body[^"\''>]*>(.*?)</div>', [System.Text.RegularExpressions.RegexOptions]::Singleline)
        if ($abMatch.Success) {
            $abContent = $abMatch.Groups[1].Value
            $openDivs = ([regex]::Matches($abContent, '<div[^>]*>')).Count
            $closeDivs = ([regex]::Matches($abContent, '</div>')).Count
            if ($openDivs -ne $closeDivs) {
                $issues += "div-nesting-unbalanced-$openDivs-$closeDivs"
            }
        }

        # 4. Mobile
        if ($content -notmatch 'viewport') {
            $issues += "viewport-missing"
        }
        if ($content -notmatch '@media') {
            $issues += "responsive-css-missing"
        }

        if ($issues.Count -eq 0) {
            $normal += $relPath
        } else {
            $problems += [PSCustomObject]@{
                File = $relPath
                Site = $site.Name
                Issues = $issues -join " | "
            }
        }
    }
}

Write-Host "=== Audit Report $(Get-Date -Format 'yyyy-MM-dd HH:mm') ===" -ForegroundColor Cyan

if ($normal.Count -gt 0) {
    Write-Host "`n[PASS] Normal pages" -ForegroundColor Green
    foreach ($n in $normal) { Write-Host "  OK  $n" }
}

if ($problems.Count -gt 0) {
    Write-Host "`n[WARN] Pages with issues" -ForegroundColor Yellow
    foreach ($p in $problems) {
        Write-Host "  $($p.Site): $($p.File)" -ForegroundColor Yellow
        Write-Host "    -> $($p.Issues)" -ForegroundColor Red
    }
}

Write-Host "`n[STAT] Total: $total | OK: $($normal.Count) | Issues: $($problems.Count)" -ForegroundColor Cyan
