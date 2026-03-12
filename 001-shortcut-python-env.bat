@echo off
setlocal EnableExtensions

rem -------------------------------------------------------------
rem Open/Bootstrap Python project environment on Windows
rem - No user input; project path is embedded as a variable.
rem -------------------------------------------------------------

set "SCRIPT_NAME=Math Marathon Quizzes"
title %SCRIPT_NAME%

rem ====== CONFIG: Set your project path here ======
rem Option A: Hardcode your project path
rem set "PROJ_PATH=C:\Dev\my_project"

rem Option B: Use the folder where this .bat file resides (recommended if this .bat sits inside the project)
rem set "PROJ_PATH=%~dp0"
set "PROJ_PATH=C:\Users\adnan\Documents\001-programming\001-python\006-kakak-math-marathon"
set "PVENV=math_marathon_env"
rem ====== END CONFIG ======

if not defined PROJ_PATH (
    echo [ERROR] PROJ_PATH is not set. Edit the script to set it.
    goto :PauseHold
)

rem Normalize (remove trailing backslash if present, except root like C:\)
if "%PROJ_PATH:~-1%"=="\" (
    if not "%PROJ_PATH%"=="%PROJ_PATH:~0,3%" (
        set "PROJ_PATH=%PROJ_PATH:~0,-1%"
    )
)

rem Create directory if it doesn't exist
if not exist "%PROJ_PATH%" (
    echo [INFO] Creating project directory "%PROJ_PATH%" ...
    mkdir "%PROJ_PATH%" || (
        echo [ERROR] Failed to create "%PROJ_PATH%".
        goto :PauseHold
    )
)

rem Open a Windows Explorer window at the project path
start "" "%PROJ_PATH%"
echo [OK] Opening project folder in Explorer...

rem Navigate to the directory
pushd "%PROJ_PATH%" || (
    echo [ERROR] Cannot change directory to "%PROJ_PATH%".
    goto :PauseHold
)
echo [OK] Working directory: "%CD%"

rem --- Identify if Python exists on machine ---
set "PY_CMD="
where py >nul 2>&1 && set "PY_CMD=py"
if not defined PY_CMD (
    where python >nul 2>&1 && set "PY_CMD=python"
)
if not defined PY_CMD (
    echo [ERROR] Python 3 is not installed or not on PATH.
    echo          Install from https://www.python.org/downloads/windows/ and tick "Add Python to PATH".
    goto :PauseHold
)

rem Optional: Show Python version
set "PY_VER="
if /i "%PY_CMD%"=="py" (
    for /f "usebackq delims=" %%v in (`py -3 -c "import platform;print(platform.python_version())" 2^>nul`) do set "PY_VER=%%v"
) else (
    for /f "usebackq delims=" %%v in (`python -c "import platform;print(platform.python_version())" 2^>nul`) do set "PY_VER=%%v"
)
if defined PY_VER (
    echo [OK] Python found: %PY_CMD% (v%PY_VER%)
) else (
    echo [OK] Python found: %PY_CMD%
)

rem --- Ensure virtual environment exists ---
set "VENV_DIR=%CD%\%PVENV%"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"
set "ACTIVATE_BAT=%VENV_DIR%\Scripts\activate.bat"

if exist "%VENV_PY%" (
    echo [OK] Virtual environment exists: "%VENV_DIR%"
) else (
    echo [INFO] Creating virtual environment at "%VENV_DIR%" ...
    if /i "%PY_CMD%"=="py" (
        py -3 -m venv "%VENV_DIR%"
    ) else (
        python -m venv "%VENV_DIR%"
    )
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        goto :PauseHold
    )
    echo [OK] Virtual environment created.
)

rem Activate the venv
if exist "%ACTIVATE_BAT%" (
    call "%ACTIVATE_BAT%"
    if errorlevel 1 (
        echo [WARN] Activation returned a non-zero code.
    )
    echo [OK] Environment activated: "%VENV_DIR%"
    where python
    python --version 2>nul
) else (
    echo [ERROR] Activate script not found at "%ACTIVATE_BAT%".
    goto :PauseHold
)

rem Navigate to the directory
pushd "%PROJ_PATH%" || (
    echo [ERROR] Cannot change directory to "%PROJ_PATH%".
    goto :PauseHold
)
echo [OK] Python working directory: "%CD%"

echo(
echo You are now in: %CD%
echo Virtual environment is active. To deactivate later, type:  deactivate \n
echo You may run streamlit run app.py 
if exist "%CD%\requirements.txt" (
    echo Tip: Detected requirements.txt. Run:  pip install -r requirements.txt
)
echo(

rem Keep terminal open so you can continue working
cmd /k

goto :EOF

:PauseHold
echo(
echo Press any key to exit...
pause >nul
goto :EOF