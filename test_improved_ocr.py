import requests

# Test the OCR endpoint with different preprocessing options
url = 'http://127.0.0.1:5000/api/v1/ocr'

# First, we need to login to get a session
login_url = 'http://127.0.0.1:5000/login'
login_data = {
    'username': 'demo',
    'password': 'demo123'
}

# Create a session to maintain cookies
session = requests.Session()

# Login
login_response = session.post(login_url, data=login_data)
print(f"Login status: {login_response.status_code}")
print(f"Login response: {login_response.json()}")

# Test OCR with different preprocessing techniques
preprocessing_options = ["basic", "grayscale", "threshold"]

for preprocess in preprocessing_options:
    print(f"\n--- Testing OCR with {preprocess} preprocessing ---")
    
    # Test with the better image
    files = {
        'imageFile': ('better_test_ocr_image.png', open('better_test_ocr_image.png', 'rb'), 'image/png')
    }
    
    # Add preprocessing parameter (you would need to modify the backend to support this)
    data = {
        'preprocess': preprocess
    }
    
    try:
        response = session.post(url, files=files, data=data)
        print(f"OCR status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Extracted text: {repr(result.get('extractedText', ''))}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        files['imageFile'][1].close()

# Test with the original image as well
print(f"\n--- Testing OCR with original image ---")
files = {
    'imageFile': ('test_ocr_image.png', open('test_ocr_image.png', 'rb'), 'image/png')
}

try:
    response = session.post(url, files=files)
    print(f"OCR status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Extracted text: {repr(result.get('extractedText', ''))}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error: {e}")
finally:
    files['imageFile'][1].close()