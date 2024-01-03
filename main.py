from PIL import Image
import pytesseract
from preprocess_image import make_image_ready


# Set the path to the Tesseract executable (you may not need this if it's in your system's PATH)
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Example usage
image_path = "/home/nimaasltoghiri/Documents/Python_Projects/OCR/samples/FaktoreForoush.png"
image = Image.open(image_path)
preprocessed_image = make_image_ready(image_path)
# custom_config = r'--oem 3 --psm 3'
text = pytesseract.image_to_string(preprocessed_image, lang='fas')

# Write the extracted text to a text file
output_file_path = 'results/output.txt'
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(text)

print(f"Extracted text saved to: {output_file_path}")
