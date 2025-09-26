from PIL import Image, ImageDraw, ImageFont
import os

# Create a new image with white background
width, height = 800, 200
image = Image.new('RGB', (width, height), 'white')
draw = ImageDraw.Draw(image)

# Use a default font
font = ImageFont.load_default()

# Draw some text
text = "This is a test image for OCR functionality."

# Get text dimensions (method varies by Pillow version)
# For newer versions of Pillow
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

x = (width - text_width) // 2
y = (height - text_height) // 2

# Draw the text in black
draw.text((x, y), text, fill='black', font=font)

# Save the image
image.save('test_ocr_image.png')
print("Test image created: test_ocr_image.png")