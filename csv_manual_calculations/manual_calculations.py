import cv2 as cv 
import numpy as np 
import os
import pandas

def select_patch():
    gray = np.loadtxt('csv_full_Image/image_gray_200x200.csv', delimiter=',', dtype=int)
    
    # create path
    start_row = 120
    start_col = 140
    patch = gray[start_row:start_row+7, start_col:start_col+7]
    
    # save patch
    np.savetxt('csv_manual_calculations/manual_input_patch_7x7.csv', patch, fmt='%d', delimiter=',')
    print(f'Selected 7x7 patch from [{start_row}:{start_row+7}, {start_col}:{start_col+7}]')
    print(patch)
    print(f'Patch Stats:')
    print(f'Min: {patch.min()}, Max: {patch.max()}, Mean: {patch.mean():.2f}, Std: {patch.std():.2f}')
    
    return patch, start_row, start_col
    
def op_01_neg(patch):
    # operation 1: image negative
    # formula: I_negative = 255 - I
    print(f'Operation 1: Image negative')
    print(f'Formula: I_negative = 255 - I')
    
    positions = [(0,0), (0,1), (1,0)]
    manual_patch = np.zeros_like(patch, dtype=int)
    
    # manual calculation
    for i, j in positions:
        input_val = patch[i,j]
        manual_val = 255 - input_val
        manual_patch[i,j] = manual_val
        print(f'[{i},{j}]: I_negative = 255 - {input_val} = {manual_val}')
        
    for i in range(7):
        for j in range(7):
            manual_patch[i,j] = 255 - patch[i,j]
    
    print(f'Manual patch:')
    print(manual_patch)
    
    # load OpenCV negative output and check
    opencv_full = np.loadtxt('csv_full_image/negative.csv', delimiter=',', dtype=int)
    start_row, start_col = 120, 140
    opencv_patch = opencv_full[start_row:start_row+7,start_col:start_col+7]
    print(f'OpenCV patch:')
    print(opencv_patch)
    
    print(f'Comparison:')
    difference = opencv_patch - manual_patch
    print(difference)
    
    # stats
    max_diff = np.max(np.abs(difference))
    mean_diff = np.mean(np.abs(difference))
    exact_matches = np.sum(difference == 0)
    percent_match = (exact_matches / 49) * 100
    
    print(f'\nVerification:')
    print(f'Max abs difference: {max_diff}')
    print(f'Mean abs difference: {mean_diff:.2f}')
    print(f'Exactly matching cells: {exact_matches}/49')
    print(f'Percentage matching: {percent_match:.2f}%')
    
    # save csvs
    np.savetxt('csv_manual_calculations/op01_input.csv', patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op01_manual_output.csv', manual_patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op01_opencv_output.csv', opencv_patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op01_difference.csv', difference, fmt='%d', delimiter=',')

def op_02_brightness(patch):
    # operation 2: brightness increase (+40)
    # formula: I_bright = clip(I + 40, 0, 255)
    print(f'Operation 2: Brightness increase (+40)')
    print(f'Formula: I_bright = clip(I + 40, 0, 255)')
    
    # manual calculation
    manual_patch = np.clip(patch.astype(np.float32) + 40, 0, 255).astype(int)
    print(f'Manual patch:')
    print(manual_patch)
    
    # load OpenCV output and check
    opencv_full = np.loadtxt('csv_full_image/brightness.csv', delimiter=',', dtype=int)
    start_row, start_col = 120, 140
    opencv_patch = opencv_full[120:127, 140:147]
    
    print(f'Comparison:')
    difference = opencv_patch - manual_patch
    
    # stats
    max_diff = np.max(np.abs(difference))
    exact_matches = np.sum(difference == 0)
    
    print(f'\nVerification:')
    print(f'Max diff: {max_diff}, Exact matches: {exact_matches}/49')
    
    # save csvs
    np.savetxt('csv_manual_calculations/op02_input.csv', patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op02_manual_output.csv', manual_patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op02_opencv_output.csv', opencv_patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op02_difference.csv', difference, fmt='%d', delimiter=',')
    
def op_03_contrast(patch):
    # operation 3: contrast (x1.25)
    # formula: I_contrast = clip(I * 1.25, 0, 255)
    print(f'Operation 3: Contrast (x1.25)')
    print(f'Formula: I_contrast = clip(I * 1.25, 0, 255)')
    
    # manual calculation
    manual_patch = np.clip(patch.astype(np.float32) * 1.25, 0, 255).astype(int)
    print(f'Manual patch:')
    print(manual_patch)
    
    # load OpenCV output and check
    opencv_full = np.loadtxt('csv_full_image/contrast.csv', delimiter=',', dtype=int)
    opencv_patch = opencv_full[120:127, 140:147]
    
    print(f'Comparison:')
    difference = opencv_patch - manual_patch
        
    # stats
    max_diff = np.max(np.abs(difference))
    exact_matches = np.sum(difference == 0)
    
    print(f'\nVerification:')
    print(f'Max diff: {max_diff}, Exact matches: {exact_matches}/49')
    
    # save csvs
    np.savetxt('csv_manual_calculations/op03_input.csv', patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op03_manual_output.csv', manual_patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op03_opencv_output.csv', opencv_patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op03_difference.csv', difference, fmt='%d', delimiter=',')

def op_04_threshold(patch):
    # operation 4: Binary threshold (127)
    # formula: I_binary = 255 if I > 127 else 0
    print(f'Operation 4: Binary threshold (127)')
    print(f'Formula: I_binary = 255 if I > 127 else 0')
    
    # manual calculation
    manual_patch = np.where(patch > 127, 255, 0).astype(int)
    print(f'Manual patch:')
    print(manual_patch)
    
    # load OpenCV output and check
    opencv_full = np.loadtxt('csv_full_image/binary.csv', delimiter=',', dtype=int)
    opencv_patch = opencv_full[120:127, 140:147]
    
    print(f'Comparison:')
    difference = opencv_patch - manual_patch
    exact_matches = np.sum(difference == 0)
    print(f'Exact matches: {exact_matches}/49')
    
    # save csvs
    np.savetxt('csv_manual_calculations/op04_input.csv', patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op04_manual_output.csv', manual_patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op04_opencv_output.csv', opencv_patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op04_difference.csv', difference, fmt='%d', delimiter=',')

def op_05_flip_horizontal(patch):
    # operation 5: Horizontal flip
    print(f'Operation 4: Binary threshold (127)')
    print(f'Formula: I_binary = 255 if I > 127 else 0')
    
    # manual calculation
    manual_patch = np.fliplr(patch)
    print(f'Manual patch:')
    print(manual_patch)
    
    # load OpenCV output and check
    opencv_full = np.loadtxt('csv_full_image/flip_horizontal.csv', delimiter=',', dtype=int)
    opencv_patch = opencv_full[120:127, 140:147]
    
    print(f'Comparison:')
    difference = opencv_patch - manual_patch
    exact_matches = np.sum(difference == 0)
    print(f'Exact matches: {exact_matches}/49')
    
    # save csvs
    np.savetxt('csv_manual_calculations/op05_input.csv', patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op05_manual_output.csv', manual_patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op05_opencv_output.csv', opencv_patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op05_difference.csv', difference, fmt='%d', delimiter=',')

def op_06_mean_filter(patch):
    # operation 6: Mean filter (3x3)
    # Kernel: (1/9) * [[1,1,1], [1,1,1], [1,1,1]]
    print(f'Operation 6: Mean filter (3x3)')
    print(f'Kernel: (1/9) * [[1,1,1], [1,1,1], [1,1,1]]')
    
    # manual calculation
    manual_patch = np.zeros((5,5), dtype=float)
    kernel = np.ones((3,3)) / 9.0
    
    for i in range(5):
        for j in range(5):
            region = patch[i:i+3, j:j+3]
            manual_patch[i,j] = np.sum(region*kernel)
    
    manual_patch = np.round(manual_patch).astype(int)
    print(f'Manual patch (5x5 valid region):')
    print(manual_patch)
    
    # load OpenCV output and check
    opencv_full = np.loadtxt('csv_full_image/mean_filter.csv', delimiter=',', dtype=int)
    opencv_patch = opencv_full[120:127, 140:147]
    opencv_valid = opencv_patch[1:6, 1:6]
    
    print(f'Comparison:')
    difference = opencv_valid - manual_patch
    max_diff = np.max(np.abs(difference))
    print(f'\nMax diff: {max_diff}')
    
    # save csvs
    np.savetxt('csv_manual_calculations/op06_input.csv', patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op06_kernel.csv', kernel, fmt='%.4f', delimiter=',')
    np.savetxt('csv_manual_calculations/op06_manual_output.csv', manual_patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op06_opencv_output.csv', opencv_valid, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op06_difference.csv', difference, fmt='%d', delimiter=',')

def op_07_gaussian_filter(patch):
    # operation 7: Gaussian filter (3x3)
    # Kernel: (1/6) * [[1,2,1], [2,4,2], [1,2,1]]
    print(f'Operation 7: Gaussian filter (3x3)')
    print(f'Kernel: (1/6) * [[1,2,1], [2,4,2], [1,2,1]]')
    
    # manual calculation
    manual_patch = np.zeros((5,5), dtype=float)
    kernel = np.array([[1,2,1], [2,4,2], [1,2,1]]) / 16.0
    
    for i in range(5):
        for j in range(5):
            region = patch[i:i+3, j:j+3]
            manual_patch[i,j] = np.sum(region*kernel)
    
    manual_patch = np.round(manual_patch).astype(int)
    print(f'Manual patch (5x5 valid region):')
    print(manual_patch)
    
    # load OpenCV output and check
    opencv_full = np.loadtxt('csv_full_image/gaussian_filter.csv', delimiter=',', dtype=int)
    opencv_patch = opencv_full[120:127, 140:147]
    opencv_valid = opencv_patch[1:6, 1:6]
    
    print(f'Comparison:')
    difference = opencv_valid - manual_patch
    max_diff = np.max(np.abs(difference))
    print(f'\nMax diff: {max_diff}')
    
    # save csvs
    np.savetxt('csv_manual_calculations/op07_input.csv', patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op07_kernel.csv', kernel, fmt='%.4f', delimiter=',')
    np.savetxt('csv_manual_calculations/op07_manual_output.csv', manual_patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op07_opencv_output.csv', opencv_valid, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op07_difference.csv', difference, fmt='%d', delimiter=',')

def op_08_median_filter(patch):
    # operation 8: Median filter (3x3)
    print(f'Operation 8: Median filter (3x3)')
    
    # manual calculation
    manual_patch = np.zeros((5,5), dtype=int)
    for i in range(5):
        for j in range(5):
            region = patch[i:i+3, j:j+3].flatten()
            manual_patch[i,j] = np.median(region)
    print(f'Manual patch:')
    print(manual_patch)
    
    opencv_full = np.loadtxt('csv_full_image/median_filter.csv', delimiter=',', dtype=int)
    opencv_patch = opencv_full[120:127, 140:147]
    
    # extract the center region (5x5)
    if opencv_patch.shape == (7,7):
        opencv_valid = opencv_patch[1:6, 1:6]
    else:
        opencv_valid = opencv_patch
    
    print(f'Comparison:')
    difference = opencv_valid - manual_patch
        
    # stats
    max_diff = np.max(np.abs(difference))
    print(f'Max diff: {max_diff}')
    
    # save csvs
    np.savetxt('csv_manual_calculations/op08_input.csv', patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op08_manual_output.csv', manual_patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op08_opencv_output.csv', opencv_valid, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op08_difference.csv', difference, fmt='%d', delimiter=',')

def op_09_10_11_sobel(patch):
    # operations 9-11: Sobel Gx, Gy, and Magnitude
    # gx kernel: [[-1,0,1], [-2,0,2], [-1,0,1]]
    # gy kernel: [[-1,-2,-1], [0,0,0], [1,2,1]]
    print(f'Operations 9-11: Sobel Gx, Gy, and Magnitude')
    print(f'Gx kernel: [[-1,0,1], [-2,0,2], [-1,0,1]]')
    print(f'Gy kernel: [[-1,-2,-1], [0,0,0], [1,2,1]]')
    
    gx_kernel = np.array([[-1,0,1], [-2,0,2], [-1,0,1]], dtype=float)
    gy_kernel = np.array([[-1,-2,-1], [0,0,0], [1,2,1]], dtype=float)
    
    # manual calculation
    gx_patch = np.zeros((5,5), dtype=float)
    gy_patch = np.zeros((5,5), dtype=float)
    
    for i in range(5):
        for j in range(5):
            region = patch[i:i+3, j:j+3]
            gx_patch[i,j] = np.sum(region* gx_kernel)
            gy_patch[i,j] = np.sum(region*gy_kernel)
            
    magnitude = np.sqrt(gx_patch**2 + gy_patch**2)
    print(f'\nManual Gx patch (5x5):')
    print(gx_patch.astype(int))
    print(f'\nManual Gy patch (5x5):')
    print(gy_patch.astype(int))
    print(f'\nManual magnitude (5x5):')
    print(magnitude.astype(int))
    
    
    # load OpenCV output
    opencv_gx_full = np.loadtxt('csv_full_image/sobelx.csv', delimiter=',', dtype=float)
    opencv_gx_patch = opencv_gx_full[120:127, 140:147][1:6, 1:6]
    
    opencv_gy_full = np.loadtxt('csv_full_image/sobely.csv', delimiter=',', dtype=float)
    opencv_gy_patch = opencv_gy_full[120:127, 140:147][1:6, 1:6]
    
    opencv_mag_full = np.loadtxt('csv_full_image/sobel_magnitude.csv', delimiter=',', dtype=float)
    opencv_mag_patch = opencv_mag_full[120:127, 140:147][1:6, 1:6]
    
    # save csvs
    np.savetxt('csv_manual_calculations/op09_input.csv', patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op09_kernel.csv', gx_kernel, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op09_manual_output.csv', gx_patch, fmt='%.2f', delimiter=',')
    np.savetxt('csv_manual_calculations/op09_opencv_output.csv', opencv_gx_patch, fmt='%.2f', delimiter=',')
    np.savetxt('csv_manual_calculations/op09_difference.csv', opencv_gx_patch - gx_patch, fmt='%.2f', delimiter=',')
    
    np.savetxt('csv_manual_calculations/op10_input.csv', patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op10_kernel.csv', gy_kernel, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op10_manual_output.csv', gy_patch, fmt='%.2f', delimiter=',')
    np.savetxt('csv_manual_calculations/op10_opencv_output.csv', opencv_gy_patch, fmt='%.2f', delimiter=',')
    np.savetxt('csv_manual_calculations/op10_difference.csv', opencv_gy_patch - gy_patch, fmt='%.2f', delimiter=',')
    
    np.savetxt('csv_manual_calculations/op11_input.csv', patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op11_manual_output.csv', magnitude, fmt='%.2f', delimiter=',')
    np.savetxt('csv_manual_calculations/op11_opencv_output.csv', opencv_mag_patch, fmt='%.2f', delimiter=',')
    np.savetxt('csv_manual_calculations/op11_difference.csv', opencv_mag_patch - magnitude, fmt='%.2f', delimiter=',')

def op_12_13_morphology(binary_patch):
    # operations 12-13: Erosion and dilation
    # kernel: 3x3 ones
    print(f'Operations 12-13: Erosion and dilation')
    
    # manual calculation
    kernel = np.ones((3,3), dtype=int)
    
    # erosion is 1 only if all 9 pixels are 1
    erosion_patch = np.zeros((5,5), dtype=int)    
    for i in range(5):
        for j in range(5):
            region = binary_patch[i:i+3, j:j+3]
            erosion_patch[i,j] = 1 if np.all(region == 1) else 0
    
    # dilation is 1 if any pixel is 1            
    dilation_patch = np.zeros((5,5), dtype=int)    
    for i in range(5):
        for j in range(5):
            region = binary_patch[i:i+3, j:j+3]
            dilation_patch[i,j] = 1 if np.any(region == 1) else 0
                
    print(f'\nManual erosion (5x5):')
    print(erosion_patch)
    print(f'\nManual dilation (5x5):')
    print(dilation_patch)
    
    # load OpenCV output
    opencv_erosion_full = np.loadtxt('csv_full_image/erosion.csv', delimiter=',', dtype=float)
    opencv_erosion_patch = (opencv_erosion_full[120:127, 140:147] > 0).astype(int)[1:6, 1:6]
    
    opencv_dilation_full = np.loadtxt('csv_full_image/dilation.csv', delimiter=',', dtype=float)
    opencv_dilation_patch = (opencv_dilation_full[120:127, 140:147] > 0).astype(int)[1:6, 1:6]
    
    # save csvs
    np.savetxt('csv_manual_calculations/op12_input.csv', binary_patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op12_kernel.csv', kernel, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op12_manual_output.csv', erosion_patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op12_opencv_output.csv', opencv_erosion_patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op12_difference.csv', opencv_erosion_patch - erosion_patch, fmt='%d', delimiter=',')
    
    np.savetxt('csv_manual_calculations/op13_input.csv', binary_patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op13_kernel.csv', kernel, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op13_manual_output.csv', dilation_patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op13_opencv_output.csv', opencv_dilation_patch, fmt='%d', delimiter=',')
    np.savetxt('csv_manual_calculations/op13_difference.csv', opencv_dilation_patch - dilation_patch, fmt='%d', delimiter=',')

if __name__ == "__main__":
    patch, row, col = select_patch()
    op_01_neg(patch)
    op_02_brightness(patch)
    op_03_contrast(patch)
    op_04_threshold(patch)
    op_05_flip_horizontal(patch)
    op_06_mean_filter(patch)
    op_07_gaussian_filter(patch)
    op_08_median_filter(patch)
    op_09_10_11_sobel(patch)
    
    binary_patch = np.where(patch > 127, 1, 0)
    op_12_13_morphology(binary_patch)
    
    print(f'\nALL MANUAL CALCULATIONS ARE COMPLETE!')