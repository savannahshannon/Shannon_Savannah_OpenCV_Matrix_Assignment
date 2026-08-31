import cv2 as cv 
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def extract_matrices_to_csv():
    root = os.getcwd()
    imgPath = os.path.join(root, 'input','image_200x200.png')
    csv_output_dir = 'csv_full_image'
    img = cv.imread(imgPath)
    
    # Step 1: convert to grayscale
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    #plt.imshow(imgGray, cmap='gray')
    #plt.show()
    
    # Step 2: split into BGR channels
    b, g, r = cv.split(img) 
    
    # Step 3: save all matrices as CSV
    np.savetxt(f'{csv_output_dir}/image_gray_200x200.csv', imgGray, fmt='%d', delimiter=',')
    np.savetxt(f'{csv_output_dir}/image_blue_200x200.csv', b, fmt='%d', delimiter=',')
    np.savetxt(f'{csv_output_dir}/image_green_200x200.csv', g, fmt='%d', delimiter=',')
    np.savetxt(f'{csv_output_dir}/image_red_200x200.csv', r, fmt='%d', delimiter=',')
    
    # Step 4: create metadata CSV
    height, width, channels = img.shape
    metadata = {
        'Property': ['Shape', 'Height', 'Width', 'Channels', 'Data Type',
                    'Min Pixel', 'Max Pixel', 'Mean Pixel', 'Std Dev'],
        'Value': [
            str(img.shape),
            height,
            width,
            channels,
            str(img.dtype),
            int(img.min()),
            int(img.max()),
            f"{img.mean():.2f}",
            f"{img.std():.2f}"
        ]
    }
    
    metadata_df = pd.DataFrame(metadata)
    metadata_df.to_csv(f'{csv_output_dir}/image_metadata.csv', index=False)

def verify_grayscale():
    gray_csv = np.loadtxt('csv_full_image/image_gray_200x200.csv', delimiter=',', dtype=int)
    blue_csv = np.loadtxt('csv_full_image/image_blue_200x200.csv', delimiter=',', dtype=int)
    green_csv = np.loadtxt('csv_full_image/image_green_200x200.csv', delimiter=',', dtype=int)
    red_csv = np.loadtxt('csv_full_image/image_red_200x200.csv', delimiter=',', dtype=int)
    
    print('Manual grayscale verification')
    print('Formula: I_gray = round(0.114*B + 0.587*G + 0.299*R)')
    
    # test pixels
    test_pixels = [
        (10,10),
        (50,50),
        (100,100),
        (150,150),
        (190,190),
    ]
    
    # store results for CSV export
    results = {
        'Row': [],
        'Col': [],
        'Blue': [],
        'Green': [],
        'Red': [],
        'Manual_Gray': [],
        'OpenCV_Gray': [],
        'Difference': []
    }
    
    for row, col in test_pixels:
        b_val = blue_csv[row, col] # get BGR values from CSVs
        g_val = green_csv[row, col]
        r_val = red_csv[row, col]
        
    manual_gray = round(0.114 * b_val + 0.587 * g_val + 0.299 * r_val)
    opencv_gray = gray_csv[row, col]
    diff = opencv_gray - manual_gray
    
    # detailed calculations
    print(f"\nPixel [{row}, {col}]:")
    print(f"  B={b_val}, G={g_val}, R={r_val}")
    print(f"  Manual: round(0.114*{b_val} + 0.587*{g_val} + 0.299*{r_val})")
    print(f"         = round({0.114*b_val:.2f} + {0.587*g_val:.2f} + {0.299*r_val:.2f})")
    print(f"         = round({0.114*b_val + 0.587*g_val + 0.299*r_val:.2f})")
    print(f"         = {manual_gray}")
    print(f"  OpenCV: {opencv_gray}")
    print(f"  Difference: {diff}")
    
    # store in results
    results['Row'].append(row)
    results['Col'].append(col)
    results['Blue'].append(b_val)
    results['Green'].append(g_val)
    results['Red'].append(r_val)
    results['Manual_Gray'].append(manual_gray)
    results['OpenCV_Gray'].append(opencv_gray)
    results['Difference'].append(diff)
    
    # save results to CSV
    results_df = pd.DataFrame(results)
    results_df.to_csv('csv_full_image/grayscale_manual_verification.csv', index=False)
    return results_df

def color_intensity_op(img, gray):
    b, g, r = cv.split(img)
    reconstructed = cv.merge([b, g, r]) # reconstruct from channels
    cv.imwrite('output_images/reconstructed.png', reconstructed)
    
    # greyscale 
    cv.imwrite('output_images/grayscale.png', gray)
    np.savetxt('csv_full_image/grayscale.csv', gray, fmt='%d', delimiter=',')
    
    # individual channels
    cv.imwrite('output_images/blue_channel.png', b)
    np.savetxt('csv_full_image/blue_channel.csv', b, fmt='%d', delimiter=',')
    
    cv.imwrite('output_images/green_channel.png', g)
    np.savetxt('csv_full_image/green_channel.csv', g, fmt='%d', delimiter=',')
    
    cv.imwrite('output_images/red_channel.png', r)
    np.savetxt('csv_full_image/red_channel.csv', r, fmt='%d', delimiter=',')
    
    # image negative
    negative = 255 - gray 
    cv.imwrite('output_images/negative.png', negative)
    np.savetxt('csv_full_image/negative.csv', negative, fmt='%d', delimiter=',')
    
    # brightness inc (+40)
    bright = cv.convertScaleAbs(gray.astype(np.float32) + 40) 
    bright = np.clip(gray.astype(np.float32) + 40, 0, 255).astype(np.uint8)
    cv.imwrite('output_images/brightness.png', bright)
    np.savetxt('csv_full_image/brightness.csv', bright, fmt='%d', delimiter=',')
    
    # contrast mod(1.25x)
    contrast = np.clip(gray.astype(np.float32) * 1.25, 0, 255).astype(np.uint8) 
    cv.imwrite('output_images/contrast.png', contrast)
    np.savetxt('csv_full_image/contrast.csv', contrast, fmt='%d', delimiter=',')
    
    # binary threshold(127)
    _, binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY) # binary threshold(127)
    cv.imwrite('output_images/binary.png', binary)
    np.savetxt('csv_full_image/binary.csv', binary, fmt='%d', delimiter=',')
    
    # histogram equalization
    equalized = cv.equalizeHist(gray)
    cv.imwrite('output_images/equalized.png', equalized)
    np.savetxt('csv_full_image/equalized.csv', equalized, fmt='%d', delimiter=',')
    
    # generate and save histograms
    hist_original = cv.calcHist([gray], [0], None, [256], [0, 256])
    hist_equalized = cv.calcHist([equalized], [0], None, [256], [0, 256])
    
    # save histogram plot
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1,2,1)
    plt.plot(hist_original, color='black')
    plt.title('Original Histogram')
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    
    plt.subplot(1,2,2)
    plt.plot(hist_equalized, color='black')
    plt.title('Equalized Histogram')
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    
    plt.tight_layout()
    plt.savefig('output_images/histograms.png', dpi=100)
    plt.close()
    
    return binary

def geometric_operations(gray):
    #extract center 100x100
    center_100 = gray[50:150, 50:150]
    cv.imwrite('output_images/center_100x100.png', center_100)
    np.savetxt('csv_full_image/center_100x100.csv', center_100, fmt='%d', delimiter=',')
    
    #flip horizontal
    flipped_h = cv.flip(gray, 1)
    cv.imwrite('output_images/flip_horizontal.png', flipped_h)
    np.savetxt('csv_full_image/flip_horizontal.csv', flipped_h, fmt='%d', delimiter=',')
    
    # rotate 90 degrees
    rotated_90 = cv.rotate(gray, cv.ROTATE_90_CLOCKWISE)
    cv.imwrite('output_images/rotate_90.png', rotated_90)
    np.savetxt('csv_full_image/rotate_90.csv', rotated_90)
    
    # rotate 30 degrees about center
    h, w = gray.shape
    center = (w // 2, h // 2)
    rotation_matrix = cv.getRotationMatrix2D(center, 30, 1.0)
    rotated_30 = cv.warpAffine(gray, rotation_matrix, (w, h))
    cv.imwrite('output_images/rotate_30.png', rotated_30)
    np.savetxt('csv_full_image/rotate_30.csv', rotated_30, fmt='%d', delimiter=',')
    
    # resize to 100x100
    resized_100 = cv.resize(gray, (100, 100))
    cv.imwrite('output_images/resize_100x100.png', resized_100)
    np.savetxt('csv_full_image/resize_100x100.csv', resized_100, fmt='%d', delimiter=',')
    
    # resize back to 200x200 with two methods
    resized_nn = cv.resize(resized_100, (200, 200), interpolation=cv.INTER_NEAREST)
    cv.imwrite('output_images/resize_nearest_neighbor.png', resized_nn)
    np.savetxt('csv_full_image/resize_bilinear.csv', resized_nn, fmt='%d', delimiter=',')
    
    # bilinear
    resized_bilinear = cv.resize(resized_100, (200, 200), interpolation=cv.INTER_LINEAR)
    cv.imwrite('output_images/resize_bilinear.png', resized_bilinear)
    np.savetxt('csv_full_image/resize_bilinear.csv', resized_bilinear, fmt='%d', delimiter=',')

def spatial_filtering_op(gray):
    # mean filter (3x3)
    mean_filter = cv.blur(gray, (3,3))
    cv.imwrite('output_images/mean_filter.png', mean_filter)
    np.savetxt('csv_full_image/mean_filter.csv', mean_filter, fmt='%d', delimiter=',')
    
    # gaussian filter (3x3)
    gaussian_filter = cv.GaussianBlur(gray, (3,3), 0)
    cv.imwrite('output_images/gaussian_filter.png', gaussian_filter)
    np.savetxt('csv_full_image/gaussian_filter.csv', gaussian_filter, fmt='%d', delimiter=',')
    
    # median filter (3x3)
    median_filter = cv.medianBlur(gray, 3)
    cv.imwrite('output_images/median_filter.png', median_filter)
    np.savetxt('csv_full_image/median_filter.csv', median_filter, fmt='%d', delimiter=',')
    
def edge_detection_op(gray):
    # sobelX
    sobelx = cv.Sobel(gray, cv.CV_32F, 1, 0, ksize=3)
    sobelx_uint = np.clip(np.abs(sobelx), 0, 255).astype(np.uint8)
    cv.imwrite('output_images/sobelx.png', sobelx_uint)
    np.savetxt('csv_full_image/sobelx.csv', sobelx, fmt='%.2f', delimiter=',')
    
    # sobelY
    sobely = cv.Sobel(gray, cv.CV_32F, 0, 1, ksize=3)
    sobely_uint = np.clip(np.abs(sobely), 0, 255).astype(np.uint8)
    cv.imwrite('output_images/sobely.png', sobely_uint)
    np.savetxt('csv_full_image/sobely.csv', sobely, fmt='%.2f', delimiter=',')
    
    # sobel magnitude
    magnitude = np.sqrt(sobelx**2 + sobely**2)
    magnitude_uint = np.clip(magnitude, 0, 255).astype(np.uint8)
    cv.imwrite('output_images/sobel_magnitude.png', magnitude_uint)
    np.savetxt('csv_full_image/sobel_magnitude.csv', magnitude, fmt='%.2f', delimiter=',')
    
    # laplacian
    laplacian = cv.Laplacian(gray, cv.CV_32F)
    laplacian_uint = np.clip(np.abs(laplacian), 0, 255).astype(np.uint8)
    cv.imwrite('output_images/laplacian.png', laplacian_uint)
    np.savetxt('csv_full_image/laplacian.csv', laplacian, fmt='%.2f', delimiter=',')
    
    # canny edge
    canny = cv.Canny(gray, 100, 200)
    cv.imwrite('output_images/canny.png', canny)
    np.savetxt('csv_full_image/canny.csv', canny, fmt='%d', delimiter=',')
    
    return canny
    
def morphological_op(binary):
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    
    # erosion
    erosion = cv.erode(binary, kernel, iterations=1)
    cv.imwrite('output_images/erosion.png', erosion)
    np.savetxt('csv_full_image/erosion.csv', erosion, fmt='%d', delimiter=',')
    
    # dilation
    dilation = cv.dilate(binary, kernel, iterations=1)
    cv.imwrite('output_images/dilation.png', dilation)
    np.savetxt('csv_full_image/dilation.csv', dilation, fmt='%d', delimiter=',')
    
    # opening (erosion then dilation)
    opening = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)
    cv.imwrite('output_images/opening.png', opening)
    np.savetxt('csv_full_image/opening.csv', opening, fmt='%d', delimiter=',')
    
    # closing (dilation then erosion)
    closing = cv.morphologyEx(binary, cv.MORPH_CLOSE, kernel)
    cv.imwrite('output_images/closing.png', closing)
    np.savetxt('csv_full_image/closing.csv', closing, fmt='%d', delimiter=',')
    
def contour_analysis_op(img, canny):
    # detect contours
    contours, hierarchy = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    print(f'Detected {len(contours)} contours')
    
    # create contour mask
    contour_mask = np.zeros_like(canny)
    cv.drawContours(contour_mask, contours, -1, 255, 1)
    cv.imwrite('output_images/contour_mask.png', contour_mask)
    np.savetxt('csv_full_image/contour_mask.csv', contour_mask, fmt='%d', delimiter=',')
    
    # draw all contours
    img_contours = cv.cvtColor(canny, cv.COLOR_GRAY2BGR)
    cv.drawContours(img_contours, contours, -1, (0, 255, 0), 2)
    cv.imwrite('output_images/all_contours.png', img_contours)
    
    # draw contour with bounding box
    img_bbox = img.copy()
    cv.drawContours(img_bbox, contours, -1, (0, 255, 0), 2)
    if len(contours) > 0:
        largest_contour = max(contours, key=cv.contourArea)
        x, y, w, h = cv.boundingRect(largest_contour)
        cv.rectangle(img_bbox, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv.imwrite('output_images/contour_bbox.png', img_bbox)
    
    # draw contour with centroid
    img_centroid = img.copy()
    cv.drawContours(img_centroid, contours, -1, (0, 255, 0), 2)
    if len(contours) > 0:
        largest_contour = max(contours, key=cv.contourArea)
        M = cv.moments(largest_contour)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv.circle(img_centroid, (cx, cy), 5, (0, 0, 255), -1)
    cv.imwrite('output_images/contour_centroid.png', img_centroid)
    
    if len(contours) > 0:
        largest_contour = max(contours, key=cv.contourArea)
        area = cv.contourArea(largest_contour)
        perimeter = cv.arcLength(largest_contour, True)
        x, y, w, h = cv.boundingRect(largest_contour)
        
        # centroid
        M = cv.moments(largest_contour)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
        else:
            cx, cy = 0, 0
    
    
    
        # save measurements
        measurements = {
            'Metric': ['Area', 'Perimeter', 'BBox_X', 'BBox_Y', 'BBox_Width', 'BBox_Height', 'Centroid_X', 'Centroid_Y'],
            'Value': [area, perimeter, x, y, w, h, cx, cy]
        }
        measurements_df = pd.DataFrame(measurements)
        measurements_df.to_csv('csv_full_image/contour_measurements.csv', index=False)
        
        print(f'Largest contour analysis:')
        print(f'Area: {area:.2f}')
        print(f'Perimeter: {perimeter:.2f}')
        print(f'BBox: ({x}, {y}) {w}*{h}')
        print(f'Centroid: ({cx}, {cy})')
        
if __name__ == "__main__":
    extract_matrices_to_csv()
    verify_grayscale()
    
    img = cv.imread('input/image_200x200.png')
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    binary = color_intensity_op(img, gray)
    geometric_operations(gray)
    spatial_filtering_op(gray)
    canny_edge = edge_detection_op(gray)
    morphological_op(binary)
    contour_analysis_op(img, canny_edge)