@echo off
echo Installing Toyo Safety QC Tools...

:: Python環境の確認
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    pause
    exit /b 1
)

:: 必要なディレクトリの作成
if not exist "%USERPROFILE%\toyo-safety-qc" (
    mkdir "%USERPROFILE%\toyo-safety-qc"
)
if not exist "%USERPROFILE%\toyo-safety-qc\CSV" (
    mkdir "%USERPROFILE%\toyo-safety-qc\CSV"
)
if not exist "%USERPROFILE%\toyo-safety-qc\CSV_LOG" (
    mkdir "%USERPROFILE%\toyo-safety-qc\CSV_LOG"
)
if not exist "%USERPROFILE%\toyo-safety-qc\templates" (
    mkdir "%USERPROFILE%\toyo-safety-qc\templates"
)

:: テンプレートファイルのコピー
xcopy /y "templates\*.*" "%USERPROFILE%\toyo-safety-qc\templates\"

:: パッケージのインストール
pip install -r requirements.txt
pip install -e .

echo Installation completed!
pause
