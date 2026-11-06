# Puts the ins排版台 icon on your Desktop.  Run: powershell -ExecutionPolicy Bypass -File app\make_shortcut.ps1
$app = $PSScriptRoot
$pyw = (Get-Command pythonw).Source
$lnk = Join-Path ([Environment]::GetFolderPath('Desktop')) 'ins排版台.lnk'
$s = (New-Object -ComObject WScript.Shell).CreateShortcut($lnk)
$s.TargetPath = $pyw
$s.Arguments = "-X utf8 `"$app\desktop.py`""
$s.WorkingDirectory = (Split-Path $app)
$s.IconLocation = "$app\app.ico,0"
$s.Description = 'ins排版台'
$s.Save()
Write-Output $lnk
