@echo off
chcp 65001
echo.

:: カレントディレクトリから1つ上の階層をルートとして設定
cd /d "%~dp0"
cd ..
set "ROOT_DIR=%CD%"
set "MAIN_SCRIPT=%ROOT_DIR%\main.py"

:: デバッグ用の出力
echo [デバッグ情報]
echo 現在のディレクトリ: "%CD%"
echo ルートディレクトリ: "%ROOT_DIR%"
echo 実行スクリプト: "%MAIN_SCRIPT%"
echo.

:: main.pyの存在確認
if exist "%MAIN_SCRIPT%" (
    echo [情報] main.pyが見つかりました
    python "%MAIN_SCRIPT%"
    if errorlevel 1 (
        echo [エラー] プログラムの実行中にエラーが発生しました
        pause
        exit /b 1
    )
) else (
    echo [エラー] main.pyが見つかりません
    echo 確認パス: "%MAIN_SCRIPT%"
    pause
    exit /b 1
)

echo [成功] 処理が完了しました
pause
