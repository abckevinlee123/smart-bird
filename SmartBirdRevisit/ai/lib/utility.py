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
    for layer in ['hidden_weights', 'output_weights', 'hidden_biases', 'output_biases']:
        param = thought_process[layer].copy()
        mutation_rates = [0.1, 0.15, 0.2]
        if score < 50:
            mutation_rates = np.array(mutation_rates) * 5                                   # Increase mutation rates arbitrarily for scores that dont come close to the pipe
        elif score < 60:
            mutation_rates = np.array(mutation_rates) * 2                                   # Increase mutation rates arbitrarily for scores that barely enter the pipe
        mutation_rate = mutation_rates[rank_index]
        num_mutations = int(param.size * mutation_rate)
        if num_mutations > 0:
            mutation_indices = np.random.choice(param.size, num_mutations, replace=False)
            param.flat[mutation_indices] += np.random.randn(num_mutations) * 0.5            # Instead of outright replacing, add a small random value to the existing weight/bias (scaled by half a standard deviation)
        thought_process[layer] = param
    return thought_process

def visualize_thought_process(fig, ax1, ax2, thought_process):
    """
    Visualize the weights of the neural network layers as grayscale images.
    This version updates an existing figure instead of creating a new one.
    """
    # --- 1. Clear the previous images ---
    ax1.clear()
    ax2.clear()

    if 'hidden_weights' not in thought_process:
        return

    hidden_weights = thought_process['hidden_weights']
    output_weights = thought_process['output_weights']

    def best_2d_shape(size):
        if size == 0: return (1, 1)
        for i in range(int(np.sqrt(size)), 0, -1):
            if size % i == 0:
                return (i, size // i)
        return (1, size) # Fallback for prime numbers

    hidden_shape = best_2d_shape(hidden_weights.size)
    output_shape = best_2d_shape(output_weights.size)

    hidden_image = hidden_weights.reshape(hidden_shape)
    output_image = output_weights.reshape(output_shape)

    # --- 2. Redraw the new images ---
    ax1.set_title('Hidden Layer Weights')
    ax1.imshow(hidden_image, cmap='gray', aspect='auto')
    ax1.axis('off')

    ax2.set_title('Output Layer Weights')
    ax2.imshow(output_image, cmap='gray', aspect='auto')
    ax2.axis('off')

    # --- 3. Update the window without blocking ---
    fig.tight_layout()
    fig.canvas.draw()
    fig.canvas.flush_events()