# OCR-Based Document Accuracy Assessment Feature

This document describes the new functionality that allows users to upload images of source and target documents and receive a detailed accuracy analysis report.

## Feature Overview

The new OCR-based accuracy assessment feature enables users to:
1. Upload images of both source and target documents
2. Select preprocessing options for optimal OCR accuracy
3. Automatically extract text from both images using Tesseract OCR
4. Compare the extracted texts and generate a detailed accuracy report

## Web Interface

### Tabbed Interface
The document upload section now features a tabbed interface:
- **Text Files Tab**: Original functionality for uploading text files
- **Image Files (OCR) Tab**: New functionality for uploading image files

### Image Upload Form
The new image upload form includes:
- Separate file inputs for source and target images
- Preprocessing selection dropdowns for both images
- Support for JPG, PNG, BMP, and TIFF formats

### Preprocessing Options
Three preprocessing techniques are available:
1. **Basic**: Default processing with minimal enhancement
2. **Grayscale**: Convert image to grayscale for better contrast
3. **Threshold**: Apply thresholding to reduce noise and improve text clarity

## API Endpoints

### New Endpoint: OCR-Based Accuracy Assessment

**POST /api/v1/ocr-accuracy**

**Request**:
```
Content-Type: multipart/form-data

sourceImageFile: [source image file]
targetImageFile: [target image file]
sourcePreprocess: [basic|grayscale|threshold] (optional)
targetPreprocess: [basic|grayscale|threshold] (optional)
```

**Response (Success)**:
```json
{
  "sourceWhitespaceCount": 120,
  "targetWhitespaceCount": 115,
  "sourceTotalChars": 520,
  "targetTotalChars": 505,
  "errorsFound": 15,
  "accuracy": "97.12%",
  "differences": [],
  "highlightedSourceHtml": "<span class='error-highlight'>original</span> line",
  "highlightedTargetHtml": "<span class='error-highlight'>typed</span> line",
  "diffOperations": [
    {
      "operation": "DELETE",
      "text": "original"
    }
  ],
  "categorizedErrors": [
    {
      "errorNumber": 1,
      "errorType": "Missing Text",
      "inSource": "original line",
      "inTarget": "(not present)"
    }
  ],
  "sourceTotalWords": 100,
  "targetTotalWords": 95,
  "timestamp": "2025-09-26T14:00:00.000000"
}
```

**Response (Error)**:
```json
{
  "error": "Error message"
}
```

## Backend Implementation

### Key Components

1. **OCR Processing Function**:
   - Enhanced [extract_text_from_image()](file://c:\Users\Lenovo\Desktop\OCR\app.py#L221-L259) function with preprocessing options
   - Support for grayscale conversion and thresholding
   - Configurable Tesseract parameters

2. **OCR Accuracy Endpoint**:
   - New `/api/v1/ocr-accuracy` endpoint
   - Handles image file uploads and preprocessing selection
   - Integrates OCR extraction with existing text comparison logic
   - Returns comprehensive accuracy report

3. **File Handling**:
   - Temporary file creation for OCR-extracted text
   - Seamless integration with existing [assess_typing_accuracy()](file://c:\Users\Lenovo\Desktop\OCR\app.py#L262-L325) function
   - Proper cleanup of temporary files

## Testing Results

Our testing shows that the new functionality works effectively:
- **Same Image Test**: 100% accuracy when comparing identical images
- **Different Image Test**: Appropriate error detection when comparing different images
- **Preprocessing Options**: Different techniques can improve accuracy for various image types

## Usage Instructions

1. Open your browser and go to http://localhost:5000
2. Log in with your credentials
3. Navigate to the "Upload Documents" section
4. Click on the "Image Files (OCR)" tab
5. Select your source and target images
6. Choose appropriate preprocessing options
7. Click "Assess Accuracy (via OCR)"
8. View the detailed analysis report

## Best Practices for Optimal Results

1. **Image Quality**: Use high-resolution images with clear text
2. **Lighting**: Ensure even lighting without shadows or glare
3. **Contrast**: Images with high contrast between text and background work best
4. **Preprocessing**: Experiment with different preprocessing options:
   - Use "Grayscale" for images with color that may interfere with text recognition
   - Use "Threshold" for images with noise or low contrast
   - Use "Basic" for high-quality images with clear text

## Error Handling

The system provides clear error messages for:
- Missing Tesseract installation
- Invalid image files
- Authentication issues
- File upload problems
- OCR processing failures

## Integration with Existing Features

The new OCR-based accuracy assessment seamlessly integrates with:
- Existing text-based document comparison
- User authentication system
- Result visualization and reporting
- History tracking
- Error categorization and highlighting