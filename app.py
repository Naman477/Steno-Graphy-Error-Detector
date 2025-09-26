from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os
from werkzeug.utils import secure_filename
import difflib
import json
import re
from datetime import datetime
import webbrowser
import threading
import time
import pytesseract
from PIL import Image
import tempfile

# Set the path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.secret_key = 'your-secret-key-here'  # In a real app, use a secure secret key

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# In-memory storage for comparison history (in a real app, this would be a database)
comparison_history = []

# Dummy users data
users = {
    'admin': {
        'password': 'admin123',
        'name': 'Administrator',
        'role': 'admin'
    },
    'user1': {
        'password': 'password1',
        'name': 'John Doe',
        'role': 'user'
    },
    'user2': {
        'password': 'password2',
        'name': 'Jane Smith',
        'role': 'user'
    },
    'demo': {
        'password': 'demo123',
        'name': 'Demo User',
        'role': 'user'
    }
}

# Flag to track if browser has been opened
browser_opened = False

class DiffOperation:
    def __init__(self, operation, text):
        self.operation = operation
        self.text = text

class CategorizedError:
    def __init__(self, error_number, error_type, in_source, in_target):
        self.error_number = error_number
        self.error_type = error_type
        self.in_source = in_source
        self.in_target = in_target

class AccuracyReport:
    def __init__(self):
        self.source_whitespace_count = 0
        self.target_whitespace_count = 0
        self.source_total_chars = 0
        self.target_total_chars = 0
        self.errors_found = 0
        self.accuracy = ""
        self.differences = []
        self.highlighted_source_html = ""
        self.highlighted_target_html = ""
        self.diff_operations = []
        self.categorized_errors = []
        self.source_total_words = 0
        self.target_total_words = 0
        self.timestamp = datetime.now().isoformat()

def read_file_content(file):
    """Read file content and normalize line endings"""
    # Handle our temporary file objects
    if hasattr(file, 'path'):
        with open(file.path, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = file.read().decode('utf-8')
    
    # Handle different line endings by normalizing to \n
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    # Remove BOM if present
    if content.startswith("\uFEFF"):
        content = content[1:]
    return content

def tokenize_words(text):
    """Tokenize text into words"""
    if not text or not text.strip():
        return []
    # Simple word tokenization: split by one or more whitespace characters
    return text.strip().split()

def get_diff_operations(source_words, target_words):
    """Get diff operations between source and target words"""
    diff_operations = []
    
    # Using difflib to compare sequences
    matcher = difflib.SequenceMatcher(None, source_words, target_words)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            diff_operations.append(DiffOperation("EQUAL", " ".join(source_words[i1:i2])))
        elif tag == 'delete':
            diff_operations.append(DiffOperation("DELETE", " ".join(source_words[i1:i2])))
        elif tag == 'insert':
            diff_operations.append(DiffOperation("INSERT", " ".join(target_words[j1:j2])))
        elif tag == 'replace':
            diff_operations.append(DiffOperation("DELETE", " ".join(source_words[i1:i2])))
            diff_operations.append(DiffOperation("INSERT", " ".join(target_words[j1:j2])))
    
    return diff_operations

def categorize_errors(diff_operations):
    """Categorize errors into different types"""
    categorized_errors = []
    error_number = 1
    
    i = 0
    while i < len(diff_operations):
        current_op = diff_operations[i]
        
        if current_op.operation == "DELETE":
            source_text = current_op.text
            target_text = "(not present)"
            whitespace_error = False
            punctuation_error = False
            
            # Check if next operation is an INSERT (potential replacement)
            if i + 1 < len(diff_operations):
                next_op = diff_operations[i + 1]
                if next_op.operation == "INSERT":
                    insert_text = next_op.text
                    
                    # Whitespace error: merged words or partial merge
                    merged_source = source_text.replace(" ", "")
                    if merged_source in insert_text:
                        categorized_errors.append(CategorizedError(
                            error_number, "Whitespace Error", source_text, insert_text))
                        error_number += 1
                        i += 2  # Skip both operations
                        whitespace_error = True
                        continue
                    
                    # Punctuation error: only punctuation differs
                    source_no_punct = re.sub(r'[^\w\s]', '', source_text)
                    insert_no_punct = re.sub(r'[^\w\s]', '', insert_text)
                    if source_no_punct == insert_no_punct and source_text != insert_text:
                        categorized_errors.append(CategorizedError(
                            error_number, "Punctuation Error", source_text, insert_text))
                        error_number += 1
                        i += 2  # Skip both operations
                        punctuation_error = True
                        continue
                    else:
                        # If the inserted text contains any part of the missing text, show it
                        source_words = source_text.split(" ")
                        for word in source_words:
                            if word in insert_text:
                                target_text = insert_text
                                break
            
            if not whitespace_error and not punctuation_error:
                categorized_errors.append(CategorizedError(
                    error_number, "Missing Text", source_text, target_text))
                error_number += 1
                
        elif current_op.operation == "INSERT":
            # Punctuation error: only punctuation differs from previous DELETE
            if i > 0:
                prev_op = diff_operations[i - 1]
                if prev_op.operation == "DELETE":
                    source_no_punct = re.sub(r'[^\w\s]', '', prev_op.text)
                    insert_no_punct = re.sub(r'[^\w\s]', '', current_op.text)
                    if source_no_punct == insert_no_punct and prev_op.text != current_op.text:
                        # Already handled above
                        i += 1
                        continue
            
            categorized_errors.append(CategorizedError(
                error_number, "Extra Text", "(not present)", current_op.text))
            error_number += 1
            
        i += 1
        
    return categorized_errors

def highlight_full_text_with_errors(words, diff_operations, is_source):
    """Generate HTML for the full file content with error highlights"""
    html = []
    for word in words:
        highlight = False
        for op in diff_operations:
            if not is_source and op.operation == "INSERT":
                op_words = op.text.split()
                if word in op_words:
                    highlight = True
                    break
        if highlight:
            html.append(f"<span class='error-highlight'>{escape_html(word)}</span>")
        else:
            html.append(escape_html(word))
    return " ".join(html)

def escape_html(text):
    """Escape HTML special characters"""
    if text is None:
        return ""
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\"", "&quot;")
                .replace("'", "&#39;"))

def extract_text_from_image(image_file, preprocess_type="basic"):
    """Perform OCR on an image file and return the extracted text with optional preprocessing"""
    try:
        # Save the image temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            image_file.save(tmp_file.name)
            tmp_filename = tmp_file.name
        
        # Open and process the image
        image = Image.open(tmp_filename)
        
        # Apply different preprocessing techniques based on the requested type
        if preprocess_type == "grayscale":
            # Convert to grayscale for better OCR accuracy
            if image.mode != 'L':
                image = image.convert('L')
        elif preprocess_type == "threshold":
            # Convert to grayscale and apply threshold
            if image.mode != 'L':
                image = image.convert('L')
            # Apply threshold to get rid of noise using a different approach
            def threshold_func(x):
                return 0 if x < 128 else 255
            image = image.point(threshold_func)
        elif preprocess_type == "basic":
            # Basic preprocessing - just ensure it's in a good format
            if image.mode not in ['L', 'RGB']:
                image = image.convert('RGB')
        
        # Perform OCR with better configuration
        # Different PSM (Page Segmentation Mode) options:
        # --psm 6: Uniform block of text
        # --psm 3: Fully automatic page segmentation, but no OSD
        # --psm 1: Automatic page segmentation with OSD
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(image, config=custom_config)
        
        # Clean up temporary file
        os.unlink(tmp_filename)
        
        return text
    except Exception as e:
        # Provide more specific error messages
        error_msg = str(e)
        if "tesseract is not installed" in error_msg.lower() or "not in your path" in error_msg.lower():
            raise Exception("Tesseract OCR is not installed or not in your PATH. Please install Tesseract OCR and ensure it's in your system PATH. See OCR_INSTALLATION.md for instructions.")
        else:
            raise Exception(f"OCR processing failed: {error_msg}")

def assess_typing_accuracy(source_file, target_file):
    """Main function to assess typing accuracy between two files"""
    # Read file contents
    source_text = read_file_content(source_file)
    target_text = read_file_content(target_file)
    
    # Create report object
    report = AccuracyReport()
    
    # Count whitespace
    report.source_whitespace_count = sum(1 for c in source_text if c.isspace())
    report.target_whitespace_count = sum(1 for c in target_text if c.isspace())
    
    # Tokenize words
    source_words = tokenize_words(source_text)
    target_words = tokenize_words(target_text)
    
    # Set character and word counts
    report.source_total_chars = len(source_text)
    report.target_total_chars = len(target_text)
    report.source_total_words = len(source_words)
    report.target_total_words = len(target_words)
    
    # Get diff operations
    diff_operations = get_diff_operations(source_words, target_words)
    report.diff_operations = diff_operations
    
    # Categorize errors
    categorized_errors = categorize_errors(diff_operations)
    report.categorized_errors = categorized_errors
    report.errors_found = len(categorized_errors)
    
    # Calculate accuracy
    # Only missing and extra errors should reduce accuracy
    error_count = 0
    for err in categorized_errors:
        if err.error_type in ["Missing Text", "Extra Text"]:
            error_count += 1
    
    accuracy_percentage = 0.0
    if len(source_words) > 0:
        correct_words = len(source_words) - error_count
        accuracy_percentage = (correct_words / len(source_words)) * 100
    
    report.accuracy = f"{accuracy_percentage:.2f}%"
    
    # Generate highlighted HTML
    report.highlighted_source_html = highlight_full_text_with_errors(source_words, diff_operations, True)
    report.highlighted_target_html = highlight_full_text_with_errors(target_words, diff_operations, False)
    
    return report

def open_browser():
    """Open the browser after a short delay to ensure the server is running"""
    global browser_opened
    if not browser_opened:
        time.sleep(2)  # Wait for server to start
        webbrowser.open_new('http://127.0.0.1:5000/')
        browser_opened = True

@app.route('/')
def index():
    # If user is logged in, show the main application
    if 'username' in session:
        return render_template('index.html', user=session.get('user'))
    # Otherwise, show the login page
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Check if user exists and password is correct
    if username in users and users[username]['password'] == password:
        session['username'] = username
        session['user'] = users[username]
        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "message": "Invalid username or password"}), 401

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/api/v1/accuracy', methods=['POST'])
def assess_accuracy():
    # Check if user is logged in
    if 'username' not in session:
        return jsonify({"error": "Authentication required"}), 401
    
    # Check if files are present
    if 'sourceFile' not in request.files or 'targetFile' not in request.files:
        return jsonify({"error": "Missing files"}), 400
    
    source_file = request.files['sourceFile']
    target_file = request.files['targetFile']
    
    # Check if files are empty
    if source_file.filename == '' or target_file.filename == '':
        return jsonify({"error": "Empty files"}), 400
    
    try:
        # Assess accuracy
        report = assess_typing_accuracy(source_file, target_file)
        
        # Add to comparison history
        comparison_history.append({
            "timestamp": report.timestamp,
            "source_filename": source_file.filename,
            "target_filename": target_file.filename,
            "accuracy": report.accuracy,
            "errors_found": report.errors_found,
            "user": session.get('username', 'unknown')
        })
        
        # Keep only the last 10 comparisons
        if len(comparison_history) > 10:
            comparison_history.pop(0)
        
        # Convert report to dictionary for JSON serialization
        report_dict = {
            "sourceWhitespaceCount": report.source_whitespace_count,
            "targetWhitespaceCount": report.target_whitespace_count,
            "sourceTotalChars": report.source_total_chars,
            "targetTotalChars": report.target_total_chars,
            "errorsFound": report.errors_found,
            "accuracy": report.accuracy,
            "differences": report.differences,
            "highlightedSourceHtml": report.highlighted_source_html,
            "highlightedTargetHtml": report.highlighted_target_html,
            "diffOperations": [{"operation": op.operation, "text": op.text} for op in report.diff_operations],
            "categorizedErrors": [{
                "errorNumber": err.error_number,
                "errorType": err.error_type,
                "inSource": err.in_source,
                "inTarget": err.in_target
            } for err in report.categorized_errors],
            "sourceTotalWords": report.source_total_words,
            "targetTotalWords": report.target_total_words,
            "timestamp": report.timestamp
        }
        
        return jsonify(report_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# New endpoint to get comparison history
@app.route('/api/v1/history', methods=['GET'])
def get_history():
    # Check if user is logged in
    if 'username' not in session:
        return jsonify({"error": "Authentication required"}), 401
    return jsonify(comparison_history)

# Endpoint to get current user info
@app.route('/api/v1/user', methods=['GET'])
def get_user():
    if 'username' in session:
        return jsonify({
            "username": session['username'],
            "name": session['user']['name'],
            "role": session['user']['role']
        })
    else:
        return jsonify({"error": "Not logged in"}), 401

# Endpoint for OCR processing
@app.route('/api/v1/ocr', methods=['POST'])
def ocr_process():
    # Check if user is logged in
    if 'username' not in session:
        return jsonify({"error": "Authentication required"}), 401
    
    # Check if file is present
    if 'imageFile' not in request.files:
        return jsonify({"error": "Missing image file"}), 400
    
    image_file = request.files['imageFile']
    
    # Check if file is empty
    if image_file.filename == '':
        return jsonify({"error": "Empty file"}), 400
    
    # Get preprocessing option (default to "basic")
    preprocess_type = request.form.get('preprocess', 'basic')
    if preprocess_type not in ['basic', 'grayscale', 'threshold']:
        preprocess_type = 'basic'
    
    try:
        # Extract text from image using OCR with specified preprocessing
        extracted_text = extract_text_from_image(image_file, preprocess_type)
        
        return jsonify({
            "success": True,
            "extractedText": extracted_text,
            "message": "OCR processing completed successfully"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint for OCR-based accuracy assessment
@app.route('/api/v1/ocr-accuracy', methods=['POST'])
def ocr_accuracy_assessment():
    # Check if user is logged in
    if 'username' not in session:
        return jsonify({"error": "Authentication required"}), 401
    
    # Check if image files are present
    if 'sourceImageFile' not in request.files or 'targetImageFile' not in request.files:
        return jsonify({"error": "Missing image files"}), 400
    
    source_image_file = request.files['sourceImageFile']
    target_image_file = request.files['targetImageFile']
    
    # Check if files are empty
    if source_image_file.filename == '' or target_image_file.filename == '':
        return jsonify({"error": "Empty files"}), 400
    
    try:
        # Get preprocessing options
        source_preprocess = request.form.get('sourcePreprocess', 'basic')
        target_preprocess = request.form.get('targetPreprocess', 'basic')
        
        # Validate preprocessing options
        if source_preprocess not in ['basic', 'grayscale', 'threshold']:
            source_preprocess = 'basic'
        if target_preprocess not in ['basic', 'grayscale', 'threshold']:
            target_preprocess = 'basic'
        
        # Extract text from source image using OCR
        source_text = extract_text_from_image(source_image_file, source_preprocess)
        
        # Extract text from target image using OCR
        target_text = extract_text_from_image(target_image_file, target_preprocess)
        
        # Create temporary files to simulate file uploads for accuracy assessment
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt') as source_tmp:
            source_tmp.write(source_text)
            source_tmp_path = source_tmp.name
        
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt') as target_tmp:
            target_tmp.write(target_text)
            target_tmp_path = target_tmp.name
        
        # Create file-like objects for accuracy assessment
        class TempFile:
            def __init__(self, path, filename):
                self.path = path
                self.filename = filename
            
            def read(self):
                with open(self.path, 'rb') as f:
                    return f.read()
            
            def seek(self, offset):
                pass  # Not needed for our use case
        
        source_file_obj = TempFile(source_tmp_path, 'source.txt')
        target_file_obj = TempFile(target_tmp_path, 'target.txt')
        
        # Assess accuracy using the existing function
        report = assess_typing_accuracy(source_file_obj, target_file_obj)
        
        # Clean up temporary files
        os.unlink(source_tmp_path)
        os.unlink(target_tmp_path)
        
        # Add to comparison history
        comparison_history.append({
            "timestamp": report.timestamp,
            "source_filename": f"OCR: {source_image_file.filename}",
            "target_filename": f"OCR: {target_image_file.filename}",
            "accuracy": report.accuracy,
            "errors_found": report.errors_found,
            "user": session.get('username', 'unknown')
        })
        
        # Keep only the last 10 comparisons
        if len(comparison_history) > 10:
            comparison_history.pop(0)
        
        # Convert report to dictionary for JSON serialization
        report_dict = {
            "sourceWhitespaceCount": report.source_whitespace_count,
            "targetWhitespaceCount": report.target_whitespace_count,
            "sourceTotalChars": report.source_total_chars,
            "targetTotalChars": report.target_total_chars,
            "errorsFound": report.errors_found,
            "accuracy": report.accuracy,
            "differences": report.differences,
            "highlightedSourceHtml": report.highlighted_source_html,
            "highlightedTargetHtml": report.highlighted_target_html,
            "diffOperations": [{"operation": op.operation, "text": op.text} for op in report.diff_operations],
            "categorizedErrors": [{
                "errorNumber": err.error_number,
                "errorType": err.error_type,
                "inSource": err.in_source,
                "inTarget": err.in_target
            } for err in report.categorized_errors],
            "sourceTotalWords": report.source_total_words,
            "targetTotalWords": report.target_total_words,
            "timestamp": report.timestamp
        }
        
        return jsonify(report_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Start a thread to open the browser
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    app.run(debug=True)