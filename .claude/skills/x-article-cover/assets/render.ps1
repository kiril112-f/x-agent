# x-article-cover · render.ps1 (v2)
# Рендерит обложку 1536x512 (3:1) из assets/cover.html через headless Chrome/Edge.
# Маршрут по умолчанию — l5: гигантский строчный текст, аккуратно перекрытый плашками.
#
#   .\render.ps1 -Hero 'organic|installs' -Plate .\plates\plate-ugc-screen.png, .\plates\plate-app-panel.png -Field cobalt -Out .\cover.png

[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)][string]$Hero,
  [string]$Kicker = '',
  [ValidateSet('cobalt','graphite','violet','teal')][string]$Field = 'cobalt',
  [ValidateSet('l1','l2','l3','l4','l5')][string]$Layout = 'l5',
  [string[]]$Plate = @(),
  [ValidateSet('card','bare')][string]$PlateStyle = 'card',
  [double]$Cover = 16,
  [double]$BandMin = 13,
  [double]$BandMax = 46,
  [double]$Gap = 3.2,
  [ValidateSet('auto','on','off')][string]$Arrow = 'auto',
  [double]$Tilt = 0,
  [double]$Bleed = 0,
  [double]$Fill = 96,
  [double]$ClusterMax = 68,
  [double]$GlowX = 50,
  [ValidateSet('on','off')][string]$Accent = 'off',
  [string]$Obj = '',
  [double]$ObjW = 0,
  [double]$ObjY = 0,
  [double]$ObjX = -60,
  [double]$HeroPx = 0,
  [string]$Mark = '',
  [string]$Out = '.\cover.png',
  [int]$Scale = 2
)

$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [Text.Encoding]::UTF8 } catch { }

# марка: в l5 её место — полоса перекрытия, поэтому по умолчанию выключена
if (-not $PSBoundParameters.ContainsKey('Mark')) {
  $Mark = if ($Layout -eq 'l5') { 'off' } else { '@KirillMorozovop' }
}

if ($Layout -eq 'l5' -and $Plate.Count -eq 0) {
  throw "В l5 текст обязан быть чем-то закрыт: передай -Plate (1-3 ассета) или возьми другой -Layout."
}
if ($Plate.Count -gt 3) { throw "Больше трёх плашек - каша. Максимум 3." }

$here = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }

function Resolve-Asset([string]$p) {
  $cands = @()
  if ([IO.Path]::IsPathRooted($p)) {
    $cands += $p
  } else {
    $cands += (Join-Path (Get-Location).Path $p)
    $cands += (Join-Path $here $p)
    $cands += (Join-Path (Join-Path $here 'plates') $p)
    $cands += (Join-Path (Join-Path $here 'icons') $p)
  }
  foreach ($c in $cands) {
    if (Test-Path -LiteralPath $c) { return ([Uri]((Resolve-Path -LiteralPath $c).Path)).AbsoluteUri }
  }
  throw "Не нашёл ассет: $p"
}

$qs = New-Object System.Collections.Generic.List[string]
function Add-Param([string]$k, $v) {
  if ($null -eq $v) { return }
  $s = if (($v -is [double]) -or ($v -is [int]) -or ($v -is [single])) {
    [string]::Format([Globalization.CultureInfo]::InvariantCulture, '{0}', $v)
  } else {
    [string]$v
  }
  if ([string]::IsNullOrEmpty($s)) { return }
  $qs.Add($k + '=' + [Uri]::EscapeDataString($s))
}

$W = 1536
$H = if ($Layout -eq 'l4') { 640 } else { 512 }

Add-Param 'w' $W
Add-Param 'h' $H
Add-Param 'layout' $Layout
Add-Param 'hero' $Hero
Add-Param 'kicker' $Kicker
Add-Param 'field' $Field
Add-Param 'glowx' $GlowX
Add-Param 'accent' $Accent
Add-Param 'mark' $Mark
if ($HeroPx -gt 0) { Add-Param 'hero_px' $HeroPx }

if ($Layout -eq 'l5') {
  $uris = @()
  foreach ($p in $Plate) { $uris += (Resolve-Asset $p) }
  Add-Param 'plate' ($uris -join ',')
  Add-Param 'platestyle' $PlateStyle
  Add-Param 'cover' $Cover
  Add-Param 'bandmin' $BandMin
  Add-Param 'bandmax' $BandMax
  Add-Param 'gap' $Gap
  Add-Param 'arrow' $Arrow
  Add-Param 'tilt' $Tilt
  Add-Param 'bleed' $Bleed
  Add-Param 'fill' $Fill
  Add-Param 'clustermax' $ClusterMax
} elseif ($Obj) {
  Add-Param 'obj' (Resolve-Asset $Obj)
  if ($ObjW -gt 0) { Add-Param 'objw' $ObjW }
  Add-Param 'objy' $ObjY
  Add-Param 'objx' $ObjX
}

$html = Join-Path $here 'cover.html'
if (-not (Test-Path -LiteralPath $html)) { throw "Рядом со скриптом нет cover.html: $html" }
$url = ([Uri]((Resolve-Path -LiteralPath $html).Path)).AbsoluteUri + '?' + ($qs -join '&')

$outAbs = if ([IO.Path]::IsPathRooted($Out)) { $Out } else { Join-Path (Get-Location).Path $Out }
$outDir = Split-Path -Parent $outAbs
if ($outDir -and -not (Test-Path -LiteralPath $outDir)) { New-Item -ItemType Directory -Path $outDir -Force | Out-Null }

$roots = @($env:ProgramFiles, ${env:ProgramFiles(x86)}, $env:LOCALAPPDATA) | Where-Object { $_ }
$chromeCandidates = @()
foreach ($r in $roots) {
  $chromeCandidates += (Join-Path $r 'Google\Chrome\Application\chrome.exe')
  $chromeCandidates += (Join-Path $r 'Microsoft\Edge\Application\msedge.exe')
}
$chrome = $chromeCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $chrome) { throw "Не нашёл Chrome или Edge - поставь Chrome либо допиши путь в `$chromeCandidates." }

$chromeArgs = @(
  '--headless=new','--disable-gpu','--no-sandbox','--hide-scrollbars',
  '--allow-file-access-from-files',
  ('--force-device-scale-factor=' + $Scale),
  ('--window-size=' + $W + ',' + $H),
  '--virtual-time-budget=6000','--enable-logging=stderr','--v=0',
  ('--screenshot=' + $outAbs),
  $url
)

if (Test-Path -LiteralPath $outAbs) { Remove-Item -LiteralPath $outAbs -Force }

$prev = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
$log = & $chrome @chromeArgs 2>&1 | Out-String
$ErrorActionPreference = $prev

foreach ($line in ($log -split "`r?`n")) {
  if ($line -match 'ГЕОМЕТРИЯ|ПРИЁМКА') {
    $clean = $line -replace '^\[[^\]]*\]\s*', '' -replace '^"', '' -replace '",\s*source:.*$', ''
    Write-Host $clean
  }
}

if (-not (Test-Path -LiteralPath $outAbs) -or (Get-Item -LiteralPath $outAbs).Length -lt 1024) {
  throw "Render failed: $outAbs"
}

# лог команды рядом с обложкой - чтобы обложку можно было повторить один в один
$parts = @('.\render.ps1')
foreach ($k in $PSBoundParameters.Keys) {
  $v = $PSBoundParameters[$k]
  if ($v -is [Array]) {
    $parts += ('-' + $k + ' ' + (($v | ForEach-Object { "'" + $_ + "'" }) -join ', '))
  } elseif ($v -is [string]) {
    $parts += ('-' + $k + " '" + $v + "'")
  } else {
    $parts += ('-' + $k + ' ' + [string]::Format([Globalization.CultureInfo]::InvariantCulture, '{0}', $v))
  }
}
$cmdFile = Join-Path (Split-Path -Parent $outAbs) 'cover.cmd.txt'
Set-Content -LiteralPath $cmdFile -Value (($parts -join ' ') + "`r`n" + $url) -Encoding UTF8

$img = Get-Item -LiteralPath $outAbs
Write-Host ('OK  ' + $outAbs + '  (' + ($W * $Scale) + 'x' + ($H * $Scale) + ', ' + [math]::Round($img.Length / 1kb) + ' kb)')
