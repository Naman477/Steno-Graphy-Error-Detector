import requests
import os

# Test the Python version of the stenography error detector

# First, let's create two simple test files
source_content = """The Project Gutenberg eBook of Dorothy and the Wizard in Oz

This ebook is for the use of anyone anywhere in the United States and
most other parts of the world at no cost and with almost no restrictions
whatsoever."""

target_content = """The Project Gutenberg eBook of Dorothy and the Wizard in Oz

This ebook is for the use of anyone anywhere in the United States and
most other parts of the world at no cost and with almost no restrictions
whatsoever. But this line is extra in the target file."""

# Write test files
with open("test_source.txt", "w") as f:
    f.write(source_content)

with open("test_target.txt", "w") as f:
    f.write(target_content)

# Test the API endpoint
url = "http://127.0.0.1:5000/api/v1/accuracy"

files = {
    'sourceFile': open('test_source.txt', 'rb'),
    'targetFile': open('test_target.txt', 'rb')
}

try:
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Clean up test files
    files['sourceFile'].close()
    files['targetFile'].close()
    os.remove("test_source.txt")
    os.remove("test_target.txt")