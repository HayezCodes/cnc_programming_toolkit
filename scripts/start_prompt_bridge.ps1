param(
    [string]$ConfigPath = ".\bridge.config.json"
)

$ErrorActionPreference = "SilentlyContinue"

function Load-Config {
    if (Test-Path $ConfigPath) {
        return Get-Content $ConfigPath | ConvertFrom-Json
    }
    return $null
}

function Open-VSCode {
    code .
}

function Open-File {
    param($file)
    code $file
}

function Get-LatestPrompt($folder) {
    Get-ChildItem $folder -Recurse -File | 
    Sort-Object LastWriteTime -Descending | 
    Select-Object -First 1
}

$config = Load-Config
$seen = @{}

Write-Host "Universal Bridge Running..."

while ($true) {

    git pull

    $latest = Get-LatestPrompt $config.prompt_folder

    if ($latest -and -not $seen[$latest.FullName]) {

        $content = Get-Content $latest.FullName -Raw

        Write-Host "`n==== NEW PROMPT ====" -ForegroundColor Cyan
        Write-Host $content
        Write-Host "====================`n"

        if ($config.copy_to_clipboard) {
            Set-Clipboard $content
        }

        if ($config.auto_open_vscode) {
            Open-VSCode
        }

        if ($config.auto_open_prompt_file) {
            Open-File $latest.FullName
        }

        $seen[$latest.FullName] = $true
    }

    Start-Sleep -Seconds $config.poll_seconds
}
