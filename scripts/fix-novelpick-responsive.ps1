$pages = @(
    "C:\Users\Administrator\.openclaw\workspace\novelpick-website\fantasy.html",
    "C:\Users\Administrator\.openclaw\workspace\novelpick-website\litrpg.html",
    "C:\Users\Administrator\.openclaw\workspace\novelpick-website\reviews.html",
    "C:\Users\Administrator\.openclaw\workspace\novelpick-website\romance.html",
    "C:\Users\Administrator\.openclaw\workspace\novelpick-website\scifi.html"
)

$mediaBlock = "@media(max-width:900px){.article-layout{grid-template-columns:1fr}.sidebar{display:none}}"

foreach ($file in $pages) {
    $content = Get-Content $file -Raw
    
    # Check if @media already exists
    if ($content -match '@media\(max-width:900px\)') {
        Write-Host "[SKIP] $file already has @media 900px"
        continue
    }
    
    # Find the </style> tag and insert @media before it
    if ($content -match '(</style>)') {
        $newContent = $content -replace '(</style>)', "$mediaBlock`$1"
        Set-Content -Path $file -Value $newContent -NoNewline
        Write-Host "[FIXED] $file - added @media 900px"
    }
}
