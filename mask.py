import numpy as np
import cv2
import matplotlib.pyplot as plt
import re

import easyocr


def blur_region(x_min, y_min, x_max, y_max, image):
    # Create ROI coordinates(region of interest)
    topLeft = (x_min, y_min)
    bottomRight = (x_max, y_max)
    x, y = topLeft[0], topLeft[1]
    w, h = bottomRight[0] - topLeft[0], bottomRight[1] - topLeft[1]

    # Grab ROI with Numpy slicing and blur
    ROI = image[y:y+h, x:x+w]
    blur = cv2.GaussianBlur(ROI, (55,55), 0)

    # Insert ROI back into image
    image[y:y+h, x:x+w] = blur

def isValidAadhaarNumber(str):
 
    # Regex to check valid
    # Aadhaar number.
    regex = ("^[2-9]{1}[0-9]{3}\\" +
             "s[0-9]{4}\\s[0-9]{4}$")
     
    # Compile the ReGex
    p = re.compile(regex)
 
    # If the string is empty
    # return false
    if (str == None):
        return False
 
    # Return if the string
    # matched the ReGex
    if(re.search(p, str)):
        return True
    else:
        return False

def save_masked_aadhar(path, aadhar_num, view):

    image = cv2.imread(path)

    # image =cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
    # img = cv2.imread('aback.JPEG')
    # print(img)
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)



    reader = easyocr.Reader(['en'])
    output = reader.readtext(image)



    #identify the PAN number
    #regex from: https://www.geeksforgeeks.org/how-to-validate-pan-card-number-using-regular-expression/
    regex = "[0-9]{5}[0-9]{8}"

    numbers = []
    for out in output:
        if isValidAadhaarNumber(out[1]):

            numbers.append(out)
            if len(numbers) == 1:
                break        

    # extracted the word which we need to blur and saved the it in the variable name cord
    ##cord = output[6][0]

    cord = numbers[0][0]
    

# catched up the min and max the cordinates of bounding box
    x_min, y_min = [int(min(idx)) for idx in zip(*cord)]
    x_max, y_max = [int(max(idx)) for idx in zip(*cord)]

    
    px_diff = (x_max-x_min)//3

    blur_region(x_min, y_min, x_max-px_diff, y_max, image)
    

    '''cord2 = numbers[1][0]

    x_min_2, y_min_2 = [int(min(idx)) for idx in zip(*cord2)]
    x_max_2, y_max_2 = [int(max(idx)) for idx in zip(*cord2)]
    
    blur_region(x_min_2, y_min_2, x_max_2, y_max_2, image)'''

    cv2.imwrite("uploads/"+str(aadhar_num)+"_"+view+".png", image)



