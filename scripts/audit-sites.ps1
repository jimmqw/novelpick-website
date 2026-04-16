# Site Audit Script - 2026-04-15
$ErrorActionPreference = "Continue"

function Test-HTMLFile {
    param([string]$Path, [string]$SiteName)

    $issues = @()
    $content = Get-Content $Path -Raw -Encoding UTF8

    $filename = Split-Path $Path -Leaf

    # 1. Structural checks
    if ($content -notmatch '<header[^>]*>.*?</header>' -and $content -notmatch '<header[^>]*>') {
        # check for header tag
        if ($content -notmatch '<header') { $issues += "header缺失" }
    }
    # header gradient check
    if ($content -match '<header[^>]*style=["\'][^"\']*gradient' -or $content -match '<style[^>]*header[^>]*gradient' -or $content -match 'header\s*\{[^}]*background[^}]*gradient') {
        # ok
    } elseif ($content -match '<header') {
        # header exists but no gradient detected
        $issues += "header无渐变背景"
    }

    if ($content -notmatch '<nav[^>]*>.*?</nav>' -and $content -notmatch '<nav') { $issues += "nav缺失" }
    if ($content -notmatch 'breadcrumb') { $issues += "面包屑缺失" }
    if ($content -notmatch '<aside|<div[^>]*id=["\']?sidebar') { $issues += "侧边栏缺失" }
    if ($content -notmatch 'footer.*copyright|footer.*©' -and $content -notmatch '<footer') { $issues += "footer缺失" }

    # 2. Baidu stats (morai + novelpick only)
    if ($SiteName -in @("morai","novelpick")) {
        if ($content -notmatch 'hm\.baidu\.com|hm\.js') { $issues += "百度统计缺失" }
    }

    # 3. Content quality
    $articleBody = [regex]::Match($content, '<div[^>]*id=["\']?article-body["\']?[^>]*>(.*?)</div>', [System.Text.RegularExpressions.RegexOptions]::Singleline)
    if ($articleBody.Success) {
        $textLen = $articleBody.Value -replace '<[^>]+>', '' | Measure-Object -Character
        if ($textLen.Characters -lt 200) { $issues += "内容过短($($textLen.Characters)字符)" }
    } else {
        # check if it's an article page
        if ($filename -match '^best-|^ai-|^books-|^shadow-|^solo-|^claude|^cursor|^chatgpt|^how-|^best-' -and $filename -notmatch 'index|search|deals|template') {
            $issues += "未找到article-body区块"
        }
    }

    # SEO meta
    if ($content -notmatch 'og:title') { $issues += "og:title缺失" }
    if ($content -notmatch 'og:description|description.*content=') { $issues += "description缺失" }
    if ($content -notmatch 'canonical') { $issues += "canonical缺失" }

    # 4. Layout
    if ($content -notmatch 'viewport') { $issues += "viewport缺失" }
    if ($content -notmatch '@media') { $issues += "无响应式CSS" }

    # div nesting balance for article-body
    if ($articleBody.Success) {
        $openCount = ([regex]::Matches($articleBody.Value, '<div[^>]*>')).Count
        $closeCount = ([regex]::Matches($articleBody.Value, '</div>')).Count
        if ($openCount -ne $closeCount) { $issues += "div嵌套不平衡(open=$openCount close=$closeCount)" }
    }

    return @{Path=$Path; Filename=$filename; Site=$SiteName; Issues=$issues}
}

# Sites to audit
$sites = @(
    @{Path="C:\Users\Administrator\github\morai-website"; Name="morai"; HasBaidu=$true},
    @{Path="C:\Users\Administrator\github\novelpick-website"; Name="novelpick"; HasBaidu=$true},
    @{Path="C:\Users\Administrator\github\fateandmethod-site"; Name="fateandmethod"; HasBaidu=$false}
)

$allResults = @()
foreach ($site in $sites) {
    $files = Get-ChildItem "$($site.Path)\*.html" -File
    foreach ($file in $files) {
        $result = Test-HTMLFile -Path $file.FullName -SiteName $site.Name
        $allResults += $result
    }
}

# Output
$problemFiles = $allResults | Where-Object { $_.Issues.Count -gt 0 }
$normalFiles = $allResults | Where-Object { $_.Issues.Count -eq 0 }

Write-Host "=== AUDIT RESULTS ===" 
Write-Host "Total: $($allResults.Count) pages | Normal: $($normalFiles.Count) | Problems: $($problemFiles.Count)"
Write-Host ""

if ($problemFiles.Count -gt 0) {
    Write-Host "### PROBLEM PAGES ###"
    foreach ($p in $problemFiles) {
        Write-Host "FILE: $($p.Filename) [$($p.Site)]"
        foreach ($issue in $p.Issues) {
            Write-Host "  - $issue"
        }
        Write-Host ""
    }
} else {
    Write-Host "All pages OK!"
}

Write-Host ""
Write-Host "### NORMAL FILES ###"
foreach ($n in $normalFiles) {
    Write-Host "  $($n.Filename) [$($n.Site)]"
}
