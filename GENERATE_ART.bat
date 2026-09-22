@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"

echo ================================================================
echo  Purple Shift - GPT Image 2.5 Art Pipeline
echo ================================================================
echo.

where py >nul 2>nul
if %errorlevel%==0 (
    set "PY=py -3"
) else (
    where python >nul 2>nul
    if not %errorlevel%==0 (
        echo [ERROR] Python 3 not found.
        echo Install Python 3.10+ and enable "Add Python to PATH".
        pause
        exit /b 1
    )
    set "PY=python"
)

%PY% -c "import openai, PIL" >nul 2>nul
if not %errorlevel%==0 (
    echo Installing required Python packages...
    %PY% -m pip install --upgrade openai pillow
    if not %errorlevel%==0 (
        echo [ERROR] Failed to install dependencies.
        pause
        exit /b 1
    )
)

%PY% tools\art_pipeline\generate_art.py --menu

echo.
pause
endlocal
