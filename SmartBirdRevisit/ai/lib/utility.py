"""
Utility functions for preprocessing, training, and visualizing the neural network
Author: Kevin Lee
"""
# utility_refactored.py
import numpy as np
import cv2
import random
import matplotlib.pyplot as plt

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


def evolve_thought_process(thought_process, num_neurons, rank_index, score):
    """
    Gradually mutate the top thought_process weights for gradual improvement.
    Currently works in-place, but ensure copying outside if needed for reproducibility.
    """
    for layer in ['hidden_weights', 'output_weights']:
        weights = thought_process[layer].copy()
        mutation_rates = [0.01, 0.05, 0.1]
        if score < 500:
            mutation_rates *= 8                                                           # Increase mutation rates for scores that dont contribute to pipe passing
        mutation_rate = mutation_rates[rank_index]
        num_mutations = int(weights.size * mutation_rate)
        if num_mutations > 0:
            mutation_indices = np.random.choice(weights.size, num_mutations, replace=False)
            weights.flat[mutation_indices] = np.random.rand(num_mutations)
        thought_process[layer] = weights
    return thought_process

def visualize_thought_process(thought_process):
    """
    Visualize the weights of the neural network layers as grayscale images.
    """
    hidden_weights = thought_process['hidden_weights']
    output_weights = thought_process['output_weights']

    hidden_size = int(np.sqrt(hidden_weights.size))
    output_size = int(np.sqrt(output_weights.size))

    hidden_image = hidden_weights.reshape((hidden_size, hidden_size))
    output_image = output_weights.reshape((output_size, output_size))

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.title('Hidden Layer Weights')
    plt.imshow(hidden_image, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.title('Output Layer Weights')
    plt.imshow(output_image, cmap='gray')
    plt.axis('off')

    plt.show()