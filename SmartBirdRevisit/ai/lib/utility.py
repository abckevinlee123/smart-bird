"""
Utility functions for preprocessing, training, and visualizing the neural network
Author: Kevin Lee
"""
# utility_refactored.py
import numpy as np
import cv2
import random


def preprocess_screen(screen):
    """
    Convert the game screen to a flattened grayscale array suitable for the neural network.
    """
    oriented = np.moveaxis(screen, 1, 0)                                                    # (width[600], height[800], RGB color channel[3]) ---> (height[800], width[600], RGB color channel[3])
    grayscale = cv2.cvtColor(oriented, cv2.COLOR_RGB2GRAY)                                  # (height[800], width[600], RGB color channel[3]) ---> (height[800], width[600], gray scale value[1])
    block_size = (10, 10)                                                                   # Reduce the total pixel count by 100x
    new_width = grayscale.shape[1] // block_size[1]                                         # Divide the width side of the array by 10
    new_height = grayscale.shape[0] // block_size[0]                                        # Divide the height side of the array by 10
    resized = cv2.resize(grayscale, (new_width, new_height), interpolation=cv2.INTER_AREA)  # (height[800], width[600]) ---> (height[80], width[60])
    return resized.flatten() / 255.0                                                        # (height[80], width[60]) ---> (column[1], pixel[4800])


def evolve_thought_process(thought_process, num_neurons, rank_index):
    """
    Gradually mutate the top thought_process weights for gradual improvement.
    Currently works in-place, but ensure copying outside if needed for reproducibility.
    """
    for layer in ['hidden_weights', 'output_weights']:
        weights = thought_process[layer].copy()
        # Define mutation rate (0.01 for top1, 0.05 top2, 0.1 top3)
        mutation_rates = [0.01, 0.05, 0.1]
        mutation_rate = mutation_rates[rank_index] if rank_index < 3 else 0.05
        num_mutations = int(weights.size * mutation_rate)
        if num_mutations > 0:
            mutation_indices = np.random.choice(weights.size, num_mutations, replace=False)
            weights.flat[mutation_indices] = np.random.rand(num_mutations)
        thought_process[layer] = weights
    return thought_process