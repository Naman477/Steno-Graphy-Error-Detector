# OCR Installation Guide

To use the OCR functionality in this application, you need to install Tesseract OCR on your system.

## Windows Installation

1. Download the Tesseract installer for Windows:
   - Visit the official Tesseract GitHub releases page: https://github.com/UB-Mannheim/tesseract/wiki
   - Download the latest version for your system (32-bit or 64-bit)

2. Run the installer:
   - Double-click the downloaded installer
   - Follow the installation wizard
   - Make sure to check the option to add Tesseract to your PATH environment variable

3. Verify the installation:
   - Open a new Command Prompt window
   - Type `tesseract --version` and press Enter
   - You should see version information for Tesseract

4. Install language packs (optional but recommended):
   - The installer usually includes English language packs by default
   - For additional languages, download the appropriate language data files

## Testing the Installation

After installing Tesseract, restart the application and test the OCR functionality:

1. Make sure the Flask application is running:
   ```
   python app.py
   ```

2. Use the web interface to upload an image and extract text

3. Or use the API endpoint directly:
   ```
   POST /api/v1/ocr
   ```

## Troubleshooting

If you still encounter issues:

1. Make sure Tesseract is added to your PATH:
   - Open Command Prompt
   - Type `echo %PATH%` and look for the Tesseract installation directory

2. Restart your terminal/command prompt after installation

3. On some systems, you may need to specify the Tesseract path in your Python code:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

## Alternative: Using Online OCR Services

If you prefer not to install Tesseract locally, you can modify the application to use online OCR services such as:
- Google Cloud Vision API
- Azure Computer Vision
- Amazon Textract

These services require API keys and have usage limits/costs.