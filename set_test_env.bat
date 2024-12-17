@echo off
:: テスト環境の設定
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%"
set "OneDriveGraph=%PROJECT_ROOT%tests\test_data"

echo テスト環境を設定しました:
echo Project Root: %PROJECT_ROOT%
echo OneDriveGraph: %OneDriveGraph%

:: Pythonパスの設定（srcディレクトリをPythonパスに追加）
set "PYTHONPATH=%PROJECT_ROOT%;%PYTHONPATH%"

:: main.pyの実行
python "%PROJECT_ROOT%main.py"
pause
