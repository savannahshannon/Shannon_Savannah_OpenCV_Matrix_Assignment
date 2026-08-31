import numpy as np 
import pandas as pd 
import os

def verify_ops():
    operations = [
        ('op01', 'Negative', True),
        ('op02', 'Brightness', True),
        ('op03', 'Contrast', True),
        ('op04', 'Threshold', True),
        ('op05', 'Horizontal flip', True),
        ('op06', 'Mean filter', True),
        ('op07', 'Gaussian filter', True),
        ('op08', 'Median filter', True),
        ('op09', 'Sobel Gx', True),
        ('op10', 'Sobel Gy', True),
        ('op11', 'Sobel magnitude', True),
        ('op12', 'Erosion', True),
        ('op13', 'Dilation', True),
    ]
    
    results = []
    
    for op_id, op_name, exact_match in operations:
        try: 
            manual_patch = f'csv_manual_calculations/{op_id}_manual_output.csv'
            opencv_patch = f'csv_manual_calculations/{op_id}_opencv_output.csv'
            
            manual = np.loadtxt(manual_patch, delimiter=',')
            opencv = np.loadtxt(opencv_patch, delimiter=',')
            
            difference = opencv - manual
            max_diff = np.max(np.abs(difference))
            mean_diff = np.mean(np.abs(difference))
            exact_matches = np.sum(difference == 0)
            total_cells = difference.size
            percent_match = (exact_matches / total_cells) * 100

            np.savetxt(f'csv_manual_calculations/{op_id}_difference.csv', difference, fmt='%.2f', delimiter=',')
            
            print(f'\n{op_id}: {op_name}')
            print(f'Max diff: {max_diff:.2f}')
            print(f'Mean diff: {mean_diff:.4f}')
            print(f'Exact matches: {exact_matches}/{total_cells} ({percent_match:.1f}%)')
            
            if exact_match:
                status = 'Pass' if max_diff == 0 else 'Close'
            else:
                status = 'Pass' if max_diff <= 1.0 else 'Acceptable' if max_diff <= 2.0 else 'Check'
                
            print(f'Status: {status}')
            
            results.append({
                'Operation': op_name,
                'Max_diff': max_diff,
                'Mean_diff': mean_diff,
                'Exact_matches': f'{exact_matches}/{total_cells}',
                'Percent_match': f'{percent_match:.1f}',
                'Status': status
            })
        except Exception as e:
            print(f'\n{op_id}: {op_name} - ERROR: {e}')
    
    # save summary to csv
    summary_df = pd.DataFrame(results)
    summary_df.to_csv('csv_manual_calculations/verification_summary.csv', index=False)
    
    
if __name__ == "__main__":
    verify_ops()