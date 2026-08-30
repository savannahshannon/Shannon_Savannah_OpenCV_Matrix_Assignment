# Overview
This project demonstrates image processing fundamentals by converting a 200x200 photograph into numerical matrices, performing 32+ OpenCV operations, and manually verifying calculations using image processing mathematics.

# Image Source
- Original: iPhone 16 Pro Max capture (4284x4284 pixels)
- Format: HEIF -> PNG conversion
- Location: Downtown Atl cityscape
- Cropping: Square crop from center
- Final size: 200x200 pixels (8-bit grayscale + BGR channels)

# Installation
bash 
pip install -r requirements.txt

# Execution Sequence
1. Prepare Image:
    bash
    cd src
    python prepare_image.py

    - loads original image
    - verifies 200x200 dimensions
    - saves as PNG

2. Extract Matrices:
    bash
    python opencv_operations.py

    - extracts grayscale and BGR channels to CSV
    - performs 32+ OpenCV operations
    - saves operation results as PNG + CSV

3. Manual Calculations:
    bash
    python manual_calculations.py

    - selects 7x7 patch from image
    - manually calculates 13 operations
    - compares with OpenCV outputs
    - generates verification CSVs

4. Verify Results:
    bash
    python verify_matrices.py

    - compares manual vs OpenCV calculations
    - reports statistics and accuracy

# Project Structure
```
OpenCV_Matrix_Assignment/
├── README.md
├── requirements.txt
│
├── src/
│ ├── prepare_image.py # Part 1: Image preparation
│ ├── opencv_operations.py # Parts 2-4: OpenCV operations
│ ├── manual_calculations.py # Part 5: Manual calculations
│ └── verify_matrices.py # Part 6: Verification
│
├── input/
│ ├── image_original.jpg # Original iPhone photo
│ └── image_200x200.png # Resized 200×200 PNG
│
├── output_images/
│ ├── reconstructed.png
│ ├── negative.png
│ ├── brightness.png
│ ├── contrast.png
│ ├── binary.png
│ ├── equalized.png
│ ├── histograms.png
│ ├── center_100x100.png
│ ├── flip_horizontal.png
│ ├── flip_vertical.png
│ ├── rotate_90.png
│ ├── rotate_30.png
│ ├── resize_100x100.png
│ ├── resize_nearest_neighbor.png
│ ├── resize_bilinear.png
│ ├── mean_filter.png
│ ├── gaussian_filter.png
│ ├── median_filter.png
│ ├── sobelx.png
│ ├── sobely.png
│ ├── sobel_magnitude.png
│ ├── laplacian.png
│ ├── canny.png
│ ├── erosion.png
│ ├── dilation.png
│ ├── opening.png
│ ├── closing.png
│ ├── contour_mask.png
│ └── all_contours.png
│
├── csv_full_image/
│ ├── image_gray_200x200.csv
│ ├── image_blue_200x200.csv
│ ├── image_green_200x200.csv
│ ├── image_red_200x200.csv
│ ├── image_metadata.csv
│ ├── grayscale_manual_verification.csv
│ ├── negative.csv through 31_contour_mask.csv
│ └── contour_measurements.csv
│
└── csv_manual_calculations/
├── manual_input_patch_7x7.csv
├── op01_input.csv through op13_difference.csv
└── verification_summary.csv
```

# Key Findings

# Image Statistics
- Shape: (200, 200, 3) BGR
- Data Type: uint8
- Min Pixel: 0, Max Pixel: 187
- Mean: 110.75, Std Dev: 40.30

# Manual Verification Results
- Negative Transform: 100% exact match
- Brightness/Contrast: Perfect matches after clipping
- Thresholding: 100% exact match
- Filtering: <1.0 pixel difference (rounding acceptable)
- Edge Detection: <2.0 magnitude difference (float precision)
- Morphology: 100% exact match

# Operations Summary
- Color/Intensity: 9 operations
- Geometric: 7 operations
- Spatial Filtering: 3 operations
- Edge Detection: 5 operations
- Morphological: 4 operations
- Contour Analysis: 4 operations

# Technical Notes

# BGR Color Order
OpenCV loads images in BGR order, not RGB. This is critical for:
    - channel separation and merging
    - color space conversions
    - manual pixel calculations

# Grayscale Formula
I_gray = round(0.114B + 0.587G + 0.299R)

These weights reflect human perception (green appears brighter than red/blue).

# Matrix Operations
All operations preserve data types:
- 8-bit operations: uint8 (0-255)
- Floating-point gradients: float32 or float64
- Clipping applied before converting back to uint8

# Edge Cases
- Borders: 3×3 filters use valid region only (5×5 output from 7×7 input)
- Clipping: Brightness/contrast operations clipped to [0, 255]
- Rounding: Floating-point results rounded before uint8 conversion

# Learning Outcomes
This assignment demonstrates:
1. Images are numerical matrices, not just visual objects
2. Image processing relies on mathematical operations
3. Digital operations involve careful data type management
4. Filtering and edge detection extract different image properties
5. Manual calculations verify that OpenCV functions implement standard algorithms correctly

# Requirements
- Python 3.8+
- OpenCV (cv2)
- NumPy
- Pandas
- Matplotlib

See `requirements.txt` for versions.

## Author
Savannah Shannon

## Date
August 2026

## Submission
GitHub Repository: Shannon_Savannah_OpenCV_Matrix_Assignment