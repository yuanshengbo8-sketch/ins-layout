# Puts the app icon on your Desktop.  Run: powershell -ExecutionPolicy Bypass -File app\make_shortcut.ps1
# Kept pure ASCII: Windows PowerShell 5 misreads UTF-8 scripts without a BOM.
$app = $PSScriptRoot
$name = 'ins' + [char]0x6392 + [char]0x7248 + [char]0x53F0
$pyw = (Get-Command pythonw).Source
$lnk = Join-Path ([Environment]::GetFolderPath('Desktop')) "$name.lnk"
$s = (New-Object -ComObject WScript.Shell).CreateShortcut($lnk)
$s.TargetPath = $pyw
$s.Arguments = "-X utf8 `"$app\desktop.py`""
$s.WorkingDirectory = (Split-Path $app)
$s.IconLocation = "$apppp.ico,0"
$s.Description = $name
$s.Save()
Write-Output $lnk
