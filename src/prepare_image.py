import cv2 as cv 
import os
import numpy as np 
import matplotlib.pyplot as plt

def load_and_prep_img():
    root = os.getcwd()
    imgPath = os.path.join(root, 'input','image_original.png')
    
    # Step 1: load the image
    img = cv.imread(imgPath)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB) # pyright: ignore[reportCallIssue]
    
    # Step 2: get image dimensions
    height, width, channels = img.shape
    print(f'\nOriginal image Info:')
    print(f'Height: {height}')
    print(f'Width: {width}')
    print(f'Channels: {channels}')
    print(f'Data type: {img.dtype}')
    print(f'Is the image a square? {height== width}')
    
    # Step 3: pixels properties
    print(f'\nPixel Properties:')
    print(f'Min pixel value: {img.min()}')
    print(f'Max pixel value: {img.max()}')
    print(f'Mean pixel value: {img.mean()}')
    print(f'Standard deviation: {img.std()}')
    
    # Step 4: resize to 200x200 and save
    resized_img = cv.resize(img, (200,200))
    resized_bgr = cv.cvtColor(resized_img,cv.COLOR_BGR2RGB)
    img = resized_bgr
    outPath = os.path.join(root, 'input/image_200x200.png')
    cv.imwrite(outPath, img)
    
    plt.imshow(img)
    plt.show()

    
if __name__ == '__main__':
    load_and_prep_img()