# Website Quality Audit Script v2 - Fixed detection logic
$results = @()
$siteConfigs = @(
    @{
        Name = "morai"
        Path = "C:\Users\Administrator\github\morai-website"
        NeedBaidu = $true
        Theme = "dark"
    },
    @{
        Name = "novelpick"
        Path = "C:\Users\Administrator\github\novelpick-website"
        NeedBaidu = $true
        Theme = "dark"
    },
    @{
        Name = "fateandmethod"
        Path = "C:\Users\Administrator\github\fateandmethod-site"
        NeedBaidu = $false
        Theme = "dark"
    }
)

function Test-HasElement($content, $selector) {
    switch ($selector) {
        "header" { return $content -match '<header|class="\.nav"|class="nav"' }
        "nav" { return $content -match '<nav|class="\.nav"' }
        "breadcrumb" { return $content -match 'breadcrumb' }
        "sidebar" { return $content -match '<aside|class="sidebar"' }
        "related" { return $content -match 'related' }
        "footer" { return $content -match '<footer|class="footer"' }
        "baidu" { return $content -match 'hm\.baidu\.com' }
        "ogtitle" { return $content -match 'og:title' }
        "ogdesc" { return $content -match 'og:description' }
        "canonical" { return $content -match 'canonical' }
        "viewport" { return $content -match 'viewport' }
        "media" { return $content -match '@media' }
        "bodybg" { return $content -match 'body[^{]*\{[^}]*background' -or $content -match 'body.*background-color' }
        "articlebody" { return $content -match 'class="article-body"' }
        "gradient" { return $content -match 'gradient' }
        "copyright" { return $content -match '&copy;|©|copyright|Copyright' }
    }
    return $false
}

foreach ($site in $siteConfigs) {
    $files = Get-ChildItem -Path $site.Path -Filter "*.html" -Recurse -File | Where-Object { $_.Name -notmatch '^template' -and $_.Name -ne 'template.html' }
    Write-Host "=== Scanning $($site.Name): $($files.Count) files ===" -ForegroundColor Cyan
    
    foreach ($file in $files) {
        $content = Get-Content $file.FullName -Raw -Encoding UTF8
        $issues = @()
        
        # === STRUCTURAL CHECKS ===
        
        # Header (nav element or header tag)
        if (-not (Test-HasElement $content "header")) {
            $issues += "HEADER_MISSING"
        }
        
        # Nav
        if (-not (Test-HasElement $content "nav")) {
            $issues += "NAV_MISSING"
        }
        
        # Breadcrumb
        if (-not (Test-HasElement $content "breadcrumb")) {
            $issues += "BREADCRUMB_MISSING"
        }
        
        # Sidebar
        if (-not (Test-HasElement $content "sidebar")) {
            $issues += "SIDEBAR_MISSING"
        }
        
        # Related articles
        if (-not (Test-HasElement $content "related")) {
            $issues += "RELATED_MISSING"
        }
        
        # Footer
        if (-not (Test-HasElement $content "footer")) {
            $issues += "FOOTER_MISSING"
        } elseif (-not (Test-HasElement $content "copyright")) {
            $issues += "FOOTER_NO_COPYRIGHT"
        }
        
        # Baidu analytics (only morai and novelpick)
        if ($site.NeedBaidu -and -not (Test-HasElement $content "baidu")) {
            $issues += "BAIDU_MISSING"
        }
        
        # === CONTENT QUALITY ===
        
        # Article body content length (only for files with article-body)
        if (Test-HasElement $content "articlebody") {
            $bodyMatch = [regex]::Match($content, 'class="article-body"[^>]*>([\s\S]{100,})</div>\s*<div class="related')
            if ($bodyMatch.Success) {
                $bodyText = $bodyMatch.Groups[1].Value -replace '<[^>]+>', ''
                if ($bodyText.Length -lt 200) {
                    $issues += "BODY_CONTENT_SHORT:$($bodyText.Length)"
                }
            }
        }
        
        # SEO meta tags
        if (-not (Test-HasElement $content "ogtitle")) { $issues += "OG_TITLE_MISSING" }
        if (-not (Test-HasElement $content "ogdesc")) { $issues += "OG_DESC_MISSING" }
        if (-not (Test-HasElement $content "canonical")) { $issues += "CANONICAL_MISSING" }
        
        # === LAYOUT CHECKS ===
        
        # Viewport
        if (-not (Test-HasElement $content "viewport")) {
            $issues += "VIEWPORT_MISSING"
        }
        
        # Responsive CSS
        if (-not (Test-HasElement $content "media")) {
            $issues += "RESPONSIVE_MISSING"
        }
        
        $status = if ($issues.Count -eq 0) { "PASS" } else { "FAIL" }
        $results += @{
            Site = $site.Name
            File = $file.Name
            Status = $status
            Issues = $issues
        }
        
        if ($status -eq "FAIL") {
            Write-Host "  FAIL: $($file.Name)" -ForegroundColor Yellow
            foreach ($issue in $issues) {
                Write-Host "    - $issue" -ForegroundColor Red
            }
        }
    }
}

# Summary
Write-Host ""
Write-Host "=== AUDIT SUMMARY ===" -ForegroundColor Cyan
$passCount = ($results | Where-Object { $_.Status -eq "PASS" }).Count
$failCount = ($results | Where-Object { $_.Status -eq "FAIL" }).Count
Write-Host "Total: $($results.Count) | PASS: $passCount | FAIL: $failCount" -ForegroundColor White

if ($failCount -gt 0) {
    Write-Host ""
    Write-Host "=== FAILED PAGES ===" -ForegroundColor Yellow
    $results | Where-Object { $_.Status -eq "FAIL" } | ForEach-Object {
        Write-Host "Site: $($_.Site) | File: $($_.File)" -ForegroundColor Red
        Write-Host "  Issues: $($_.Issues -join ', ')" -ForegroundColor Red
        Write-Host ""
    }
} else {
    Write-Host ""
    Write-Host "All pages passed inspection!" -ForegroundColor Green
}

# Export to JSON
$logDir = "C:\Users\Administrator\.openclaw\workspace\logs"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }
$results | ConvertTo-Json -Depth 10 | Out-File "$logDir\audit-results-$(Get-Date -Format 'yyyyMMdd').json" -Encoding UTF8
Write-Host ""
Write-Host "Full results saved to logs\audit-results-$(Get-Date -Format 'yyyyMMdd').json"