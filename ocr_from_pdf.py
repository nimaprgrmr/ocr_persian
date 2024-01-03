from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
from pdf2image import convert_from_path
import pytesseract


# convert image to pdf 
def convert_image_to_pdf(image_path, output_pdf_path):
    # Open the image
    img = Image.open(image_path)

    # Create a PDF document
    pdf_canvas = canvas.Canvas(output_pdf_path, pagesize=letter)

    # Set up the PDF canvas and draw the image
    pdf_canvas.drawImage(image_path, 0, 0, width=letter[0], height=letter[1])

    # Save the PDF
    pdf_canvas.save()


def convert_image_to_pdf(image_path, output_pdf_path):
    # Open the image
    img = Image.open(image_path)

    # Create a PDF document
    pdf_canvas = canvas.Canvas(output_pdf_path, pagesize=letter)

    # Set up the PDF canvas and draw the image
    pdf_canvas.drawImage(image_path, 0, 0, width=letter[0], height=letter[1])

    # Save the PDF
    pdf_canvas.save()

def extract_text_from_pdf(pdf_path):
    # Convert PDF pages to images
    images = convert_from_path(pdf_path)

    # Initialize an empty string to store extracted text
    extracted_text = ''

    # Iterate through each image and extract text
    for i, image in enumerate(images):
        # Save the image temporarily (optional)
        image_path = f'temp_image_{i}.png'
        image.save(image_path, 'PNG')

        # Use pytesseract to extract text from the image
        text = pytesseract.image_to_string(image, lang='fas')
        extracted_text += text + '\n'

    # Optionally, you can remove temporary images
    # for i in range(len(images)):
    #     temp_image_path = f'temp_image_{i}.png'
    #     os.remove(temp_image_path)

    return extracted_text


# Specify the path to your image and the output PDF
image_path = '/home/nimaasltoghiri/Documents/Python_Projects/OCR/samples/simple_photo.jpg'
output_pdf_path = '/home/nimaasltoghiri/Documents/Python_Projects/OCR/samples/simple_photo.pdf'

# Convert the image to a PDF
convert_image_to_pdf(image_path, output_pdf_path)

# Use pytesseract to extract text from the generated PDF
text = extract_text_from_pdf(output_pdf_path)

# Print the extracted text
print(text)