Get-ChildItem C:\Users\Administrator -Directory -Force -ErrorAction SilentlyContinue | ForEach-Object {
  $_.FullName
}
