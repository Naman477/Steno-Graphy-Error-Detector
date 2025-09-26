import requests

# Test the OCR endpoint through the web interface
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

# Test OCR with the better image and different preprocessing options
test_cases = [
    {"image": "better_test_ocr_image.png", "preprocess": "basic"},
    {"image": "better_test_ocr_image.png", "preprocess": "grayscale"},
    {"image": "better_test_ocr_image.png", "preprocess": "threshold"},
    {"image": "test_ocr_image.png", "preprocess": "basic"}
]

for i, test_case in enumerate(test_cases):
    image_file = test_case["image"]
    preprocess = test_case["preprocess"]
    
    print(f"\n--- Test Case {i+1}: {image_file} with {preprocess} preprocessing ---")
    
    try:
        # Test with the better image
        with open(image_file, 'rb') as f:
            files = {
                'imageFile': (image_file, f, 'image/png')
            }
            data = {
                'preprocess': preprocess
            }
            
            response = session.post(url, files=files, data=data)
            print(f"OCR status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                extracted_text = result.get('extractedText', '')
                print(f"Extracted text: {repr(extracted_text)}")
                
                # Check if the text contains expected content
                if "OCR TEXT RECOGNITION TEST" in extracted_text:
                    print("✓ Successfully recognized main title")
                elif "This is a test image for OCR functionality" in extracted_text:
                    print("✓ Successfully recognized test sentence")
                else:
                    print("✗ Could not recognize expected text")
            else:
                print(f"Error: {response.text}")
    except FileNotFoundError:
        print(f"File {image_file} not found")
    except Exception as e:
        print(f"Error: {e}")