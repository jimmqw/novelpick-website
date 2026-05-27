$footer = @"
<footer>
<a href="/">Fate & Method</a> | <a href="/ziwei.html">Zi Wei</a> | <a href="/liuyao.html">Liu Yao</a> | <a href="/bazi.html">Ba Zi</a> | <a href="/daily-wisdom.html">Daily Wisdom</a>
<p style="margin-top:0.5rem">© 2026 FateAndMethod.com — Explore Eastern Metaphysics</p>
</footer>
"@

$f = "C:\Users\Administrator\github\fateandmethod-site\index.html"
$content = Get-Content $f -Raw -Encoding UTF8
$newContent = $content -replace '(\s*)(</body>)', "`$1$footer`$1`$2"
Set-Content -Path $f -Value $newContent -Encoding UTF8 -NoNewline
Write-Host "Done"
