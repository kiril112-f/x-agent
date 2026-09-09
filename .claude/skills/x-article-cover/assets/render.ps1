<#
  Рендер обложки X Article в точный PNG через Chrome headless.

  Пример:
    .\render.ps1 -Kicker "THE UNDER-18 PLAYBOOK" -Hero "*$70K* Before 18" `
                 -Obj ".\covers\under18\object.png" -Out ".\covers\under18\cover.png"

  В -Hero:  "|" = перенос строки,  *звёздочки* = акцентный цвет.
#>
param(
  [Parameter(Mandatory = $true)][string]$Hero,
  [string]$Kicker = "",
  [ValidateSet('cobalt', 'graphite', 'violet', 'teal')][string]$Field = 'cobalt',
  [ValidateSet('l1', 'l2', 'l3', 'l4')][string]$Layout = 'l1',
  [string[]]$Obj = @(),
  [int]$ObjW = 0,
  [int]$ObjY = 0,
  [int]$ObjX = -60,
  [int]$HeroPx = 0,
  [string]$Mark = '@KirillMorozovop',
  [string]$Out = ".\cover.png",
  [int]$Scale = 2
)

$ErrorActionPreference = 'Stop'

$chrome = @(
  "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
  "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
  "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $chrome) { throw "Chrome не найден. Укажи путь вручную в render.ps1." }

# 1536x512 — ровно 3:1, обе стороны кратны 16: тот же размер, что gpt-image-2.5 отдаёт нативно
$W = 1536
$H = if ($Layout -eq 'l4') { 640 } else { 512 }

$tpl = Join-Path $PSScriptRoot 'cover.html'
if (-not (Test-Path $tpl)) { throw "Не найден шаблон: $tpl" }

$qs = [System.Collections.Generic.List[string]]::new()
function Add-Param($k, $v) {
  if ($null -ne $v -and "$v" -ne "") { $script:qs.Add("$k=" + [uri]::EscapeDataString("$v")) }
}
Add-Param 'hero'    $Hero
Add-Param 'kicker'  $Kicker
Add-Param 'field'   $Field
Add-Param 'layout'  $Layout
Add-Param 'mark'    $Mark
Add-Param 'w'       $W
Add-Param 'h'       $H
if ($HeroPx -gt 0) { Add-Param 'hero_px' $HeroPx }
if ($ObjW  -gt 0)  { Add-Param 'objw'    $ObjW }
if ($ObjY  -ne 0)  { Add-Param 'objy'    $ObjY }
Add-Param 'objx' $ObjX
if ($Obj.Count -gt 0) {
  $urls = $Obj | ForEach-Object { "file:///" + ((Resolve-Path $_).Path -replace '\\', '/') }
  Add-Param 'obj' ($urls -join ',')
}

$url = "file:///" + ($tpl -replace '\\', '/') + "?" + ($qs -join '&')

$outAbs = if ([IO.Path]::IsPathRooted($Out)) { $Out }
          else { [IO.Path]::GetFullPath((Join-Path (Get-Location).Path $Out)) }
$outDir = Split-Path -Parent $outAbs
if (-not (Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir -Force | Out-Null }
if (Test-Path $outAbs) { Remove-Item $outAbs -Force }

# Chrome пишет "N bytes written to file" в stderr. В PS 5.1 stderr native-команды прилетает
# в error stream, и при $ErrorActionPreference='Stop' это валит скрипт на успешном рендере.
# Поэтому вокруг вызова временно отпускаем EAP.
$cargs = @(
  '--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars',
  '--allow-file-access-from-files',
  "--force-device-scale-factor=$Scale",
  "--window-size=$W,$H",
  '--virtual-time-budget=4000',
  "--screenshot=$outAbs",
  $url
)
$prevEAP = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
& $chrome @cargs 2>&1 | Out-Null
$ErrorActionPreference = $prevEAP

if (-not (Test-Path $outAbs) -or (Get-Item $outAbs).Length -lt 1kb) {
  throw "Render failed: $outAbs"
}
Write-Host "OK  $outAbs  ($($W * $Scale)x$($H * $Scale))"
