import numpy as np
from skimage import io
from skimage.transform import rotate
from skimage.color import rgb2gray
from deskew import determine_skew
from matplotlib import pyplot as plt
import cv2 
from skimage.filters import threshold_local
from PIL import Image
from pyimgscan import image_corrector
import pytesseract
import os


def resize(img_path):
    img = Image.open(img_path)
    length_x, width_y = img.size
    factor = float(1024.0 / length_x)
    size = int(factor * length_x), int(factor * width_y)
    image_resize = img.resize(size, Image.Resampling.LANCZOS)
    image_resize.save(f"{img_path.split('.')[0]}_upscaled.png", dpi=(300, 300))


def deskew(_img):
    image = io.imread(_img)
    grayscale = rgb2gray(image)
    angle = determine_skew(grayscale, num_peaks=15) #num_peaks=default(20), angle_pm_90=True
    rotated = rotate(image, angle, resize=True) * 255
    return rotated.astype(np.uint8)


def threshhold(img):
    V = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2HSV))[2]
    T = threshold_local(V, 25, offset=15, method="gaussian")
    # Apply the threshold operation
    thresh = (V > T).astype("uint8") * 255
    return thresh 


def denoising1(img):  # best threshhold until now 1402/10/11 13:57 pm 
    blurred_img = cv2.bilateralFilter(img, 9, 75, 75)
    return blurred_img


def denoising2(img):
    ret3,th3 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return th3


def denoising3(img):
    denoised_img = cv2.fastNlMeansDenoisingColored(img, None, 6, 6, 7, 21)
    return denoised_img


def sharpness(img):
    # Create our shapening kernel, remember it must sum to one
    kernel_sharpening = np.array([[-1,-1,-1],
                                  [-1, 6,-1],
                                  ])

    # applying the sharpening kernel to the image
    sharpened = cv2.filter2D(img, -1, kernel_sharpening)
    return sharpened


def dilation(img):
    # Apply Dilation
    dilated_img = cv2.dilate(img, np.ones((3, 3), np.uint8), iterations=1)
    return dilated_img

def erotion(img):
    eroded_img = cv2.erode(img, np.ones((1, 1), np.uint8), iterations=2)
    return eroded_img

def opening(img):
    opened_img = cv2.morphologyEx(img, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=1)
    return opened_img

def closing(img):
    closed_img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8), iterations=1)
    return closed_img 

def predict_text_with_resize(image_path):
    resize(image_path)
    image_name = image_path.split(".")[0]
    image_path_new = image_name+"_upscaled.png"
    image = threshhold(denoising1(deskew(image_path_new)))
    custom_config = r'-l fas'
    text = pytesseract.image_to_string(image, config=custom_config)
    os.remove(image_path_new)
    return text

def predict_text(image_path):
    image = threshhold(denoising1(deskew(image_path)))
    custom_config = r'-l fas --psm 4'
    text = pytesseract.image_to_string(image, config=custom_config)
    return text 

image_path = "samples/kaj3.jpg"
image_corrector(image_path)

image_path_edited = "corrected.png"
image_to_text = predict_text(image_path_edited)
os.remove(image_path_edited)

# Write the extracted text to a text file
output_file_root = 'results/'
output_file_name1 = (image_path.split(".")[0]).split("/")[1]+".txt"
output_file_path = output_file_root + output_file_name1

with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(image_to_text)

print(f"Extracted text saved to: {output_file_path}")



# def display_before_after(_original):
#     plt.figure(figsize=(20, 20))
#     # plt.subplot(2, 2, 1)
#     # plt.imshow(io.imread(_original))
#     plt.subplot(2, 2, 1)
#     fig = plt.imshow(threshhold(denoising1(deskew(_original))), cmap='gray')
#     plt.title("dilateral")
#     plt.show(fig)
#     plt.subplot(2, 2, 2)
#     plt.imshow(denoising2(threshhold(deskew(_original))), cmap='gray')
#     plt.title("gaussian")
#     plt.subplot(2, 2, 3)
#     plt.imshow(threshhold(denoising3(deskew(_original))), cmap='gray')
#     plt.title("Fastn1")

# display_before_after('samples/sample1.jpg')
