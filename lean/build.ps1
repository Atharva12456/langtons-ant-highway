$ErrorActionPreference = 'Stop'
$toolRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\lean_toolchain')).Path
$env:ELAN_HOME = Join-Path $toolRoot '.elan'
$lake = Join-Path $env:ELAN_HOME 'bin\lake.exe'
Push-Location $PSScriptRoot
try {
    & $lake build
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    & $lake env lean (Join-Path $PSScriptRoot 'Audit.lean')
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally {
    Pop-Location
}
exit 0
