$html = Get-Content 'C:\Users\Administrator\github\novelpick-website\litrpg.html' -Raw

# More precise: find first article-body opening and trace divs from there
$startIdx = $html.IndexOf('<div class="article-body"')
if ($startIdx -eq -1) { Write-Output "No article-body found"; exit }

$slice = $html.Substring($startIdx)

$open = ([regex]::Matches($slice, '<div\b')).Count
$close = ([regex]::Matches($slice, '</div>')).Count
Write-Output "In article-body slice: open=$open close=$close diff=$($close - $open)"

# Also check the original file had this issue
$lines = Get-Content 'C:\Users\Administrator\github\novelpick-website\litrpg.html'
$totalOpen = ([regex]::Matches($html, '<div\b')).Count
$totalClose = ([regex]::Matches($html, '</div>')).Count
Write-Output "Total HTML: open=$totalOpen close=$totalClose diff=$($totalClose - $totalOpen)"