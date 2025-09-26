@echo off
title Stenography Error Detector with OCR
echo ======================================================
echo        Stenography Error Detector with OCR
echo ======================================================
echo.
echo Starting the application...
echo The application will automatically open in your default browser.
echo.
echo If the browser doesn't open automatically:
echo    - Open your browser manually
echo    - Go to http://127.0.0.1:5000
echo.
echo To stop the application, close this window or press CTRL+C
echo.
echo ======================================================
echo.
echo IMPORTANT: Make sure you have installed Tesseract OCR before running this application.
echo See OCR_INSTALLATION.md for installation instructions.
echo.
timeout /t 3 /nobreak >nul
python app.py