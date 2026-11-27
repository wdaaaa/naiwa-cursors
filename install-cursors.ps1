$ErrorActionPreference = "Stop"
$schemeName = "NaiwaCursors"
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$installDir = Join-Path $env:LOCALAPPDATA "Microsoft\Windows\Cursors\NaiwaCursors"
New-Item -ItemType Directory -Force -Path $installDir | Out-Null
Copy-Item -Path (Join-Path $scriptRoot "*.cur") -Destination $installDir -Force
$cursorMap = [ordered]@{
    "Arrow" = "normal_select.cur"
    "Help" = "help_select.cur"
    "AppStarting" = "working_in_background.cur"
    "Wait" = "busy.cur"
    "Crosshair" = "precision_select.cur"
    "IBeam" = "text_select.cur"
    "NWPen" = "handwriting.cur"
    "No" = "unavailable.cur"
    "SizeNS" = "vertical_resize.cur"
    "SizeWE" = "horizontal_resize.cur"
    "SizeNWSE" = "diagonal_resize_nwse.cur"
    "SizeNESW" = "diagonal_resize_nesw.cur"
    "SizeAll" = "move.cur"
    "UpArrow" = "alternate_select.cur"
    "Hand" = "link_select.cur"
    "Pin" = "location_select.cur"
    "Person" = "person_select.cur"
}
$cursorKey = "HKCU:\Control Panel\Cursors"
Set-ItemProperty -Path $cursorKey -Name "(default)" -Value $schemeName
foreach ($entry in $cursorMap.GetEnumerator()) {
    Set-ItemProperty -Path $cursorKey -Name $entry.Key -Value (Join-Path $installDir $entry.Value)
}
$schemeKey = Join-Path $cursorKey "Schemes"
New-Item -Path $schemeKey -Force | Out-Null
Set-ItemProperty -Path $schemeKey -Name $schemeName -Value (($cursorMap.Values | ForEach-Object { Join-Path $installDir $_ }) -join ",")
Add-Type @"
using System; using System.Runtime.InteropServices;
public static class CursorRefresh { [DllImport("user32.dll")] public static extern bool SystemParametersInfo(int a,int b,string c,int d); }
"@
[CursorRefresh]::SystemParametersInfo(0x0057, 0, $null, 0x03) | Out-Null
Write-Host "Installed cursor scheme: $schemeName"
