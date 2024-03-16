import numpy as np
import random
import matplotlib.colors as mcolors
from matplotlib import pyplot as plt

def remove_layer_pixels(array, layer_index):
    #value_to_remove = random.choice(unique_values)
    value_to_remove = 6413
    pixels_to_remove = np.argwhere(array[layer_index] == value_to_remove)
    for pixel in pixels_to_remove:
        array[layer_index, pixel[0], pixel[1]] = 0
    changed_np_val = np.max(array)
    for i in range(layer_index + 1, len(array)):
        array[i][array[i] == value_to_remove] = changed_np_val + 500
    return array

def visualize():
    data = np.load('/Users/chenpeter/Desktop/SimulatedData/Leaf_00_masks_R.npy')
    data_max = np.max(data)
    data_min = np.min(data)
    num_slices = data.shape[0]
    cmap = plt.cm.inferno
    norm = mcolors.Normalize(vmin=data_min, vmax=data_max)
    for i in range(num_slices):
        plt.figure(figsize=(8, 6))
        plt.imshow(data[i], cmap=cmap, norm=norm)
        plt.colorbar()
        plt.title(f'Heatmap of Slice {i}')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.show()

def main():
    input_file_path = '/Users/chenpeter/Desktop/Leaf/Leaf_00_masks.npy'
    output_file_path = '/Users/chenpeter/Desktop/SimulatedData/Leaf_00_masks_R.npy'
    array = np.load(input_file_path)
    modified_array = remove_layer_pixels(array, 4)
    np.save(output_file_path, modified_array)
    visualize()

if __name__ == "__main__":
    main()
