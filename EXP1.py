import CandidateSearching as cs
import matplotlib.pyplot as plt
import os
import numpy as np
from scipy.stats import linregress

class Cell:
    def __init__(self, value, highest_layer, lowest_layer):
        self.value = value
        self.highest_layer = highest_layer
        self.lowest_layer = lowest_layer

def linear_r_squared(arr):
    if np.isnan(arr).any() or len(arr) < 2:
        return np.nan
    x = np.arange(len(arr))
    slope, intercept, r_value, p_value, std_err = linregress(x, arr)
    return r_value ** 2 if not np.isnan(r_value) else np.nan

def quadratic_r_squared(arr):
    x = np.arange(len(arr))
    coeffs = np.polyfit(x, arr, 2)
    predicted = np.polyval(coeffs, x)
    total_sum_squares = np.sum((arr - np.mean(arr))**2)
    residual_sum_squares = np.sum((arr - predicted)**2)
    r_squared = 1 - (residual_sum_squares / total_sum_squares)
    return r_squared

def O_index_visualizor(Cell_val, highest_layer, lowest_layer, array):
    result = []
    for layer in range(highest_layer, lowest_layer):
        cellA_coordinates = set()
        for row_idx, row in enumerate(array[layer]):
            for col_idx, cell_value in enumerate(row):
                if cell_value == Cell_val:
                    cellA_coordinates.add((row_idx, col_idx))
        
        cellB_coordinates = set()
        for row_idx, row in enumerate(array[layer + 1]):
            for col_idx, cell_value in enumerate(row):
                if cell_value == Cell_val:
                    cellB_coordinates.add((row_idx, col_idx))

        Overlapping_area = len(cellA_coordinates.intersection(cellB_coordinates))
        result.append((layer, Overlapping_area))
    y_values = [point[1] for point in result]   
    O_checker_result = O_checker(y_values)
    if O_checker_result == 1:
        linear_result = linear_r_squared(y_values)
        return O_checker_result, linear_result
    elif O_checker_result == -1:
        quadratic_result = quadratic_r_squared(y_values)
        return O_checker_result, quadratic_result
    elif O_checker_result == 0:
        return O_checker_result, 0
       

    '''
    # plot the figure
    x_values = [point[0] for point in result]
    y_values = [point[1] for point in result]
    plt.scatter(x_values, y_values, color='purple')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Plot of Points')
    plt.grid(True)
    plt.show()
    '''

def O_checker(arr):
    increasing = decreasing = True
    turning_point_found = False
    for i in range(1, len(arr)):
        if arr[i] > arr[i - 1]:
            decreasing = False
        elif arr[i] < arr[i - 1]:
            if increasing:
                turning_point_found = True
            increasing = False
        else:
            return 0
    if increasing or decreasing:
        return 1
    elif turning_point_found:
        return -1

def main():
    # Fill the file_path with your 2D segmentation result
    directory = '/Users/chenpeter/Desktop/AcademicMaterial/Research/Codes/Leaf/'
    cnt = 0
    passed = 0
    linear = []
    quadratic = []
    for i in range(3):
        file_name = f'Leaf_{i:02d}_masks.npy'
        file_path = os.path.join(directory, file_name)
        if os.path.exists(file_path):
            array = cs.load_array(file_path)
            cell_dict = cs.extract_cells_info(array)
            for cell_val, cell_info in cell_dict.items():
                cnt += 1
                num, linearity = O_index_visualizor(cell_val, cell_info.highest_layer, cell_info.lowest_layer, array)
                passed += abs(num)
                if num == 1 and not np.isnan(linearity):
                    linear.append(linearity)
                elif num == -1:
                    quadratic.append(linearity)
    print(f"Number of total cell: {cnt}")
    print(f"Number of total cells that passed all the strict criterion: {passed}")
    print(f"Linear Type: mean of R^2: {np.mean(linear)}")
    print(f"Linear Type: std of R^2: {np.std(linear)}")
    print(f"Quadratic Type: mean of R^2: {np.mean(quadratic)}")
    print(f"Quadratic Type: std of R^2: {np.std(quadratic)}")
if __name__ == "__main__":
    main()