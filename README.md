# Stenography Error Detector (Enhanced Python Version)

This is an enhanced Python implementation of the Stenography Error Detector web application. It provides a REST API to detect stenography errors by comparing two uploaded text files, with additional OCR functionality for image-based document analysis.

## Key Features

### Text Comparison
- Compare two text files and calculate typing accuracy
- Detailed error categorization (Missing Text, Extra Text, Whitespace Errors, Punctuation Errors)
- Visual highlighting of errors in both documents
- Word-level accuracy calculation

### OCR Processing
- Extract text from images using Tesseract OCR
- Multiple preprocessing options (grayscale, threshold)
- Support for various image formats (JPG, PNG, BMP, TIFF)

### OCR-based Document Comparison
- Compare documents extracted from images
- Combine OCR and text comparison for image-based analysis
- Preprocessing options for both source and target images

### Modern Web Interface
- Responsive, card-based design with gradient backgrounds
- Drag and drop file upload
- Real-time progress indicators
- Interactive error visualization
- Error distribution charts
- Fullscreen document viewing
- User authentication system

## Project Structure

```
.
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html         # Main HTML template
├── static/
│   ├── css/
│   │   ├── style.css      # Main stylesheet
│   │   └── grid.css       # Grid system
│   └── js/
│       └── main.js        # Frontend JavaScript
├── uploads/               # Directory for uploaded files (created automatically)
├── README.md              # This file
├── OCR_INSTALLATION.md    # OCR installation guide
├── OCR_FEATURE_SUMMARY.md # OCR feature documentation
├── ENHANCED_FEATURES.md   # UI/UX enhancement documentation
└── Procfile               # Deployment configuration
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

2. The application will automatically open in your default web browser at `http://localhost:5000`

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

## Web Interface

The application includes a modern web interface where users can:
1. Log in with demo credentials
2. Upload source and target files (text or images)
3. Select preprocessing options for OCR
4. Submit the files for analysis
5. View the accuracy report with categorized errors
6. See highlighted differences in both documents
7. Extract text from images using OCR
8. Use extracted text for document comparison

## Error Handling

- **Missing/Empty Files:** Returns `400 Bad Request`.
- **Internal Server Errors:** Returns `500 Internal Server Error` for unexpected issues during file processing.
- **OCR Errors:** Returns specific error messages for Tesseract installation issues.
- **Authentication Issues:** Returns `401 Unauthorized` for unauthenticated requests.

## User Authentication

The application includes a simple user authentication system with the following demo users:
- admin / admin123 (Administrator)
- user1 / password1 (John Doe)
- user2 / password2 (Jane Smith)
- demo / demo123 (Demo User)

## Differences from Original Implementation

This enhanced Python implementation includes several improvements over the original:
- Modern, responsive UI with gradient backgrounds and card-based layout
- OCR functionality for image-based document analysis
- Enhanced error categorization and visualization
- Interactive charts for error distribution
- Real-time progress indicators
- Fullscreen document viewing
- User authentication system
- Improved error handling and user feedback

## Deployment

This application can be deployed to various platforms including Heroku, as indicated by the Procfile in the repository.

## License

This project is licensed under the MIT License - see the LICENSE file for details.