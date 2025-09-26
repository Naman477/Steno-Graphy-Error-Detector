# Stenography Error Detector (Python Version)

This is a Python implementation of the Stenography Error Detector web application. It provides a REST API to detect stenography errors by comparing two uploaded text files.

## Project Structure

```
.
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html         # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css      # Stylesheet
│   └── js/
│       └── main.js        # Frontend JavaScript
├── uploads/               # Directory for uploaded files (created automatically)
└── README_PYTHON.md       # This file
```

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Tesseract OCR (see OCR_INSTALLATION.md for installation instructions)

## Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Install Tesseract OCR (see OCR_INSTALLATION.md for instructions)

## How to Run

1. Start the Flask application:

```bash
python app.py
```

2. Open your web browser and go to `http://localhost:5000`

## API Endpoints

### Document Comparison

**POST /api/v1/accuracy**

This endpoint accepts `multipart/form-data` with two files:
- `sourceFile`: The file containing the original, correct text.
- `targetFile`: The file containing the text as typed by a user.

### OCR Processing

**POST /api/v1/ocr**

This endpoint accepts `multipart/form-data` with one file:
- `imageFile`: An image file containing text to be extracted (JPG, PNG, BMP, TIFF)

Additional parameters:
- `preprocess`: Preprocessing technique (basic, grayscale, threshold)

### OCR-based Document Comparison

**POST /api/v1/ocr-accuracy**

This endpoint accepts `multipart/form-data` with two image files:
- `sourceImageFile`: Image of the original, correct text.
- `targetImageFile`: Image of the text as typed by a user.

Additional parameters:
- `sourcePreprocess`: Preprocessing technique for source image (basic, grayscale, threshold)
- `targetPreprocess`: Preprocessing technique for target image (basic, grayscale, threshold)

### Request Example (using curl)

```bash
# Text file comparison
curl -X POST \
  http://localhost:5000/api/v1/accuracy \
  -H 'Content-Type: multipart/form-data' \
  -F 'sourceFile=@/path/to/your/source.txt' \
  -F 'targetFile=@/path/to/your/target.txt'

# OCR processing
curl -X POST \
  http://localhost:5000/api/v1/ocr \
  -H 'Content-Type: multipart/form-data' \
  -F 'imageFile=@/path/to/your/image.png' \
  -F 'preprocess=grayscale'

# OCR-based comparison
curl -X POST \
  http://localhost:5000/api/v1/ocr-accuracy \
  -H 'Content-Type: multipart/form-data' \
  -F 'sourceImageFile=@/path/to/your/source.png' \
  -F 'targetImageFile=@/path/to/your/target.png' \
  -F 'sourcePreprocess=grayscale' \
  -F 'targetPreprocess=grayscale'
```

Replace `/path/to/your/` with the actual paths to your files.

### Response Example (JSON)

```json
{
  "sourceTotalChars": 520,
  "targetTotalChars": 505,
  "sourceTotalWords": 100,
  "targetTotalWords": 95,
  "sourceWhitespaceCount": 120,
  "targetWhitespaceCount": 115,
  "errorsFound": 15,
  "accuracy": "97.12%",
  "differences": [],
  "highlightedSourceHtml": "<span class='error-highlight'>original</span> line",
  "highlightedTargetHtml": "<span class='error-highlight'>typed</span> line",
  "diffOperations": [
    {
      "operation": "DELETE",
      "text": "original"
    },
    {
      "operation": "INSERT",
      "text": "typed"
    }
  ],
  "categorizedErrors": [
    {
      "errorNumber": 1,
      "errorType": "Missing Text",
      "inSource": "original line",
      "inTarget": "(not present)"
    }
  ]
}
```

## Core Functionality

- **File Reading:** Reads content from uploaded files, normalizing line endings (`\r\n` and `\r` are converted to `\n`).
- **Text Comparison:** Uses Python's `difflib` library to compare the source and target texts.
- **Error Categorization:** Categorizes errors into:
  - Missing Text
  - Extra Text
  - Whitespace Errors
  - Punctuation Errors
- **Accuracy Calculation:** Uses the formula: `Accuracy = ((Total Words in Source - Errors) / Total Words in Source) * 100`.
- **HTML Highlighting:** Generates HTML with highlighted errors for visual display.
- **OCR Processing:** Extracts text from images using Tesseract OCR with preprocessing options.
- **OCR-based Comparison:** Combines OCR and text comparison for image-based document analysis.

## Web Interface

The application includes a web interface where users can:
1. Upload source and target files (text or images)
2. Select preprocessing options for OCR
3. Submit the files for analysis
4. View the accuracy report with categorized errors
5. See highlighted differences in both documents

## Error Handling

- **Missing/Empty Files:** Returns `400 Bad Request`.
- **Internal Server Errors:** Returns `500 Internal Server Error` for unexpected issues during file processing.
- **OCR Errors:** Returns specific error messages for Tesseract installation issues.

## Differences from Java Version

This Python implementation maintains the same core functionality as the Java/Spring Boot version but with some differences:
- Uses Flask instead of Spring Boot
- Uses Python's built-in `difflib` instead of `java-diff-utils`
- Simplified project structure
- Same REST API endpoints and response format
- Added OCR functionality
- Added OCR-based document comparison