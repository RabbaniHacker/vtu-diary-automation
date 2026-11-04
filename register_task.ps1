# VTU Diary Automation - Task Scheduler Registration
# Runs silently on Logon AND repeats every 15 minutes indefinitely

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $ScriptDir) { $ScriptDir = (Get-Location).Path }
$VbsPath = Join-Path $ScriptDir "launcher.vbs"

$Action = New-ScheduledTaskAction -Execute "wscript.exe" -Argument "`"$VbsPath`""

# Trigger 1: On user Logon / Laptop Wake
$Trigger1 = New-ScheduledTaskTrigger -AtLogOn

# Trigger 2: Repeating every 15 minutes indefinitely
$Trigger2 = New-ScheduledTaskTrigger -Once -At (Get-Date).Date -RepetitionInterval (New-TimeSpan -Minutes 15) -RepetitionDuration (New-TimeSpan -Days 3650)

# Settings: run on battery, start immediately when laptop wakes up / becomes available
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 15)

Register-ScheduledTask -TaskName "VTU_Diary_Automation" -Action $Action -Trigger @($Trigger1, $Trigger2) -Settings $Settings -Force
Write-Host "[OK] Successfully registered VTU_Diary_Automation task with 15-minute silent background check!"
