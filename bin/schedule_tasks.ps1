# Windows: register the school automations in Task Scheduler. Safe to re-run (replaces its own tasks).
#   powershell -NoProfile -ExecutionPolicy Bypass -File schedule_tasks.ps1            install
#   powershell -NoProfile -ExecutionPolicy Bypass -File schedule_tasks.ps1 -Remove    take them out
# canvas_watch every 30 min, assess_watch Sundays 17:00, weak_notes daily 16:40. Runs as you, only while you are logged in.
param([switch]$Remove)
$bin = Join-Path $env:USERPROFILE ".claude\bin"
$tasks = @(
  @{ Name = "ClaudeCanvasWatch"; Script = "canvas_watch.py"; Sched = @("/sc", "minute", "/mo", "30") },
  @{ Name = "ClaudeAssessWatch"; Script = "assess_watch.py"; Sched = @("/sc", "weekly", "/d", "SUN", "/st", "17:00") },
  @{ Name = "ClaudeWeakNotes";   Script = "weak_notes.py";   Sched = @("/sc", "daily", "/st", "16:40") }
)
if ($Remove) {
  foreach ($t in $tasks) { schtasks /delete /tn $t.Name /f 2>$null | Out-Null }
  Write-Output "removed the Claude tasks"
  exit 0
}
# find a real python (skip the Microsoft Store stub, which prints nothing useful)
$py = $null
foreach ($c in @("python", "python3", "py")) {
  $cmd = Get-Command $c -ErrorAction SilentlyContinue
  if ($cmd -and $cmd.Source -notmatch "WindowsApps") {
    $v = & $cmd.Source --version 2>&1
    if ($v -match "Python 3") { $py = $cmd.Source; break }
  }
}
if (-not $py) { Write-Output "FAIL: no working python found. Install Python 3 and re-run."; exit 1 }
# pythonw runs without a console window flashing every 30 minutes
$w = Join-Path (Split-Path $py) "pythonw.exe"
if (Test-Path $w) { $py = $w }
$fail = 0
foreach ($t in $tasks) {
  $q = '\"'   # Windows PowerShell 5.1 drops plain inner quotes when calling schtasks, so escape them
  $tr = "$q$py$q $q$(Join-Path $bin $t.Script)$q"
  $out = schtasks /create /tn $t.Name /tr $tr @($t.Sched) /f 2>&1
  if ($LASTEXITCODE -ne 0) { Write-Output "FAIL $($t.Name): $out"; $fail = 1 } else { Write-Output "registered $($t.Name)" }
}
exit $fail
