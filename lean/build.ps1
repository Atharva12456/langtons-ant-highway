param(
    [string]$Lake = $env:LANGTON_LEAN_LAKE
)

$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($Lake)) {
    $portable = Join-Path $PSScriptRoot '..\lean_toolchain\.elan\bin\lake.exe'
    if (Test-Path -LiteralPath $portable) {
        $Lake = (Resolve-Path -LiteralPath $portable).Path
    } else {
        $command = Get-Command lake -ErrorAction SilentlyContinue
        if ($null -eq $command) {
            throw 'lake was not found. Install the pinned Lean toolchain or set LANGTON_LEAN_LAKE to lake.exe.'
        }
        $Lake = $command.Source
    }
}

Push-Location $PSScriptRoot
try {
    & $Lake build
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    & $Lake env lean (Join-Path $PSScriptRoot 'Audit.lean')
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally {
    Pop-Location
}
exit 0
