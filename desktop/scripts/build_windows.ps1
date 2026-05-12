param(
  [string]$Python = "py",
  [string]$Name = "HarInspector"
)

$ErrorActionPreference = "Stop"

& $Python -m pip install -U pip
& $Python -m pip install -e ".[build]"

& $Python -m PyInstaller -y --clean --noconsole --onefile `
  --name $Name `
  --collect-submodules customtkinter `
  har_inspector_desktop/__main__.py

Write-Host "Built: dist/$Name.exe"

