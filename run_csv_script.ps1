# ショートカットのコード：powershell -ExecutionPolicy Bypass -File "C:\Users\QC07\TSホールディングス株式会社\OfficeScriptの整理 - ドキュメント\QC_グラフ作成\Scripts\run_csv_script.ps1"

# PowerShellスクリプトの先頭でカレントディレクトリを設定
$scriptPath = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
Set-Location $scriptPath
# PowerShellスクリプトの文字エンコーディングを指定
$OutputEncoding = [System.Text.Encoding]::UTF8

# 環境変数からフォルダパスを取得
$OneDriveGraphPath = [Environment]::GetEnvironmentVariable("OneDriveGraph", "User")

# 各スクリプトのフルパスを動的に指定
$script_CSVimport = Join-Path -Path $OneDriveGraphPath -ChildPath "Scripts\csvimport.py"
$script_CSVpivot = Join-Path -Path $OneDriveGraphPath -ChildPath "Scripts\csvpivot.py"
$script_CSVtoXlsx = Join-Path -Path $OneDriveGraphPath -ChildPath "Scripts\csvtoxlsxconverter.py"

# Pythonスクリプトを実行
python $script_CSVimport
python $script_CSVpivot
python $script_CSVtoXlsx

# スクリプトの終了を一時停止
pause
