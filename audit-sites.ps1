# 每日站点巡检脚本
$ErrorActionPreference = "SilentlyContinue"
$results = @()

$dirs = @{
    'morai'         = 'C:\Users\Administrator\github\morai-website'
    'novelpick'     = 'C:\Users\Administrator\github\novelpick-website'
    'fateandmethod' = 'C:\Users\Administrator\github\fateandmethod-site'
}

function Test-HtmlStructure {
    param([string]$path, [string]$site)

    $content = Get-Content $path -Raw -Encoding UTF8
    $filename = Split-Path $path -Leaf

    $issues = @()

    # 1. 结构性检查
    # header深色渐变
    if ($content -notmatch '(?s)<header[^>]*\s+style=["\'][^"\']*(?:background|gradient|linear)[^"\']*dark|black|#0|#1|#2') {
        $issues += "[header渐变缺失]"
    }

    # nav存在
    if ($content -notmatch '<nav[^>]*>') {
        $issues += "[nav缺失]"
    }

    # 面包屑
    if ($content -notmatch 'breadcrumb') {
        $issues += "[面包屑缺失]"
    }

    # 侧边栏
    if ($content -notmatch '<aside|sidebar') {
        $issues += "[侧边栏缺失]"
    }

    # 相关文章
    if ($content -notmatch 'related|相关文章|推荐阅读') {
        $issues += "[相关文章缺失]"
    }

    # footer
    if ($content -notmatch '<footer') {
        $issues += "[footer缺失]"
    }

    # 百度统计 (morai/novelpick)
    if ($site -ne 'fateandmethod' -and $content -notmatch 'hm\.baidu\.com') {
        $issues += "[百度统计缺失]"
    }

    # 2. 内容质量检查
    # 文章正文长度
    $bodyMatch = [regex]::Match($content, '(?s)<div[^>]*id=["\']article-body["\'][^>]*>(.+)</div>')
    if ($bodyMatch.Success) {
        $textLen = $bodyMatch.Groups[1].Value.Replace('<',' ').Replace('>',' ').Length
        if ($textLen -lt 200) { $issues += "[内容过短:${textLen}字符]" }
    } else {
        # 试article-body div嵌套平衡检查
        $abMatch = [regex]::Match($content, '(?s)<div[^>]*class=["\'][^"\']*article-body[^"\']*["\'][^>]*>')
        if ($abMatch.Success) {
            # 检查div平衡
            $inner = $content.Substring($abMatch.Index)
            $openCount = ([regex]::Matches($inner, '<div[^>]*>') ).Count
            $closeCount = ([regex]::Matches($inner, '</div>') ).Count
            # article-body自身算1个open
            if ($openCount -ne $closeCount) { $issues += "[div嵌套不平衡:open=$openCount close=$closeCount]" }
        }
    }

    # SEO meta
    if ($content -notmatch 'og:title' -or $content -notmatch 'og:description') {
        $issues += "[SEO meta缺失]"
    }
    if ($content -notmatch 'canonical') {
        $issues += "[canonical缺失]"
    }

    # 阅读时间
    if ($content -notmatch '阅读|分钟|min|read') {
        $issues += "[阅读时间估算缺失]"
    }

    # 3. 布局检查
    # CSS背景色
    if ($content -notmatch 'background[- ]color') {
        $issues += "[CSS背景色缺失]"
    }

    # viewport
    if ($content -notmatch 'viewport') {
        $issues += "[viewport缺失]"
    }

    # 响应式
    if ($content -notmatch '@media') {
        $issues += "[响应式CSS缺失]"
    }

    return $issues
}

$total = 0; $ok = 0; $bad = 0
$problemPages = @()

foreach ($site in $dirs.Keys) {
    $htmlFiles = @(Get-ChildItem $dirs[$site] -Filter "*.html" -Recurse -File)
    foreach ($f in $htmlFiles) {
        $total++
        $issues = Test-HtmlStructure -path $f.FullName -site $site
        if ($issues.Count -eq 0) {
            $ok++
        } else {
            $bad++
            $relPath = $f.FullName.Replace($dirs[$site], '').TrimStart('\')
            $problemPages += [PSCustomObject]@{
                Site = $site
                File = $relPath
                Issues = ($issues -join ' ')
            }
        }
    }
}

# 输出报告
Write-Host "=== 每日站点巡检报告 $(Get-Date -Format 'yyyy-MM-dd HH:mm') ==="
Write-Host ""
Write-Host "### 统计"
Write-Host "- 总页面数: $total"
Write-Host "- 正常: $ok 个"
Write-Host "- 有问题: $bad 个"
Write-Host ""

if ($problemPages.Count -gt 0) {
    Write-Host "### ⚠️ 有问题的页面"
    foreach ($p in $problemPages) {
        Write-Host "- [$($p.Site)] $($p.File)"
        Write-Host "  问题类型: $($p.Issues)"
    }
} else {
    Write-Host "### ✅ 正常页面"
    Write-Host "今日巡检完成，无异常"
}