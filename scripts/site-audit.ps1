# Site Audit Script - Daily Health Check
$ErrorActionPreference = "SilentlyContinue"
$results = @()
$issues = @()

$sites = @(
    @{Path="C:\Users\Administrator\github\morai-website"; Name="morai.top"; CheckBaidu=$true},
    @{Path="C:\Users\Administrator\github\novelpick-website"; Name="novelpick.top"; CheckBaidu=$true},
    @{Path="C:\Users\Administrator\github\fateandmethod-site"; Name="fateandmethod.com"; CheckBaidu=$false}
)

foreach ($site in $sites) {
    $htmlFiles = Get-ChildItem $site.Path -Filter "*.html" -Recurse
    Write-Host "[$($site.Name)] Scanning $($htmlFiles.Count) files..."

    foreach ($file in $htmlFiles) {
        $content = Get-Content $file.FullName -Raw
        $relPath = $file.FullName.Replace($site.Path + "\", "")
        $fileIssues = @()

        # 1. Structural checks
        $hasHeader = $content -match '<header[^>]*class="[^"]*header[^"]*"[^>]*>.*?</header>' -or $content -match '<header[^>]*>.*?background.*?</header>'
        $headerGradient = $content -match 'background.*:(linear-gradient|gradient)'
        $hasNav = $content -match '<nav[^>]*>.*?</nav>'
        $hasBreadcrumb = $content -match 'breadcrumb' -or $content -match 'breadcrumbs'
        $hasSidebar = $content -match '<aside[^>]*class="[^"]*sidebar[^"]*".*?</aside>' -or $content -match 'sidebar'
        $hasRelatedArticles = $content -match 'related.*article' -or $content -match 'recommended.*post'
        $hasFooter = $content -match '<footer[^>]*>.*?</footer>'
        $hasBaidu = $content -match 'hm\.baidu\.com'

        if ($site.CheckBaidu -and -not $hasBaidu) {
            $fileIssues += "百度统计缺失"
        }

        # 2. Content quality checks
        $ogTitle = $content -match 'og:title'
        $ogDesc = $content -match 'og:description'
        $canonical = $content -match 'canonical'
        $hasReadTime = $content -match 'read.*time|分钟阅读|阅读时间'

        # Article body length
        $articleMatch = [regex]::Match($content, '<article[^>]*class="[^"]*article-body[^"]*"[^>]*>(.*?)</article>', [System.Text.RegularExpressions.RegexOptions]::Singleline)
        if ($articleMatch.Success) {
            $articleText = $articleMatch.Groups[1].Value -replace '<[^>]+>', ''
            $articleLen = $articleText.Length
        } else {
            # Try body class
            $bodyMatch = [regex]::Match($content, '<div[^>]*class="[^"]*article-body[^"]*"[^>]*>(.*?)</article>', [System.Text.RegularExpressions.RegexOptions]::Singleline)
            if ($bodyMatch.Success) {
                $articleText = $bodyMatch.Groups[1].Value -replace '<[^>]+>', ''
                $articleLen = $articleText.Length
            } else {
                $articleLen = 0
            }
        }

        if ($articleLen -lt 200) {
            $fileIssues += "内容过短(${articleLen}字符)"
        }

        # 3. Layout checks
        $hasViewport = $content -match 'viewport'
        $hasMediaQuery = $content -match '@media'
        $hasBodyBg = $content -match 'body.*background-color' -or $content -match 'background-color.*body'

        # Div nesting balance check
        $openDivs = ([regex]::Matches($content, '<div')).Count
        $closeDivs = ([regex]::Matches($content, '</div>')).Count
        $divBalanced = $openDivs -eq $closeDivs

        if (-not $divBalanced) {
            $fileIssues += "div嵌套不平衡(开$openDivs/关$closeDivs)"
        }

        # Sidebar content check
        $sidebarMatch = [regex]::Match($content, '<aside[^>]*class="[^"]*sidebar[^"]*"[^>]*>(.*?)</aside>', [System.Text.RegularExpressions.RegexOptions]::Singleline)
        if (-not $sidebarMatch.Success) {
            $sidebarMatch = [regex]::Match($content, '<div[^>]*class="[^"]*sidebar[^"]*"[^>]*>(.*?)</div>', [System.Text.RegularExpressions.RegexOptions]::Singleline)
        }
        if ($sidebarMatch.Success) {
            $sidebarText = $sidebarMatch.Groups[1].Value -replace '<[^>]+>', '' -replace '\s+', ''
            if ($sidebarText.Length -lt 20) {
                $fileIssues += "侧边栏内容空"
            }
        }

        # Record results
        $result = [ordered]@{
            Site = $site.Name
            File = $relPath
            Header = $hasHeader
            HeaderGradient = $headerGradient
            Nav = $hasNav
            Breadcrumb = $hasBreadcrumb
            Sidebar = $hasSidebar
            RelatedArticles = $hasRelatedArticles
            Footer = $hasFooter
            BaiduStats = $hasBaidu
            ArticleLen = $articleLen
            SEO_OGTitle = $ogTitle
            SEO_OGDesc = $ogDesc
            Canonical = $canonical
            ReadTime = $hasReadTime
            Viewport = $hasViewport
            MediaQuery = $hasMediaQuery
            BodyBg = $hasBodyBg
            DivBalance = $divBalanced
            OpenDiv = $openDivs
            CloseDiv = $closeDivs
            Issues = $fileIssues -join "; "
            Status = if ($fileIssues.Count -eq 0) { "OK" } else { "ISSUE" }
        }
        $results += $result

        if ($fileIssues.Count -gt 0) {
            $issues += $result
        }
    }
}

# Output summary
Write-Host "`n========== AUDIT SUMMARY =========="
Write-Host "Total files scanned: $($results.Count)"
Write-Host "OK: $($results | Where-Object { $_.Status -eq 'OK' }).Count"
Write-Host "Issues: $($issues.Count)"

if ($issues.Count -gt 0) {
    Write-Host "`n========== ISSUES =========="
    foreach ($issue in $issues) {
        Write-Host "$($issue.Site) | $($issue.File) | $($issue.Issues)"
    }
}

# Export CSV
$results | Export-Csv -Path "$env:TEMP\site_audit_$((Get-Date).ToString('yyyyMMdd')).csv" -NoTypeInformation -Encoding UTF8
Write-Host "`nFull report: $env:TEMP\site_audit_$((Get-Date).ToString('yyyyMMdd')).csv"