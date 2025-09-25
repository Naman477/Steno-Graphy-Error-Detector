@echo off
title OCR Application
echo ======================================================
echo        OCR (Optical Character Recognition) Error Detector
echo ======================================================
echo.
echo Starting the OCR application...
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
timeout /t 3 /nobreak >nul
dist\OCRApp.exe