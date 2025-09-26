import requests

# Test the OCR-based accuracy assessment endpoint
url = 'http://127.0.0.1:5000/api/v1/ocr-accuracy'

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

# Test OCR-based accuracy assessment
print(f"\n--- Testing OCR-based Accuracy Assessment ---")

try:
    # Test with the better test images
    with open('better_test_ocr_image.png', 'rb') as source_img, \
         open('better_test_ocr_image.png', 'rb') as target_img:
        
        files = {
            'sourceImageFile': ('source.png', source_img, 'image/png'),
            'targetImageFile': ('target.png', target_img, 'image/png')
        }
        
        data = {
            'sourcePreprocess': 'basic',
            'targetPreprocess': 'basic'
        }
        
        response = session.post(url, files=files, data=data)
        print(f"OCR Accuracy status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Accuracy: {result.get('accuracy', 'N/A')}")
            print(f"Errors found: {result.get('errorsFound', 'N/A')}")
            print(f"Source words: {result.get('sourceTotalWords', 'N/A')}")
            print(f"Target words: {result.get('targetTotalWords', 'N/A')}")
            
            # Since we're using the same image for both source and target,
            # we expect high accuracy (100% or close to it)
            accuracy = float(result.get('accuracy', '0%').replace('%', ''))
            if accuracy > 95:
                print("✓ Accuracy assessment successful - high similarity detected")
            else:
                print("? Accuracy lower than expected - may be due to OCR variations")
        else:
            print(f"Error: {response.text}")
except FileNotFoundError as e:
    print(f"File not found: {e}")
except Exception as e:
    print(f"Error: {e}")

# Test with different images to verify error detection
print(f"\n--- Testing OCR-based Accuracy Assessment with Different Images ---")

try:
    # Test with different images
    with open('better_test_ocr_image.png', 'rb') as source_img, \
         open('test_ocr_image.png', 'rb') as target_img:
        
        files = {
            'sourceImageFile': ('source.png', source_img, 'image/png'),
            'targetImageFile': ('target.png', target_img, 'image/png')
        }
        
        data = {
            'sourcePreprocess': 'grayscale',
            'targetPreprocess': 'grayscale'
        }
        
        response = session.post(url, files=files, data=data)
        print(f"OCR Accuracy status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Accuracy: {result.get('accuracy', 'N/A')}")
            print(f"Errors found: {result.get('errorsFound', 'N/A')}")
            print(f"Source words: {result.get('sourceTotalWords', 'N/A')}")
            print(f"Target words: {result.get('targetTotalWords', 'N/A')}")
            
            # Since we're using different images, we expect some errors
            errors = result.get('errorsFound', 0)
            if errors > 0:
                print("✓ Accuracy assessment successful - differences detected")
            else:
                print("? No errors detected - may be due to similar content")
        else:
            print(f"Error: {response.text}")
except FileNotFoundError as e:
    print(f"File not found: {e}")
except Exception as e:
    print(f"Error: {e}")