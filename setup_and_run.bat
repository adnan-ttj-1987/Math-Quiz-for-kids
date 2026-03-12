@echo off
REM Multi-Modal AI Processing Platform - Windows Setup and Run Script
REM This script will set up the Python environment and start the platform
REM Can be run from anywhere - automatically navigates to project directory
REM This version keeps the terminal open for manual commands

echo.
echo 🚀 Multi-Modal AI Processing Platform
echo ======================================
echo.
echo This version keeps the terminal open so you can run commands manually.
echo.
echo Current directory: %CD%
echo Script directory: %~dp0
echo.
echo Navigating to project directory...
cd /d "%~dp0"

echo Now in: %CD%
echo.

REM Check if setup is needed (first run or requirements changed)
set SETUP_NEEDED=false
if not exist "math-marathon-env" (
    set SETUP_NEEDED=true
) else (
    REM Check if requirements.txt is newer than the virtual environment
    for %%i in (requirements.txt) do set req_time=%%~ti
    for %%i in (multi-modal-env) do set env_time=%%~ti
    
    REM Simple check: if requirements file exists and is newer, or if setup marker doesn't exist
    if not exist "setup_complete.marker" (
        set SETUP_NEEDED=true
    )
)

if "%SETUP_NEEDED%"=="true" (
    echo Setting up Python environment for the first time...
    echo.
    
    REM Check if Python is installed
    echo Checking Python installation...
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Python is not installed or not in PATH
        echo Please install Python 3.10 or higher from: https://python.org
        echo.
        echo You can now run commands manually in this terminal.
        echo For example: python --version
        echo.
        echo When you're ready, press any key to exit...
        pause >nul
        exit /b 1
    )
    
    echo ✅ Python found
    echo.
    
    REM Create or recreate virtual environment
    if exist "multi-modal-env" (
        echo Recreating virtual environment...
        rmdir /s /q multi-modal-env
    ) else (
        echo Creating virtual environment...
    )
    
    python -m venv multi-modal-env
    if %errorlevel% neq 0 (
        echo ❌ Failed to create virtual environment
        echo Error code: %errorlevel%
        echo.
        echo You can now run commands manually in this terminal.
        echo For example: python -m venv test-env
        echo.
        echo When you're ready, press any key to exit...
        pause >nul
        exit /b 1
    )
    echo ✅ Virtual environment created
    echo.
    
    REM Activate virtual environment
    echo Activating virtual environment...
    call multi-modal-env\Scripts\activate
    if %errorlevel% neq 0 (
        echo ❌ Failed to activate virtual environment
        echo Error code: %errorlevel%
        echo.
        echo You can now run commands manually in this terminal.
        echo For example: multi-modal-env\Scripts\activate
        echo.
        echo When you're ready, press any key to exit...
        pause >nul
        exit /b 1
    )
    
    echo ✅ Virtual environment activated
    echo.
    
    REM Upgrade pip
    echo Upgrading pip...
    python -m pip install --upgrade pip
    if %errorlevel% neq 0 (
        echo ❌ Failed to upgrade pip
        echo Error code: %errorlevel%
        echo.
        echo You can now run commands manually in this terminal.
        echo For example: python -m pip install --upgrade pip --trusted-host pypi.org
        echo.
        echo When you're ready, press any key to exit...
        pause >nul
        exit /b 1
    )
    echo ✅ pip upgraded
    echo.
    
    REM Install requirements
    echo Installing requirements...
    echo.
    echo Checking for CUDA support...
    
    REM Check if CUDA is available
    python -c "import torch; print('CUDA available:', torch.cuda.is_available())" >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ CUDA detected - using optimized requirements
        if exist "requirements-cuda.txt" (
            pip install -r requirements-cuda.txt
        ) else (
            pip install -r requirements.txt
        )
    ) else (
        echo ⚠️  CUDA not available - using CPU requirements
        pip install -r requirements.txt
    )
    
    if %errorlevel% neq 0 (
        echo ❌ Failed to install requirements
        echo Error code: %errorlevel%
        echo.
        echo You can now run commands manually in this terminal.
        echo For example: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
        echo.
        echo When you're ready, press any key to exit...
        pause >nul
        exit /b 1
    )
    echo ✅ Requirements installed
    echo.
    
    REM Create setup complete marker
    echo Setup completed on %date% %time% > setup_complete.marker
    
    echo.
    echo 🎉 Initial setup complete!
    echo =================================
) else (
    echo ✅ Using existing virtual environment
    echo =================================
)

REM Activate virtual environment for manual use
echo.
echo Activating virtual environment for manual commands...
call multi-modal-env\Scripts\activate
echo ✅ Virtual environment activated
echo.

REM Check if Tesseract is installed
echo.
echo Checking Tesseract OCR...
tesseract --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Tesseract OCR not found
    echo Tesseract is required for OCR functionality
    echo Download from: https://github.com/tesseract-ocr/tesseract/releases
    echo Or install via: choco install tesseract
    echo.
    echo You can install it manually while the terminal is open.
    echo.
) else (
    echo ✅ Tesseract OCR found
)

REM Check Hugging Face token
echo.
echo Checking Hugging Face configuration...
if "%HF_TOKEN%"=="" (
    echo ⚠️  Hugging Face token not set
    echo Set HF_TOKEN environment variable or edit .env file
    echo Visit: https://huggingface.co/settings/tokens
    echo.
    echo You can set it manually while the terminal is open:
    echo set HF_TOKEN=your_token_here
    echo.
) else (
    echo ✅ Hugging Face token configured
)

REM Start the platform
echo.
echo 🎉 Starting Multi-Modal AI Processing Platform...
echo ===============================================
echo.
echo The platform will open in your web browser at: http://localhost:8501
echo.
echo To stop the platform, press Ctrl+C in this window
echo.
echo Starting Streamlit web application...
echo.

REM Set Python path to include current directory for app module
set PYTHONPATH=%CD%;%PYTHONPATH%

REM Start Streamlit in the background
start "" cmd /c "streamlit run app/main.py"

REM Keep terminal open for manual commands
echo.
echo 🎯 Terminal is now open for manual commands!
echo ==========================================
echo.
echo You can now run commands in this activated virtual environment:
echo.
echo Useful commands:
echo   pip list                    - Show installed packages
echo   python --version            - Show Python version
echo   python -c "import torch; print(torch.cuda.is_available())" - Check CUDA
echo   streamlit run app/main.py   - Start platform manually
echo   pip install package_name    - Install additional packages
echo   deactivate                  - Deactivate virtual environment
echo.
echo The platform should be running in your browser at http://localhost:8501
echo.
echo To close this terminal, type: exit
echo.

REM Keep the terminal open and interactive
cmd /k "echo Terminal ready for commands. Type 'exit' to close."