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

## Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## How to Run

1. Start the Flask application:

```bash
python app.py
```

2. Open your web browser and go to `http://localhost:5000`

## API Endpoint

The application exposes a single REST endpoint:

**POST /api/v1/accuracy**

This endpoint accepts `multipart/form-data` with two files:
- `sourceFile`: The file containing the original, correct text.
- `targetFile`: The file containing the text as typed by a user.

### Request Example (using curl)

```bash
curl -X POST \
  http://localhost:5000/api/v1/accuracy \
  -H 'Content-Type: multipart/form-data' \
  -F 'sourceFile=@/path/to/your/source.txt' \
  -F 'targetFile=@/path/to/your/target.txt'
```

Replace `/path/to/your/source.txt` and `/path/to/your/target.txt` with the actual paths to your files.

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

## Web Interface

The application includes a web interface where users can:
1. Upload source and target files
2. Submit the files for analysis
3. View the accuracy report with categorized errors
4. See highlighted differences in both documents

## Error Handling

- **Missing/Empty Files:** Returns `400 Bad Request`.
- **Internal Server Errors:** Returns `500 Internal Server Error` for unexpected issues during file processing.

## Differences from Java Version

This Python implementation maintains the same core functionality as the Java/Spring Boot version but with some differences:
- Uses Flask instead of Spring Boot
- Uses Python's built-in `difflib` instead of `java-diff-utils`
- Simplified project structure
- Same REST API endpoints and response format