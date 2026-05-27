# Website Quality Audit Script - ASCII safe version
$results = @()
$siteConfigs = @(
    @{
        Name = "morai"
        Path = "C:\Users\Administrator\github\morai-website"
        NeedBaidu = $true
    },
    @{
        Name = "novelpick"
        Path = "C:\Users\Administrator\github\novelpick-website"
        NeedBaidu = $true
    },
    @{
        Name = "fateandmethod"
        Path = "C:\Users\Administrator\github\fateandmethod-site"
        NeedBaidu = $false
    }
)

foreach ($site in $siteConfigs) {
    $files = Get-ChildItem -Path $site.Path -Filter "*.html" -Recurse -File
    Write-Host "=== Scanning $($site.Name): $($files.Count) files ===" -ForegroundColor Cyan
    
    foreach ($file in $files) {
        $content = Get-Content $file.FullName -Raw -Encoding UTF8
        $issues = @()
        
        # 1. Structural checks
        
        # header with dark gradient
        if ($content -notmatch '<header[^>]*class=[" ''][^" '']*header[^" '']*[" '']' -and $content -notmatch '<header') {
            $issues += "[HEADER_MISSING]"
        } elseif ($content -notmatch 'background.*gradient|gradient.*background') {
            $issues += "[HEADER_NO_GRADIENT]"
        }
        
        # nav navigation
        if ($content -notmatch '<nav[^>]*>') {
            $issues += "[NAV_MISSING]"
        } elseif ($content -match '<nav[^>]*>\s*</nav>' -or $content -notmatch '<nav[^>]*>[\s\S]{10,}</nav>') {
            $issues += "[NAV_EMPTY]"
        }
        
        # breadcrumb
        if ($content -notmatch 'breadcrumb') {
            $issues += "[BREADCRUMB_MISSING]"
        }
        
        # sidebar
        if ($content -notmatch 'sidebar') {
            $issues += "[SIDEBAR_MISSING]"
        } elseif ($content -match 'sidebar[^>]*>\s*</aside>' -or $content -match 'sidebar[^>]*>\s*</div>') {
            $issues += "[SIDEBAR_EMPTY]"
        }
        
        # related articles
        if ($content -notmatch 'related') {
            $issues += "[RELATED_MISSING]"
        } elseif ($content -match 'related[^>]*>\s*</div>') {
            $issues += "[RELATED_EMPTY]"
        }
        
        # footer
        if ($content -notmatch '<footer') {
            $issues += "[FOOTER_MISSING]"
        } elseif ($content -notmatch 'copyright|Copyright') {
            $issues += "[FOOTER_NO_COPYRIGHT]"
        }
        
        # Baidu analytics (only morai and novelpick)
        if ($site.NeedBaidu -and $content -notmatch 'hm\.baidu\.com') {
            $issues += "[BAIDU_MISSING]"
        }
        
        # 2. Content quality
        
        # article body length
        $bodyMatch = [regex]::Match($content, '<div[^>]*id=["'']article-body["''][^>]*>([\s\S]{200,})</div>')
        if (-not $bodyMatch.Success) {
            $issues += "[BODY_TOO_SHORT]"
        } else {
            $bodyText = $bodyMatch.Groups[1].Value -replace '<[^>]+>', ''
            if ($bodyText.Length -lt 200) {
                $issues += "[BODY_CONTENT_SHORT:$($bodyText.Length)]"
            }
        }
        
        # SEO meta tags
        if ($content -notmatch 'og:title') { $issues += "[OG_TITLE_MISSING]" }
        if ($content -notmatch 'og:description') { $issues += "[OG_DESC_MISSING]" }
        if ($content -notmatch 'canonical') { $issues += "[CANONICAL_MISSING]" }
        
        # 3. Layout checks
        
        # CSS background-color on body
        if ($content -notmatch 'body[^}]*\{[^}]*background') {
            $issues += "[BODY_NO_BG_COLOR]"
        }
        
        # viewport meta
        if ($content -notmatch 'viewport') {
            $issues += "[VIEWPORT_MISSING]"
        }
        
        # responsive CSS
        if ($content -notmatch '@media') {
            $issues += "[RESPONSIVE_MISSING]"
        }
        
        # div nesting balance inside article-body
        $abMatch = [regex]::Match($content, '<div[^>]*id=["'']article-body["''][^>]*>')
        if ($abMatch.Success) {
            $startPos = $abMatch.Index + $abMatch.Length
            $remaining = $content.Substring($startPos)
            $openDivs = (($remaining | Select-String -Pattern '<div[^>]*>' -AllMatches).Matches).Count
            $closeDivs = (($remaining | Select-String -Pattern '</div>' -AllMatches).Matches).Count
            if ($openDivs -ne $closeDivs) {
                $issues += "[DIV_NEST_UNBALANCED:$openDivs/$closeDivs]"
            }
        }
        
        $status = if ($issues.Count -eq 0) { "PASS" } else { "FAIL" }
        $results += @{
            Site = $site.Name
            File = $file.Name
            Path = $file.FullName
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
        Write-Host "Site: $($_.Site)" -ForegroundColor Red
        Write-Host "File: $($_.File)" -ForegroundColor Red
        Write-Host "Issues: $($_.Issues -join ', ')" -ForegroundColor Red
        Write-Host ""
    }
}

# Export to JSON
$logDir = "C:\Users\Administrator\.openclaw\workspace\logs"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }
$results | ConvertTo-Json -Depth 10 | Out-File "$logDir\audit-results-$(Get-Date -Format 'yyyyMMdd').json" -Encoding UTF8
Write-Host "Full results saved to logs\audit-results-$(Get-Date -Format 'yyyyMMdd').json"