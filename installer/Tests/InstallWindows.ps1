param([string]$Shared, [string]$Distribution)
$ErrorActionPreference = 'Stop'
$root = Join-Path $env:TEMP ('DragonsInstallerTest-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $root | Out-Null
$archive = Join-Path $root 'win-fixture.zip'
& robocopy.exe $Shared $root win-fixture.zip /J /R:0 /W:0 /NFL /NDL /NP | Out-Null
if ($LASTEXITCODE -ge 8) { throw 'Could not copy test fixture' }
$game = Join-Path $root 'fake-game'
New-Item -ItemType Directory -Path $game | Out-Null
tar.exe -xf $archive -C $game
if ($LASTEXITCODE -ne 0) { throw 'Could not extract test fixture' }
$dist = Join-Path $root 'installer'
& robocopy.exe $Distribution $dist /E /J /R:0 /W:0 /NFL /NDL /NP | Out-Null
if ($LASTEXITCODE -ge 8) { throw 'Could not copy installer' }
$config = Get-Content -Raw -LiteralPath (Join-Path $dist 'Resources\PackageConfig.json') | ConvertFrom-Json
$script = Join-Path $dist 'install.ps1'
$status = Join-Path $root 'status.txt'
$receiptPath = Join-Path $game '.vn-revival\dragons\receipt.json'
function Digest([string]$Path) { return (Get-FileHash -LiteralPath $Path).Hash.ToLowerInvariant() }
function Install([string]$Locale) {
    & powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File $script -BaseDirectory $dist -RuntimeCode $Locale -StatusFile $status -GamePath $game
}
foreach ($locale in @('ar','th','th','he','fa','hi')) {
    Install $locale
    $result = Get-Content -Raw -LiteralPath $status
    if ($LASTEXITCODE -ne 0 -or !$result.StartsWith("SUCCESS`n")) { throw $result }
    if ((Get-Content -Raw -LiteralPath $result.Substring(8)) -cne 'test only') {
        throw 'Launch target does not match the isolated test executable'
    }
    $receipt = Get-Content -Raw -LiteralPath $receiptPath | ConvertFrom-Json
    if ($receipt.activeLanguage.siteLocale -ne $locale) { throw 'Locale did not persist' }
    $selected = $config.languages | Where-Object { $_.siteLocale -eq $locale }
    foreach ($item in $selected.files) {
       if ((Digest (Join-Path $game ('DragNWash_Data\' + $item.path))) -ne $item.payloadSHA256) {
           throw ('Installed payload differs: ' + $item.path)
       }
    }
    if ((Get-Content -Raw -LiteralPath (Join-Path $game 'DragNWash_Data\ForeignMod.txt')) -cne 'preserve this unrelated test file') {
        throw 'Foreign mod changed'
    }
    Write-Output ('verified install and persisted locale: ' + $locale)
}
$victim = Join-Path $game 'DragNWash_Data\Managed\Unity.TextMeshPro.dll'
[IO.File]::AppendAllText($victim,'external test edit')
$before = Digest $victim
Install 'fa'
$result = Get-Content -Raw -LiteralPath $status
if ($LASTEXITCODE -eq 0 -or $result -notmatch 'modified|another mod|changed' -or $before -ne (Digest $victim)) { throw $result }
Write-Output 'conflicting managed file preserved'
