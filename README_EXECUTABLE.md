# OCR Application Executable

This package contains a standalone Windows executable version of the OCR (Optical Character Recognition) Error Detector application.

## Files Included

- `dist\OCRApp.exe` - The standalone executable application
- `run_ocr_app.bat` - A batch file to easily run the application
- `templates\` - HTML templates directory (required for the web interface)
- `static\` - CSS and JavaScript files (required for the web interface)

## How to Run

### Option 1: Using the batch file (Recommended)
1. Double-click on `run_ocr_app.bat`
2. The application will start and automatically open your default browser at http://127.0.0.1:5000
3. If the browser doesn't open automatically, manually navigate to http://127.0.0.1:5000
4. Press CTRL+C in the command window or close the window to stop the application

### Option 2: Direct execution
1. Navigate to the `dist` folder
2. Double-click on `OCRApp.exe`
3. The application will start and automatically open your default browser at http://127.0.0.1:5000
4. If the browser doesn't open automatically, manually navigate to http://127.0.0.1:5000
5. Close the command window to stop the application

## How to Use the Application

1. Once the browser opens, you will see the "Stenography Error Detector" interface
2. Upload two text files:
   - Source File: The original, correct text
   - Target File: The text to be analyzed
3. Click "Assess Accuracy"
4. View the accuracy report, including:
   - Overall accuracy percentage
   - Number of errors found
   - Error distribution chart
   - Detailed error analysis
   - Side-by-side comparison of documents with highlighted differences

## System Requirements

- Windows 7 or later (64-bit)
- No additional software installation required

## Troubleshooting

- If the application doesn't start, make sure no other application is using port 5000
- If you get a Windows SmartScreen warning, click "More info" and then "Run anyway"
- Make sure all files remain in their original folder structure
- If the browser doesn't open automatically, check your browser settings or manually navigate to http://127.0.0.1:5000

## Building from Source

If you want to build the executable from the Python source code:

1. Install Python 3.10+
2. Install required packages:
   ```
   pip install -r requirements.txt
   pip install pyinstaller
   ```
3. Build the executable:
   ```
   pyinstaller OCRApp.spec
   ```

The executable will be created in the `dist` folder.