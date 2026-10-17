param(
  [Parameter(Mandatory = $true)][string]$Python,
  [Parameter(Mandatory = $true)][string]$Analyzer,
  [string]$GitHubConfig,
  [string]$EncryptedToken
)

$ErrorActionPreference = 'Stop'
$collector = Join-Path $PSScriptRoot 'collect.py'
$failed = $false
try {
  & $Python $collector codex --analyzer $Analyzer
  if ($LASTEXITCODE -ne 0) { $failed = $true }
  if ($GitHubConfig) {
    if ($EncryptedToken) {
      $tokenPath = [IO.Path]::GetFullPath($EncryptedToken)
      $repoPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../..')) + [IO.Path]::DirectorySeparatorChar
      if ($tokenPath.StartsWith($repoPath, [StringComparison]::OrdinalIgnoreCase)) { throw 'Private token must be outside checkout' }
      $secureToken = Get-Content -LiteralPath $tokenPath -Raw | ConvertTo-SecureString
      $tokenPtr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureToken)
      try {
        $env:ACTIVITY_READ_TOKEN = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($tokenPtr)
      } finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($tokenPtr)
      }
    }
    & $Python $collector github --config $GitHubConfig
    if ($LASTEXITCODE -ne 0) { $failed = $true }
  }
} catch {
  [Console]::Error.WriteLine('Local activity update failed; inspect private setup without sharing raw logs.')
  $failed = $true
} finally {
  Remove-Item Env:ACTIVITY_READ_TOKEN -ErrorAction SilentlyContinue
}
if ($failed) { exit 1 }
exit 0
