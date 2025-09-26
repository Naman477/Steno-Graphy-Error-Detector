import requests

# Test the OCR endpoint
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

# Test OCR with the created image
files = {
    'imageFile': ('test_ocr_image.png', open('test_ocr_image.png', 'rb'), 'image/png')
}

try:
    response = session.post(url, files=files)
    print(f"OCR status: {response.status_code}")
    print(f"OCR response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
finally:
    files['imageFile'][1].close()