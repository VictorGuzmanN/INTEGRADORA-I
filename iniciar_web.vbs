Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c cd /d ""C:\Users\victo\OneDrive\Escritorio\TEST"" && ""C:\Program Files\Python313\python.exe"" app_web.py", 0, False