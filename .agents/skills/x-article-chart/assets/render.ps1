<#
  Рендер графика для X Article в точный PNG через Chrome headless.

  Пример:
    .\render.ps1 -Spec .\examples\curve-linear-vs-exponential.json `
                 -Out ..\..\..\..\x-content-engine\assets\charts\<slug>\chart.png

  Спека — JSON. Схема и типы описаны в references/chart-types.md.
  Скрипт валидирует спеку до рендера: молча кривой график не соберётся.
#>
param(
  [Parameter(Mandatory = $true, ParameterSetName = 'file')][string]$Spec,
  [Parameter(Mandatory = $true, ParameterSetName = 'inline')][string]$Json,
  [string]$Out = ".\chart.png",
  [int]$Scale = 2,
  [switch]$KeepHtml,
  [switch]$Open
)

$ErrorActionPreference = 'Stop'

$chrome = @(
  "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
  "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
  "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $chrome) { throw "Chrome не найден. Укажи путь вручную в render.ps1." }

if ($PSCmdlet.ParameterSetName -eq 'file') {
  if (-not (Test-Path $Spec)) { throw "Спека не найдена: $Spec" }
  $Json = Get-Content -Raw -Encoding UTF8 $Spec
}
try { $s = $Json | ConvertFrom-Json } catch { throw "Спека не парсится как JSON: $($_.Exception.Message)" }

# ---------------------------------------------------------------- валидация
$problems = New-Object System.Collections.Generic.List[string]
$KNOWN = @('curve', 'bars', 'line', 'area', 'split', 'stat')
$type = if ($s.type) { "$($s.type)" } else { 'curve' }
if ($KNOWN -notcontains $type) { $problems.Add("type '$type' неизвестен. Допустимо: $($KNOWN -join ', ')") }

$hasSource = ($s.PSObject.Properties.Name -contains 'source') -and "$($s.source)".Trim()
if ($type -ne 'curve' -and -not $hasSource) {
  $problems.Add("нет source. График с числами без источника не публикуется — см. proof-and-claims.md")
}
if ($type -eq 'curve' -and $hasSource -and "$($s.source)" -notmatch '(?i)illustrative|схема|not to scale|conceptual') {
  $problems.Add("концептуальная кривая с source: подпиши её как illustrative, иначе форму прочитают как измерение")
}

$sn = @($s.series).Count
if ($type -eq 'curve' -or $type -eq 'line' -or $type -eq 'area') {
  if ($sn -eq 0) { $problems.Add("$type без series") }
  if ($sn -gt 4 -and -not $s.palette) {
    $problems.Add("серий $sn при четырёх фирменных цветах. Задай palette: okabe-ito или сократи до 4")
  }
  $emph = @($s.series | Where-Object { $_.emphasis }).Count
  if ($emph -gt 1) { $problems.Add("emphasis стоит у $emph серий. Акцент на визуале ровно один") }
}
if (($type -eq 'bars' -or $type -eq 'split') -and @($s.data).Count -eq 0) { $problems.Add("$type без data") }
if ($type -eq 'bars') {
  $e = @($s.data | Where-Object { $_.emphasis }).Count
  if ($e -gt 1) { $problems.Add("emphasis стоит у $e столбцов. Акцент ровно один") }
  if (@($s.data).Count -gt 9) { $problems.Add("столбцов $(@($s.data).Count): на телефоне это уже таблица, режь до 7") }
}
if ($type -eq 'stat' -and @($s.items).Count -gt 4) { $problems.Add("stat: элементов $(@($s.items).Count), рисуются первые 4") }
if ($s.title -and "$($s.title)".Length -gt 68) { $problems.Add("title длиной $("$($s.title)".Length) — в одну строку не встанет, режь до 68") }

foreach ($p in $problems) { Write-Host "WARN  $p" -ForegroundColor Yellow }

# ------------------------------------------------------------------- рендер
$SIZES = @{ wide = @(1600, 900); tall = @(1600, 1120); strip = @(1600, 620); square = @(1200, 1200) }
$key = if ($s.size -and $SIZES.ContainsKey("$($s.size)")) { "$($s.size)" } else { 'wide' }
$W = if ($s.width) { [int]$s.width } else { $SIZES[$key][0] }
$H = if ($s.height) { [int]$s.height } else { $SIZES[$key][1] }

$tpl = Join-Path $PSScriptRoot 'chart.html'
if (-not (Test-Path $tpl)) { throw "Не найден шаблон: $tpl" }

# Спека уезжает в шаблон base64-ом: так в неё можно класть кавычки, обратные
# апострофы и юникод, ничего не экранируя и не ломая ни JS, ни URL.
$b64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($Json))
$html = (Get-Content -Raw -Encoding UTF8 $tpl).Replace('__SPEC_B64__', $b64)

$outAbs = if ([IO.Path]::IsPathRooted($Out)) { $Out }
          else { [IO.Path]::GetFullPath((Join-Path (Get-Location).Path $Out)) }
$outDir = Split-Path -Parent $outAbs
if (-not (Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir -Force | Out-Null }
if (Test-Path $outAbs) { Remove-Item $outAbs -Force }

$buildHtml = [IO.Path]::ChangeExtension($outAbs, '.build.html')
[IO.File]::WriteAllText($buildHtml, $html, (New-Object Text.UTF8Encoding $false))

# Chrome пишет "N bytes written to file" в stderr. В PS 5.1 stderr native-команды
# прилетает в error stream и при EAP='Stop' валит скрипт на успешном рендере.
$cargs = @(
  '--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars',
  '--allow-file-access-from-files',
  "--force-device-scale-factor=$Scale",
  "--window-size=$W,$H",
  '--virtual-time-budget=4000',
  "--screenshot=$outAbs",
  ("file:///" + $buildHtml.Replace([char]92, [char]47))
)
$prevEAP = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
& $chrome @cargs 2>&1 | Out-Null
$ErrorActionPreference = $prevEAP

if (-not $KeepHtml) { Remove-Item $buildHtml -Force -ErrorAction SilentlyContinue }
if (-not (Test-Path $outAbs) -or (Get-Item $outAbs).Length -lt 1kb) { throw "Render failed: $outAbs" }

# Спека лежит рядом с PNG: график должен пересобираться через месяц, когда
# правится заголовок или приезжает свежая цифра.
if ($PSCmdlet.ParameterSetName -eq 'inline') {
  [IO.File]::WriteAllText([IO.Path]::ChangeExtension($outAbs, '.json'), $Json, (New-Object Text.UTF8Encoding $false))
} else {
  $side = [IO.Path]::ChangeExtension($outAbs, '.json')
  if ((Resolve-Path $Spec).Path -ne $side) { Copy-Item $Spec $side -Force }
}

Write-Host "OK  $outAbs  ($($W * $Scale)x$($H * $Scale))" -ForegroundColor Green
if ($KeepHtml) { Write-Host "HTML $buildHtml" }
if ($Open) { Start-Process $outAbs }
