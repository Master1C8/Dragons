param(
    [Parameter(Mandatory = $true)][string]$BaseDirectory,
    [Parameter(Mandatory = $true)][string]$RuntimeCode,
    [Parameter(Mandatory = $true)][string]$StatusFile,
    [string]$GamePath,
    [string]$SteamRootOverride,
    [string]$StateRootOverride
)

$ErrorActionPreference = 'Stop'
$ExpectedAppId = '4739660'
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Write-Status([string]$Kind, [string]$Message) {
    [System.IO.File]::WriteAllText($StatusFile, "$Kind`n$Message", $Utf8NoBom)
}

function Get-Sha256([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return $null }
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Get-VdfValue([string]$Text, [string]$Name) {
    $match = [regex]::Match($Text, '"' + [regex]::Escape($Name) + '"\s+"([^"]*)"', 'IgnoreCase')
    if (-not $match.Success) { return $null }
    return $match.Groups[1].Value
}

function Get-SafePath([string]$Root, [string]$Relative) {
    $normalized = $Relative.Replace('/', '\')
    if ([string]::IsNullOrWhiteSpace($normalized) -or $normalized.Contains(':') -or [System.IO.Path]::IsPathRooted($normalized)) {
        throw "Unsafe path in the localization package: $Relative"
    }
    foreach ($part in $normalized.Split('\')) {
        if ([string]::IsNullOrEmpty($part) -or $part -eq '.' -or $part -eq '..') {
            throw "Unsafe path in the localization package: $Relative"
        }
    }
    $rootFull = [System.IO.Path]::GetFullPath($Root).TrimEnd('\')
    $result = [System.IO.Path]::GetFullPath((Join-Path $rootFull $normalized))
    if (-not $result.StartsWith($rootFull + '\', [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Unsafe path in the localization package: $Relative"
    }
    $cursor = $rootFull
    foreach ($part in @('') + $normalized.Split('\')) {
        if ($part) { $cursor = Join-Path $cursor $part }
        $entry = Get-Item -LiteralPath $cursor -Force -ErrorAction SilentlyContinue
        if ($entry -and ($entry.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
            throw "Refusing a link in the installation path: $cursor"
        }
    }
    return $result
}

function Get-InstallationStateRoot($Installation, [string]$Override) {
    if (-not [string]::IsNullOrWhiteSpace($Override)) {
        return [System.IO.Path]::GetFullPath($Override)
    }
    return Get-SafePath $Installation.GameRoot '.vn-revival/dragons'
}

function Resolve-GameRoot([string]$InstallRoot) {
    $candidates = @($InstallRoot, (Join-Path $InstallRoot 'DragNWash'), (Join-Path $InstallRoot 'game'))
    foreach ($candidate in $candidates) {
        $exe = Join-Path $candidate 'DragNWash.exe'
        $data = Join-Path $candidate 'DragNWash_Data'
        if ((Test-Path -LiteralPath $exe -PathType Leaf) -and (Test-Path -LiteralPath $data -PathType Container)) {
            return [pscustomobject]@{ GameRoot = $candidate; DataRoot = $data; Executable = $exe }
        }
    }
    return $null
}

function Get-SteamRoots([string]$Override) {
    $roots = New-Object System.Collections.Generic.List[string]
    if (-not [string]::IsNullOrWhiteSpace($Override)) {
        $roots.Add(([System.IO.Path]::GetFullPath($Override)))
    }
    foreach ($entry in @(
        @{ Path = 'HKCU:\Software\Valve\Steam'; Name = 'SteamPath' },
        @{ Path = 'HKLM:\SOFTWARE\WOW6432Node\Valve\Steam'; Name = 'InstallPath' },
        @{ Path = 'HKLM:\SOFTWARE\Valve\Steam'; Name = 'InstallPath' }
    )) {
        try {
            $value = (Get-ItemProperty -LiteralPath $entry.Path -Name $entry.Name -ErrorAction Stop).($entry.Name)
            if ($value) { $roots.Add(([System.IO.Path]::GetFullPath($value.Replace('/', '\')))) }
        } catch { }
    }
    foreach ($root in @($roots)) {
        $libraries = Join-Path $root 'steamapps\libraryfolders.vdf'
        if (-not (Test-Path -LiteralPath $libraries -PathType Leaf)) { continue }
        $text = [System.IO.File]::ReadAllText($libraries)
        foreach ($match in [regex]::Matches($text, '"path"\s+"([^"]+)"', 'IgnoreCase')) {
            $roots.Add(([System.IO.Path]::GetFullPath($match.Groups[1].Value.Replace('\\', '\'))))
        }
    }
    return @($roots | Select-Object -Unique)
}

function Test-GameAnchors($Game, $Anchors) {
    foreach ($anchor in $Anchors.PSObject.Properties) {
        if ((Get-Sha256 (Join-Path $Game.DataRoot $anchor.Name)) -ne [string]$anchor.Value) { return $false }
    }
    return $true
}

function Find-GameInstallation([string]$SelectedPath, $Anchors, [string[]]$SearchRoots) {
    if ($SelectedPath -and (Test-Path -LiteralPath $SelectedPath -PathType Leaf)) {
        if ([IO.Path]::GetFileName($SelectedPath) -ne 'DragNWash.exe') { throw 'Select DragNWash.exe.' }
        $SelectedPath = Split-Path -Parent $SelectedPath
    }
    foreach ($steamRoot in Get-SteamRoots $SteamRootOverride) {
        $manifestPath = Join-Path $steamRoot "steamapps\appmanifest_$ExpectedAppId.acf"
        if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) { continue }
        $manifestText = [System.IO.File]::ReadAllText($manifestPath)
        $appId = Get-VdfValue $manifestText 'appid'
        $installDir = Get-VdfValue $manifestText 'installdir'
        $buildId = Get-VdfValue $manifestText 'buildid'
        if ($appId -ne $ExpectedAppId -or [string]::IsNullOrWhiteSpace($installDir) -or [string]::IsNullOrWhiteSpace($buildId)) { continue }
        $installRoot = Join-Path $steamRoot ("steamapps\common\" + $installDir)
        $resolved = Resolve-GameRoot $installRoot
        if ($null -eq $resolved) { continue }
        if ([string]::IsNullOrWhiteSpace($SelectedPath) -and -not (Test-GameAnchors $resolved $Anchors)) { continue }
        if (-not [string]::IsNullOrWhiteSpace($SelectedPath)) {
            $selected = [System.IO.Path]::GetFullPath($SelectedPath).TrimEnd('\')
            $allowed = @(
                [System.IO.Path]::GetFullPath($installRoot).TrimEnd('\'),
                [System.IO.Path]::GetFullPath($resolved.GameRoot).TrimEnd('\'),
                [System.IO.Path]::GetFullPath($resolved.DataRoot).TrimEnd('\')
            )
            if (-not ($allowed | Where-Object { $_.Equals($selected, [System.StringComparison]::OrdinalIgnoreCase) })) { continue }
        }
        return [pscustomobject]@{
            SteamRoot = $steamRoot
            ManifestPath = $manifestPath
            BuildId = $buildId
            InstallRoot = $installRoot
            GameRoot = $resolved.GameRoot
            DataRoot = $resolved.DataRoot
            Executable = $resolved.Executable
        }
    }
    if (-not [string]::IsNullOrWhiteSpace($SelectedPath)) {
        $resolved = Resolve-GameRoot ([IO.Path]::GetFullPath($SelectedPath))
        if ($null -ne $resolved) {
            return [pscustomobject]@{
                ManifestPath = $null; BuildId = 'content-pinned'
                GameRoot = $resolved.GameRoot; DataRoot = $resolved.DataRoot; Executable = $resolved.Executable
            }
        }
        throw 'Select a DragNWash game folder containing the executable.'
    }
    if ($null -eq $SearchRoots) {
        $SearchRoots = @([IO.DriveInfo]::GetDrives() | Where-Object {
            $_.IsReady -and $_.DriveType -in @('Fixed','Removable')
        } | ForEach-Object { $_.RootDirectory.FullName })
    }
    $pending = New-Object 'System.Collections.Generic.Queue[string]'
    foreach ($root in $SearchRoots) { $pending.Enqueue($root) }
    $timer = [Diagnostics.Stopwatch]::StartNew()
    while ($pending.Count -gt 0 -and $timer.Elapsed.TotalSeconds -lt 15) {
        $directory = $pending.Dequeue()
        $exe = Join-Path $directory 'DragNWash.exe'
        if (Test-Path -LiteralPath $exe -PathType Leaf) {
            $resolved = Resolve-GameRoot $directory
            if ($null -ne $resolved -and (Test-GameAnchors $resolved $Anchors)) {
                return [pscustomobject]@{
                    ManifestPath = $null; BuildId = 'content-pinned'
                    GameRoot = $resolved.GameRoot; DataRoot = $resolved.DataRoot; Executable = $resolved.Executable
                }
            }
        }
        foreach ($child in (Get-ChildItem -LiteralPath $directory -Directory -ErrorAction SilentlyContinue)) {
            if (-not ($child.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
                $pending.Enqueue($child.FullName)
            }
        }
    }
    throw 'No compatible copy of Drag’N Wash was found. Select DragNWash.exe.'
}

function Write-JsonFile($Value, [string]$Path) {
    $parent = Split-Path -Parent $Path
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
    [System.IO.File]::WriteAllText($Path, (($Value | ConvertTo-Json -Depth 12) + "`n"), $Utf8NoBom)
}

function Read-Receipt([string]$Path, [string]$PackageId) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return $null }
    $receipt = [System.IO.File]::ReadAllText($Path) | ConvertFrom-Json
    if ([int]$receipt.schemaVersion -ne 1 -or [string]$receipt.packageID -ne $PackageId) {
        throw 'The previous VN Revival installation data could not be verified.'
    }
    return $receipt
}

function Recover-Transaction([string]$StateRoot, [string]$DataRoot, [string]$ReceiptPath) {
    $transaction = Join-Path $StateRoot 'transaction'
    if (-not (Test-Path -LiteralPath $transaction -PathType Container)) { return }
    $statePath = Join-Path $transaction 'state.json'
    if (-not (Test-Path -LiteralPath $statePath -PathType Leaf)) {
        Remove-Item -LiteralPath $transaction -Recurse -Force
        return
    }
    $state = [System.IO.File]::ReadAllText($statePath) | ConvertFrom-Json
    if ([int]$state.schemaVersion -ne 1) { throw 'The interrupted installation record is malformed.' }
    if (-not [bool]$state.committed) {
        foreach ($file in @($state.files)) {
            $destination = Get-SafePath $DataRoot ([string]$file.path)
            $rollback = Get-SafePath (Join-Path $transaction 'rollback') ([string]$file.path)
            if (Test-Path -LiteralPath $rollback -PathType Leaf) {
                New-Item -ItemType Directory -Path (Split-Path -Parent $destination) -Force | Out-Null
                Copy-Item -LiteralPath $rollback -Destination $destination -Force
            } elseif (-not [bool]$file.originalExisted -and (Test-Path -LiteralPath $destination -PathType Leaf)) {
                Remove-Item -LiteralPath $destination -Force
            }
        }
        $previousReceipt = Join-Path $transaction 'previous-receipt.json'
        if ([bool]$state.previousReceiptExisted) {
            if (-not (Test-Path -LiteralPath $previousReceipt -PathType Leaf)) {
                throw 'The interrupted installation is missing its previous receipt.'
            }
            Copy-Item -LiteralPath $previousReceipt -Destination $ReceiptPath -Force
        } elseif (Test-Path -LiteralPath $ReceiptPath -PathType Leaf) {
            Remove-Item -LiteralPath $ReceiptPath -Force
        }
    }
    Remove-Item -LiteralPath $transaction -Recurse -Force
}

function Validate-Artifact([string]$PayloadRoot, $Artifact, [string]$Owner) {
    $path = Get-SafePath $PayloadRoot ([string]$Artifact.path)
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "A payload file is missing: $Owner" }
    if ((Get-Sha256 $path) -ne ([string]$Artifact.sha256).ToLowerInvariant()) {
        throw "A payload checksum does not match: $Owner"
    }
    return $path
}

function Stage-PayloadFile($Item, [string]$PayloadRoot, [string]$BackupRoot, [string]$Output, [string]$Transaction) {
    $artifacts = @($Item.artifacts)
    if ($null -eq $Item.artifacts -or $artifacts.Count -eq 0) {
        $payloadRelative = if ([string]::IsNullOrWhiteSpace([string]$Item.payloadPath)) { [string]$Item.path } else { [string]$Item.payloadPath }
        $source = Get-SafePath $PayloadRoot $payloadRelative
        Copy-Item -LiteralPath $source -Destination $Output
        return
    }
    $tool = Join-Path $PayloadRoot 'Tools\xdelta3.exe'
    if (-not (Test-Path -LiteralPath $tool -PathType Leaf)) { throw 'The xdelta3 payload tool is missing.' }
    $source = Get-SafePath $BackupRoot ([string]$Item.path)
    $intermediates = @()
    try {
        for ($index = 0; $index -lt $artifacts.Count; $index++) {
            $patch = Get-SafePath $PayloadRoot ([string]$artifacts[$index].path)
            if ($index -eq $artifacts.Count - 1) {
                $target = $Output
            } else {
                $target = Join-Path $Transaction ("delta-" + [guid]::NewGuid().ToString('N'))
                $intermediates += $target
            }
            & $tool -d -f -s $source $patch $target | Out-Null
            if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $target -PathType Leaf)) {
                throw "The localized file could not be reconstructed: $($Item.path)"
            }
            $source = $target
        }
    } finally {
        foreach ($path in $intermediates) { Remove-Item -LiteralPath $path -Force -ErrorAction SilentlyContinue }
    }
}

try {
    Write-Status 'WORKING' 'Finding Drag’N Wash…'
    $configPath = Join-Path $BaseDirectory 'Resources\PackageConfig.json'
    $payloadRoot = Join-Path $BaseDirectory 'Resources\LocalizationPayload'
    if (-not (Test-Path -LiteralPath $configPath -PathType Leaf)) { throw 'PackageConfig.json is missing.' }
    $config = [System.IO.File]::ReadAllText($configPath) | ConvertFrom-Json
    if ([int]$config.schemaVersion -ne 2 -or [string]$config.steamAppID -ne $ExpectedAppId) {
        throw 'The localization package configuration is invalid.'
    }
    $languages = @($config.languages | Where-Object { $null -ne $_ })
    if (-not [bool]$config.payloadReady -or $languages.Count -eq 0 -or
        @($languages | Where-Object { -not $_.ready -or -not $_.siteLocale -or -not $_.runtimeCode }).Count -ne 0 -or
        @($languages | Group-Object siteLocale | Where-Object Count -gt 1).Count -ne 0 -or
        @($languages | Group-Object runtimeCode | Where-Object Count -gt 1).Count -ne 0) {
        throw 'The localization package is incomplete or has duplicate locale codes.'
    }
    $sharedFiles = @($config.files | Where-Object { $null -ne $_ })
    $selected = @($config.languages | Where-Object { [string]$_.runtimeCode -eq $RuntimeCode })
    if ($selected.Count -ne 1 -or -not [bool]$selected[0].ready) {
        throw "The selected language is not ready: $RuntimeCode"
    }
    $selected = $selected[0]
    $selectedFiles = @($sharedFiles + @($selected.files))
    if ($selectedFiles.Count -eq 0) { throw 'The selected language payload is empty.' }
    $duplicatePaths = @($selectedFiles | Group-Object path | Where-Object { $_.Count -ne 1 })
    if ($duplicatePaths.Count -ne 0) { throw 'The localization package contains duplicate destination paths.' }

    $installation = Find-GameInstallation $GamePath $config.anchors
    $running = Get-Process -ErrorAction SilentlyContinue | Where-Object {
        try { $_.Path -and $_.Path.StartsWith($installation.GameRoot + '\', [System.StringComparison]::OrdinalIgnoreCase) }
        catch { $false }
    }
    if ($running) { throw 'The game is running. Close it before installing a localization.' }

    foreach ($name in @('globalgamemanagers','globalgamemanagers.assets')) {
        if ([string]::IsNullOrEmpty($config.anchors.$name) -or
            (Get-Sha256 (Get-SafePath $installation.DataRoot $name)) -ne $config.anchors.$name) {
            throw "The selected game version does not match: $name"
        }
    }
    Write-Status 'WORKING' 'Verifying the localization package…'
    $tool = Join-Path $payloadRoot 'Tools\xdelta3.exe'
    $buildManifestPath = Join-Path $payloadRoot 'BuildManifest.json'
    if (-not (Test-Path -LiteralPath $buildManifestPath -PathType Leaf)) { throw 'The payload build manifest is missing.' }
    $buildManifest = [System.IO.File]::ReadAllText($buildManifestPath) | ConvertFrom-Json
    if ((Get-Sha256 $tool) -ne ([string]$config.deltaToolSHA256).ToLowerInvariant() -or
        $config.deltaToolSHA256 -ne $buildManifest.deltaTool.sha256) {
        throw 'The xdelta3 payload tool failed its integrity check.'
    }
    foreach ($item in $selectedFiles) {
        if ($null -ne $item.artifacts) {
            foreach ($artifact in @($item.artifacts)) { [void](Validate-Artifact $payloadRoot $artifact ([string]$item.path)) }
        } else {
            $payloadRelative = if ([string]::IsNullOrWhiteSpace([string]$item.payloadPath)) { [string]$item.path } else { [string]$item.payloadPath }
            $artifact = [pscustomobject]@{ path = $payloadRelative; sha256 = [string]$item.artifactSHA256 }
            [void](Validate-Artifact $payloadRoot $artifact ([string]$item.path))
        }
    }

    $stateRoot = Get-InstallationStateRoot $installation $StateRootOverride
    $backupRoot = Join-Path $stateRoot 'original-backup'
    $receiptPath = Join-Path $stateRoot 'receipt.json'
    New-Item -ItemType Directory -Path $stateRoot -Force | Out-Null
    $null = Get-SafePath $stateRoot 'installer.lock'
    $installationLock = [IO.File]::Open((Join-Path $stateRoot 'installer.lock'), 'OpenOrCreate', 'ReadWrite', 'None')
    Recover-Transaction $stateRoot $installation.DataRoot $receiptPath

    $previousReceipt = Read-Receipt $receiptPath ([string]$config.packageID)
    $steamBuildChanged = if ($null -ne $previousReceipt) {
        [string]$previousReceipt.steamBuildID -ne [string]$installation.BuildId
    } else {
        [string]$installation.BuildId -ne [string]$config.steamBuildID
    }

    New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null
    $receiptFiles = @()
    foreach ($item in $selectedFiles) {
        $relative = [string]$item.path
        $destination = Get-SafePath $installation.DataRoot $relative
        $originalHash = if ([string]::IsNullOrWhiteSpace([string]$item.originalSHA256)) { $null } else { ([string]$item.originalSHA256).ToLowerInvariant() }
        $payloadHash = ([string]$item.payloadSHA256).ToLowerInvariant()
        $currentHash = Get-Sha256 $destination
        $prior = @()
        if ($null -ne $previousReceipt) { $prior = @($previousReceipt.files | Where-Object { [string]$_.path -eq $relative }) }
        if ($prior.Count -gt 1) { throw "The previous receipt contains a duplicate path: $relative" }
        if ($prior.Count -eq 1) {
            $restoredOriginal = $null -ne $originalHash -and $currentHash -eq $originalHash
            $missingOwnedAddition = $null -eq $currentHash -and -not [bool]$prior[0].originalExisted -and $null -eq $originalHash
            if ($currentHash -ne ([string]$prior[0].installedSHA256).ToLowerInvariant() -and
                $currentHash -ne $payloadHash -and -not $restoredOriginal -and -not $missingOwnedAddition) {
                if ($steamBuildChanged) { throw "Steam build $($installation.BuildId) changed a required game file: $relative" }
                throw "The file was modified by another patch: $relative"
            }
        } elseif ($null -ne $originalHash) {
            if ($null -eq $currentHash) { throw "A required game file is missing: $relative" }
            if ($currentHash -ne $originalHash) {
                if ($steamBuildChanged) { throw "Steam build $($installation.BuildId) changed a required game file: $relative" }
                throw "The game file version is unsupported: $relative"
            }
        } elseif ($null -ne $currentHash) {
            throw "The file belongs to another patch: $relative"
        }
        if ($null -ne $originalHash) {
            $backup = Get-SafePath $backupRoot $relative
            if (Test-Path -LiteralPath $backup -PathType Leaf) {
                if ((Get-Sha256 $backup) -ne $originalHash) { throw "The original-file backup is damaged: $relative" }
            } else {
                if ($currentHash -ne $originalHash) { throw "The original-file backup is unavailable: $relative" }
                New-Item -ItemType Directory -Path (Split-Path -Parent $backup) -Force | Out-Null
                Copy-Item -LiteralPath $destination -Destination $backup
                if ((Get-Sha256 $backup) -ne $originalHash) { throw "The original-file backup could not be verified: $relative" }
            }
        }
        $receiptFiles += [pscustomobject]@{
            path = $relative
            originalExisted = ($null -ne $originalHash)
            originalSHA256 = $originalHash
            installedSHA256 = $payloadHash
        }
    }

    $activePaths = @{}
    foreach ($item in $selectedFiles) { $activePaths[[string]$item.path] = $true }
    $retiredFiles = @()
    if ($null -ne $previousReceipt) {
        $retiredFiles = @($previousReceipt.files | Where-Object { -not $activePaths.ContainsKey([string]$_.path) })
    }
    foreach ($prior in $retiredFiles) {
        $relative = [string]$prior.path
        $destination = Get-SafePath $installation.DataRoot $relative
        $currentHash = Get-Sha256 $destination
        if ($null -ne $currentHash -and $currentHash -ne ([string]$prior.installedSHA256).ToLowerInvariant()) {
            throw "A retired localization file was modified by another patch: $relative"
        }
        if ($null -eq $currentHash -and [bool]$prior.originalExisted) {
            throw "A previously owned game file is missing: $relative"
        }
        if ([bool]$prior.originalExisted) {
            $backup = Get-SafePath $backupRoot $relative
            if ((Get-Sha256 $backup) -ne ([string]$prior.originalSHA256).ToLowerInvariant()) {
                throw "The original-file backup is damaged: $relative"
            }
        }
    }

    Write-Status 'WORKING' 'Reconstructing the selected language…'
    $transaction = Join-Path $stateRoot 'transaction'
    if (Test-Path -LiteralPath $transaction) { Remove-Item -LiteralPath $transaction -Recurse -Force }
    $rollbackRoot = Join-Path $transaction 'rollback'
    $stageRoot = Join-Path $transaction 'staged'
    New-Item -ItemType Directory -Path $rollbackRoot -Force | Out-Null
    New-Item -ItemType Directory -Path $stageRoot -Force | Out-Null
    $transactionFiles = @($receiptFiles) + @($retiredFiles)
    foreach ($file in $transactionFiles) {
        $destination = Get-SafePath $installation.DataRoot ([string]$file.path)
        if (Test-Path -LiteralPath $destination -PathType Leaf) {
            $rollback = Get-SafePath $rollbackRoot ([string]$file.path)
            New-Item -ItemType Directory -Path (Split-Path -Parent $rollback) -Force | Out-Null
            Copy-Item -LiteralPath $destination -Destination $rollback
        }
    }
    $previousReceiptExisted = Test-Path -LiteralPath $receiptPath -PathType Leaf
    if ($previousReceiptExisted) { Copy-Item -LiteralPath $receiptPath -Destination (Join-Path $transaction 'previous-receipt.json') }
    foreach ($item in $selectedFiles) {
        $stage = Get-SafePath $stageRoot ([string]$item.path)
        New-Item -ItemType Directory -Path (Split-Path -Parent $stage) -Force | Out-Null
        Stage-PayloadFile $item $payloadRoot $backupRoot $stage $transaction
        if ((Get-Sha256 $stage) -ne ([string]$item.payloadSHA256).ToLowerInvariant()) {
            throw "The reconstructed file checksum does not match: $($item.path)"
        }
    }
    $state = [pscustomobject]@{
        schemaVersion = 1
        packageID = [string]$config.packageID
        committed = $false
        previousReceiptExisted = [bool]$previousReceiptExisted
        files = $transactionFiles
    }
    Write-JsonFile $state (Join-Path $transaction 'state.json')

    try {
        Write-Status 'WORKING' 'Installing the selected language…'
        foreach ($item in $selectedFiles) {
            $destination = Get-SafePath $installation.DataRoot ([string]$item.path)
            $stage = Get-SafePath $stageRoot ([string]$item.path)
            New-Item -ItemType Directory -Path (Split-Path -Parent $destination) -Force | Out-Null
            Move-Item -LiteralPath $stage -Destination $destination -Force
            if ((Get-Sha256 $destination) -ne ([string]$item.payloadSHA256).ToLowerInvariant()) {
                throw "Installed-file verification failed: $($item.path)"
            }
        }
        foreach ($prior in $retiredFiles) {
            $destination = Get-SafePath $installation.DataRoot ([string]$prior.path)
            if ([bool]$prior.originalExisted) {
                Copy-Item -LiteralPath (Get-SafePath $backupRoot ([string]$prior.path)) -Destination $destination -Force
            } elseif (Test-Path -LiteralPath $destination -PathType Leaf) {
                Remove-Item -LiteralPath $destination -Force
            }
        }
        $receipt = [pscustomobject]@{
            schemaVersion = 1
            packageID = [string]$config.packageID
            steamBuildID = [string]$installation.BuildId
            installedAt = [DateTime]::UtcNow.ToString('o')
            activeLanguage = [pscustomobject]@{
                siteLocale = [string]$selected.siteLocale
                runtimeCode = [string]$selected.runtimeCode
            }
            files = $receiptFiles
        }
        Write-JsonFile $receipt $receiptPath
        $state.committed = $true
        Write-JsonFile $state (Join-Path $transaction 'state.json')
        Remove-Item -LiteralPath $transaction -Recurse -Force
    } catch {
        Recover-Transaction $stateRoot $installation.DataRoot $receiptPath
        throw
    }

    $launch = if ($installation.ManifestPath) { 'steam://rungameid/4739660' } else { $installation.Executable }
    Write-Status 'SUCCESS' $launch
    exit 0
} catch {
    try { Write-Status 'ERROR' $_.Exception.Message } catch { }
    exit 1
}
