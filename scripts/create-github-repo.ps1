param(
  [string]$RepoName = "socialmnger",
  [string]$Visibility = "public"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
  throw "GitHub CLI (gh) kurulu değil. Önce https://cli.github.com/ adresinden kur."
}

gh auth status

if ($Visibility -eq "private") {
  gh repo create $RepoName --private --source=. --remote=origin --push
} else {
  gh repo create $RepoName --public --source=. --remote=origin --push
}

Write-Host "GitHub repo oluşturuldu ve push edildi: $RepoName"
