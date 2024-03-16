import numpy as np
import ot

"""
Different attributes we need to store for a cell

Parameters:
value: (int) the value of cell in 2D segmentation numpy
highest_layer: (int) the highest layer of the cell 
lowest_layer: (int) the lowest layer of the cell
"""
class Cell:
    def __init__(self, value, highest_layer, lowest_layer):
        self.value = value
        self.highest_layer = highest_layer
        self.lowest_layer = lowest_layer

"""
Read in the file

Parameters:
file_path: (str) the path of 2D segmentation numpy file
"""
def load_array(file_path):
    try:
        return np.load(file_path)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print("An error occurred while loading the array:", e)
    return None

"""
For class Cell, fills in the info for each specific cell in 2D segmentation 
numpy file

Parameters:
array: (3D np array) result of 2D segmentation numpy file
"""
def extract_cells_info(array):
    cell_dict = {}

    if array is None:
        return cell_dict
    
    for i in range(array.shape[0]):
        layer = array[i]

        for row_idx, row in enumerate(layer):
            for col_idx, cell_value in enumerate(row):
                # Empty spot without cell
                if cell_value == 0:
                    continue
                # A new cell is detected, create a new instance for this cell
                if cell_value not in cell_dict:
                    cell_dict[cell_value] = Cell(cell_value, i, i)
                else:
                    # Update the cell info
                    cell_dict[cell_value].lowest_layer = max(cell_dict[cell_value].lowest_layer, i)
                    cell_dict[cell_value].highest_layer = min(cell_dict[cell_value].highest_layer, i)

    return cell_dict

"""
Jaccard index calculator for cell mask A and cell mask B

Parameters:
array: (3D np array) result of 2D segmentation numpy file
layerA: (int) the number of layer that cell mask A resides
layerB: (int) the number of layer that cell mask B resides
CellA_val: (int) the np value of cell A
CellB_val: (int) the np value of cell B
"""
def jaccard_index_calc(array, layerA, layerB, CellA_val, CellB_val):
    # Collect all the coordinates of Cell mask A
    cellA_coordinates = set()
    for row_idx, row in enumerate(array[layerA]):
        for col_idx, cell_value in enumerate(row):
            if cell_value == CellA_val:
                cellA_coordinates.add((row_idx, col_idx))
    
    # Collect all the coordinates of Cell mask B
    cellB_coordinates = set()
    for row_idx, row in enumerate(array[layerB]):
        for col_idx, cell_value in enumerate(row):
            if cell_value == CellB_val:
                cellB_coordinates.add((row_idx, col_idx))
    
    # Calculate the intersection and union of Cell mask A and Cell mask B
    intersection = len(cellA_coordinates.intersection(cellB_coordinates))
    union = len(cellA_coordinates.union(cellB_coordinates))
    
    if union == 0: 
        return 0.0
    jaccard_index = intersection / union
    return jaccard_index

"""
Find the candidates of pairs of cells that could have a missing mask 

Parameters:
cell_dict: (dict) A dictionary that contains three attributes for each cell
array: (3D np array) result of 2D segmentation numpy file
"""
def missing_mask_search(cell_dict, array):
    missing_cell_pairs = []
    # Detect whether there's a one-layer gap between two cells 
    for cell_A_key, cell_A in cell_dict.items():
        for cell_B_key, cell_B in cell_dict.items():
            if cell_A_key != cell_B_key:  
                if cell_B.highest_layer - cell_A.lowest_layer == 2:
                    missing_cell_pairs.append((cell_A_key, cell_B_key))
    
    missing_cell_pairs_final = []
    # Detect whether two cells are overlapped (jarccard index > 0)
    for cell_A_key, cell_B_key in missing_cell_pairs:
        cell_A = cell_dict[cell_A_key] 
        cell_B = cell_dict[cell_B_key] 
        jaccard_index = jaccard_index_calc(array, cell_A.highest_layer, cell_B.lowest_layer, cell_A.value, cell_B.value)
        if jaccard_index > 0:
            missing_cell_pairs_final.append((cell_A, cell_B))
    return  missing_cell_pairs_final

"""
Using the OT match in CellStitch to consider the situation that
not all the cells are one-to-one correspondent 

Parameters:
candidates: (2D array) storing the primary candidate for further processing
array: (3D np array) result of 2D segmentation numpy file
"""
def one_to_one_correspondence_check(candidates,array):
    final_candidate = []
    for layer in range(array.shape[0]):
        lowest_layer_set = []
        highest_layer_set = []
        for candidate in candidates:
            if candidate[0].lowest_layer == layer and candidate[0] not in lowest_layer_set:
                lowest_layer_set.append(candidate[0])
            if candidate[1].highest_layer == layer + 2 and candidate[1] not in highest_layer_set:
                highest_layer_set.append(candidate[1])

        # If it's possible for a cell mask to be matched by multiple other masks
        if len(lowest_layer_set) > 1 or len(highest_layer_set) > 1:
            lowest_layer_size = []
            highest_layer_size = []
            for cell in lowest_layer_set:
                lowest_layer_size.append(np.count_nonzero(array[layer] == cell.value))
            for cell in highest_layer_set:
                highest_layer_size.append(np.count_nonzero(array[layer + 2] == cell.value))

            # Preparing for OT distribution setting
            sum_lowest_layer_size = sum(lowest_layer_size)
            sum_highest_layer_size = sum(highest_layer_size)
            normalized_lowest_layer_size = [size / sum_lowest_layer_size for size in lowest_layer_size]
            normalized_highest_layer_size = [size / sum_highest_layer_size for size in highest_layer_size]
            
            # Calculate the cost matrix for OT
            Cost_Matrix = np.zeros((len(lowest_layer_set), len(highest_layer_set)))
            for i in range(len(lowest_layer_set)):
                for j in range(len(highest_layer_set)):
                    CellA_val = lowest_layer_set[i].value
                    CellB_val = highest_layer_set[j].value
                    # 1 - Jaccard Index as the cost for transportation
                    Cost_Matrix[i, j] = 1 - jaccard_index_calc(array, layer, layer + 2, CellA_val, CellB_val)
            # Solve the OT plan
            OT_plan = ot.emd(normalized_lowest_layer_size, normalized_highest_layer_size, Cost_Matrix)
            n, m = len(OT_plan), len(OT_plan[0])
            soft_matching = np.zeros((n, m))
            # Match the cell from n to m by finding the argmax of the OT_plan
            for i in range(n):
                soft_matching[i, OT_plan[i].argmax()] = 1
            # Reversely match the cell from m to n to find the one with least transportation cost
            for i in range(m):
                # If multiple cells in n are matched with ith cell in m
                if np.sum(soft_matching[:, i]) > 1:
                    soft_matching[np.argmax(soft_matching[:, i]), i] += 1
                    for j in range(n):
                        soft_matching[j, i] = max(0, soft_matching[j, i] - 1)
            for i in range(n):
                for j in range(m):
                    if(soft_matching[i, j] == 1):
                        final_candidate.append((lowest_layer_set[i],highest_layer_set[j]))
    return final_candidate


def print_cells_info(cell_dict):
    if not cell_dict:
        print("No cell information available.")
        return
    
    for cell_value, cell_info in cell_dict.items():
        print(f"Cell value: {cell_info.value}, Highest layer: {cell_info.highest_layer}, Lowest layer: {cell_info.lowest_layer}")


def print_candidates(candidates):
    if len(candidates) == 0:
        print("None")
    else:
        print(candidates)

def main():
    # Fill the file_path with your 2D segmentation result
    file_path = '/Users/chenpeter/Desktop/SimulatedData/Leaf_00_masks_R.npy'
    array = load_array(file_path)
    cell_dict = extract_cells_info(array)
    #print_cells_info(cell_dict)
    primary_candidates = missing_mask_search(cell_dict, array)
    final_candidates = one_to_one_correspondence_check(primary_candidates,array)
    print_candidates(final_candidates)


if __name__ == "__main__":
    main()