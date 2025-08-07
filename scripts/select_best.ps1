param(
  [string]$BaseDir = (Join-Path (Split-Path (Get-Location).Path -Parent) "ensemble-spike"),
  [switch]$Apply
)

$ErrorActionPreference = "Stop"

function Invoke-PytestInWorktree {
  param(
    [Parameter(Mandatory)] [string]$WorktreePath
  )
  $python = Join-Path $WorktreePath ".venv/Scripts/python.exe"
  if (-not (Test-Path $python)) {
    Push-Location $WorktreePath
    try { py -3 -m venv .venv } catch { python -m venv .venv }
    Pop-Location
  }
  # garantir pip
  & $python -m ensurepip --upgrade | Out-Null
  & $python -m pip install -q -r (Join-Path $WorktreePath 'requirements.txt') | Out-Null
  $sw = [System.Diagnostics.Stopwatch]::StartNew()
  & $python -m pytest -q
  $pytestExit = $LASTEXITCODE
  $sw.Stop()
  return @{ ExitCode = $pytestExit; DurationMs = $sw.ElapsedMilliseconds }
}

function Get-ShortStat {
  param(
    [Parameter(Mandatory)] [string]$WorktreePath
  )
  $stat = (git -C $WorktreePath diff --shortstat)
  if (-not $stat) { return @{ Insertions = 0; Deletions = 0; Files = 0 } }
  $files = 0; $ins = 0; $del = 0
  if ($stat -match "(\d+) files? changed") { $files = [int]$Matches[1] }
  if ($stat -match "(\d+) insertions?\(\+\)") { $ins = [int]$Matches[1] }
  if ($stat -match "(\d+) deletions?\(-\)") { $del = [int]$Matches[1] }
  return @{ Insertions = $ins; Deletions = $del; Files = $files }
}

function Copy-CandidateToBase {
  param(
    [Parameter(Mandatory)] [string]$CandidatePath,
    [Parameter(Mandatory)] [string]$BaseDir,
    [Parameter(Mandatory)] [string]$Agent
  )
  Copy-Item -Path (Join-Path $CandidatePath 'src/calc.py') -Destination (Join-Path $BaseDir 'src/calc.py') -Force
  Copy-Item -Path (Join-Path $CandidatePath 'tests/test_calc.py') -Destination (Join-Path $BaseDir 'tests/test_calc.py') -Force
  Push-Location $BaseDir
  git add src tests | Out-Null
  git commit -m ("spike: integrar melhor candidato ({0})" -f $Agent) | Out-Null
  Pop-Location
}

function Ensure-IntegrationBranch {
  param([string]$BaseDir)
  Push-Location $BaseDir
  git checkout -B spike/integration | Out-Null
  Pop-Location
}

if (-not (Test-Path $BaseDir)) {
  throw "BaseDir não encontrado: $BaseDir"
}

# Assumir nomes de worktrees padrão ao lado do BaseDir
$parent = Split-Path $BaseDir -Parent
$projectLeaf = Split-Path $BaseDir -Leaf
$candidates = @(
  @{ Agent = 'claude'; Path = (Join-Path $parent ("{0}-wt-claude" -f $projectLeaf)) },
  @{ Agent = 'gemini'; Path = (Join-Path $parent ("{0}-wt-gemini" -f $projectLeaf)) },
  @{ Agent = 'cursor'; Path = (Join-Path $parent ("{0}-wt-cursor" -f $projectLeaf)) }
)

$results = @()
foreach ($c in $candidates) {
  if (-not (Test-Path $c.Path)) { continue }
  Write-Host ("A validar {0} em {1}" -f $c.Agent, $c.Path)
  $test = Invoke-PytestInWorktree -WorktreePath $c.Path
  $stat = Get-ShortStat -WorktreePath $c.Path
  $linesChanged = $stat.Insertions + $stat.Deletions
  $pass = ($test.ExitCode -eq 0)
  $score = if ($pass) { $linesChanged } else { [int]::MaxValue }
  $results += [pscustomobject]@{
    Agent = $c.Agent
    Path = $c.Path
    Passed = $pass
    FilesChanged = $stat.Files
    Insertions = $stat.Insertions
    Deletions = $stat.Deletions
    LinesChanged = $linesChanged
    DurationMs = $test.DurationMs
    Score = $score
  }
}

Write-Host "\n=== Scoreboard ==="
$results | Sort-Object Score, DurationMs | Format-Table -AutoSize

$best = $results | Where-Object { $_.Passed } | Sort-Object Score, DurationMs | Select-Object -First 1
if ($null -eq $best) {
  Write-Host "\nNenhum candidato passou os testes." -ForegroundColor Yellow
  exit 1
}

Write-Host ("\nMelhor candidato: {0} (score={1}, tempo={2}ms)" -f $best.Agent, $best.Score, $best.DurationMs) -ForegroundColor Green

if ($Apply) {
  Ensure-IntegrationBranch -BaseDir $BaseDir
  Copy-CandidateToBase -CandidatePath $best.Path -BaseDir $BaseDir -Agent $best.Agent
  Write-Host "Alterações integradas na branch spike/integration." -ForegroundColor Green
}


