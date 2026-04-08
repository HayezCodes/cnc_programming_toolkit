param(
    [string]$ConfigPath
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $PSCommandPath
$repoRoot = Split-Path -Parent $scriptDir

function Write-ConfigErrorAndExit {
    param([string]$Message)

    Write-Host "[config error] $Message" -ForegroundColor Red
    exit 1
}

function Resolve-BridgePath {
    param(
        [Parameter(Mandatory = $true)][string]$BasePath,
        [Parameter(Mandatory = $true)][string]$Path
    )

    if ([System.IO.Path]::IsPathRooted($Path)) {
        return [System.IO.Path]::GetFullPath($Path)
    }

    return [System.IO.Path]::GetFullPath((Join-Path $BasePath $Path))
}

function Get-ConfigPath {
    param([string]$RequestedPath)

    if ([string]::IsNullOrWhiteSpace($RequestedPath)) {
        return Join-Path $repoRoot "bridge.config.json"
    }

    if ([System.IO.Path]::IsPathRooted($RequestedPath)) {
        return [System.IO.Path]::GetFullPath($RequestedPath)
    }

    return [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $RequestedPath))
}

function Load-Config {
    param([string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        Write-ConfigErrorAndExit "Missing bridge config: $Path"
    }

    try {
        $config = Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json
    } catch {
        Write-ConfigErrorAndExit "Invalid JSON in bridge config: $Path"
    }

    if ($null -eq $config) {
        Write-ConfigErrorAndExit "Bridge config is empty: $Path"
    }

    if ($null -eq $config.poll_seconds -or [int]$config.poll_seconds -lt 1) {
        Write-ConfigErrorAndExit "bridge.config.json must define poll_seconds as an integer greater than 0."
    }

    if ([string]::IsNullOrWhiteSpace($config.prompt_folder)) {
        Write-ConfigErrorAndExit "bridge.config.json must define prompt_folder."
    }

    return $config
}

function Ensure-Directory {
    param([string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
    }
}

function Open-VSCode {
    param([string]$Path)

    try {
        & code $Path *> $null
    } catch {
    }
}

function Open-File {
    param([string]$Path)

    try {
        & code $Path *> $null
    } catch {
    }
}

function Get-LatestPrompt {
    param([string]$Folder)

    if (-not (Test-Path -LiteralPath $Folder)) {
        return $null
    }

    return Get-ChildItem -LiteralPath $Folder -File |
        Where-Object { $_.Name -notmatch "example|sample|test" } |
        Sort-Object LastWriteTimeUtc, FullName -Descending |
        Select-Object -First 1
}

function Get-UniqueDestinationPath {
    param(
        [string]$Folder,
        [string]$FileName
    )

    $candidate = Join-Path $Folder $FileName

    if (-not (Test-Path -LiteralPath $candidate)) {
        return $candidate
    }

    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($FileName)
    $extension = [System.IO.Path]::GetExtension($FileName)
    $counter = 1

    do {
        $candidate = Join-Path $Folder ("{0}_{1}{2}" -f $baseName, $counter, $extension)
        $counter++
    } while (Test-Path -LiteralPath $candidate)

    return $candidate
}

function Invoke-GitPull {
    param([string]$RepoRoot)

    $output = & git -C $RepoRoot pull --ff-only --quiet 2>&1
    $exitCode = $LASTEXITCODE

    if ($exitCode -ne 0) {
        $message = ($output | Out-String).Trim()
        if ([string]::IsNullOrWhiteSpace($message)) {
            $message = "git pull failed with exit code $exitCode."
        }

        Write-Host "[git error] $message" -ForegroundColor Red
    }
}

$resolvedConfigPath = Get-ConfigPath -RequestedPath $ConfigPath
$config = Load-Config -Path $resolvedConfigPath
$configRoot = Split-Path -Parent $resolvedConfigPath
$promptFolder = Resolve-BridgePath -BasePath $configRoot -Path $config.prompt_folder
$doneFolder = Join-Path (Split-Path -Parent $promptFolder) "done"
$processed = @{}
$pollSeconds = [int]$config.poll_seconds

Ensure-Directory -Path $promptFolder
Ensure-Directory -Path $doneFolder

while ($true) {
    Invoke-GitPull -RepoRoot $repoRoot

    $latestPrompt = Get-LatestPrompt -Folder $promptFolder

    if ($latestPrompt) {
        $promptKey = "{0}|{1}|{2}" -f $latestPrompt.FullName.ToLowerInvariant(), $latestPrompt.LastWriteTimeUtc.Ticks, $latestPrompt.Length

        if (-not $processed.ContainsKey($promptKey)) {
            $content = Get-Content -LiteralPath $latestPrompt.FullName -Raw
            $donePath = Get-UniqueDestinationPath -Folder $doneFolder -FileName $latestPrompt.Name

            Move-Item -LiteralPath $latestPrompt.FullName -Destination $donePath

            Write-Host "===== NEW PROMPT: $($latestPrompt.Name) =====" -ForegroundColor Cyan
            Write-Host $content
            Write-Host "===== MOVED TO: $donePath =====" -ForegroundColor Cyan

            if ($config.copy_to_clipboard) {
                try {
                    Set-Clipboard -Value $content
                } catch {
                }
            }

            if ($config.auto_open_vscode) {
                Open-VSCode -Path $repoRoot
            }

            if ($config.auto_open_prompt_file) {
                Open-File -Path $donePath
            }

            $processed[$promptKey] = $true
        }
    }

    Start-Sleep -Seconds $pollSeconds
}
