param(
    [string]$ConfigPath
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $PSCommandPath
$repoRoot = Split-Path -Parent $scriptDir
$repoName = Split-Path -Leaf $repoRoot

if ([string]::IsNullOrWhiteSpace($ConfigPath)) {
    $ConfigPath = Join-Path $repoRoot "bridge.config.json"
} elseif (-not [System.IO.Path]::IsPathRooted($ConfigPath)) {
    $ConfigPath = Join-Path (Get-Location) $ConfigPath
}

$ConfigPath = [System.IO.Path]::GetFullPath($ConfigPath)

$stateRoot = if (-not [string]::IsNullOrWhiteSpace($env:LOCALAPPDATA)) {
    Join-Path $env:LOCALAPPDATA "UniversalPromptBridge"
} elseif (-not [string]::IsNullOrWhiteSpace($env:TEMP)) {
    Join-Path $env:TEMP "UniversalPromptBridge"
} else {
    $scriptDir
}

if (-not (Test-Path -LiteralPath $stateRoot)) {
    New-Item -ItemType Directory -Path $stateRoot -Force | Out-Null
}

$statePath = Join-Path $stateRoot "$repoName.processed.json"

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

function Load-Config {
    param([string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        throw "Bridge config not found: $Path"
    }

    return Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json
}

function Load-ProcessedState {
    param([string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        return @{}
    }

    try {
        $state = Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json
        $processed = @{}

        foreach ($entry in @($state.processed)) {
            if (-not [string]::IsNullOrWhiteSpace($entry)) {
                $processed[$entry] = $true
            }
        }

        return $processed
    } catch {
        return @{}
    }
}

function Save-ProcessedState {
    param(
        [string]$Path,
        [hashtable]$Processed
    )

    $payload = @{
        processed = @($Processed.Keys | Sort-Object)
    }

    $payload | ConvertTo-Json | Set-Content -LiteralPath $Path -Encoding UTF8
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

    return Get-ChildItem -LiteralPath $Folder -Recurse -File |
        Where-Object { $_.Name -notmatch "example" } |
        Sort-Object LastWriteTimeUtc, FullName -Descending |
        Select-Object -First 1
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

$config = Load-Config -Path $ConfigPath
$configRoot = Split-Path -Parent $ConfigPath
$promptFolder = Resolve-BridgePath -BasePath $configRoot -Path $config.prompt_folder
$processed = Load-ProcessedState -Path $statePath
$pollSeconds = [int]$config.poll_seconds

while ($true) {
    Invoke-GitPull -RepoRoot $repoRoot

    $latest = Get-LatestPrompt -Folder $promptFolder

    if ($latest) {
        $promptKey = $latest.FullName.ToLowerInvariant()

        if (-not $processed.ContainsKey($promptKey)) {
            $content = Get-Content -LiteralPath $latest.FullName -Raw

            Write-Host "NEW PROMPT: $($latest.Name)" -ForegroundColor Cyan
            Write-Host $content

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
                Open-File -Path $latest.FullName
            }

            $processed[$promptKey] = $true
            Save-ProcessedState -Path $statePath -Processed $processed
        }
    }

    Start-Sleep -Seconds $pollSeconds
}
