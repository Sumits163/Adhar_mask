import cv2
import pytesseract
import numpy as np


image = cv2.imread('aback.jpg')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

_, binary = cv2.threshold(gray, 178, 228, cv2.THRESH_BINARY)
custom_config = r'--oem 3 --psm 6'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
text = pytesseract.image_to_string(binary, config=custom_config)

import re
numbers = re.findall(r'\d+', text)

for number in numbers:
    x, y, w, h = cv2.boundingRect(binary)
    blur_region = image[y:y+h, x:x+w]
    blurred = cv2.GaussianBlur(blur_region, (99, 99), 0)
    image[y:y+h, x:x+w] = blurred

cv2.imshow('Blurred Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
