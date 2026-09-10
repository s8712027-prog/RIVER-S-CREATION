param(
    [string]$Input = "data/incoming/DEMO-B20260824-001.csv",
    [string]$CoilId = "DEMO-B20260824-001"
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
python curve_os_cli.py --input $Input --coil-id $CoilId
Write-Host "啟動本機儀表板：http://127.0.0.1:8765"
python app.py
