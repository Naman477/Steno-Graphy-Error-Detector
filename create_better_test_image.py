from PIL import Image, ImageDraw, ImageFont

# Create a new image with white background
width, height = 800, 300
image = Image.new('RGB', (width, height), 'white')
draw = ImageDraw.Draw(image)

# Use a better font if available
try:
    # Try to use a better font (you may need to adjust the path based on your system)
    font = ImageFont.truetype("arial.ttf", 36)
except:
    # Fallback to default font if specific font not available
    font = ImageFont.load_default()

# Draw some text with better spacing
text = "This is a test image for OCR functionality."
lines = [
    "OCR TEXT RECOGNITION TEST",
    "========================",
    "",
    "This is a test image for OCR functionality.",
    "",
    "The quick brown fox jumps over the lazy dog.",
    "1234567890 !@#$%^&*()"
]

y_position = 30
for line in lines:
    # Get text dimensions
    bbox = draw.textbbox((0, 0), line, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center the text
    x = (width - text_width) // 2
    draw.text((x, y_position), line, fill='black', font=font)
    y_position += text_height + 10

# Save the image
image.save('better_test_ocr_image.png')
print("Better test image created: better_test_ocr_image.png")