# Find fateandmethod repo location
Write-Host "Searching for fateandmethod..."
Write-Host ""

# Check github folder
$githubDir = "C:\Users\Administrator\github"
if (Test-Path $githubDir) {
  Write-Host "GitHub repos:"
  Get-ChildItem $githubDir -Directory | ForEach-Object { Write-Host "  $($_.Name)" }
}

Write-Host ""

# Search for directories with 'fate' or 'method' in name
Write-Host "Searching in C:\Users\Administrator..."
Get-ChildItem C:\Users\Administrator -Directory -Filter "*fate*" -Depth 1 -ErrorAction SilentlyContinue | ForEach-Object { 
  Write-Host "  FOUND: $($_.FullName)" 
}
Get-ChildItem C:\Users\Administrator -Directory -Filter "*method*" -Depth 1 -ErrorAction SilentlyContinue | ForEach-Object { 
  Write-Host "  FOUND: $($_.FullName)" 
}

# Also search in Documents, Desktop etc
foreach ($dir in @("Documents", "Desktop", "Downloads")) {
  $p = Join-Path $env:USERPROFILE $dir
  if (Test-Path $p) {
    Get-ChildItem $p -Directory -Filter "*fate*" -Depth 2 -ErrorAction SilentlyContinue | ForEach-Object { 
      Write-Host "  FOUND in ${dir}: $($_.FullName)" 
    }
  }
}
