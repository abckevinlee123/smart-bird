"""
Utility functions for preprocessing, training, and visualizing the neural network
Author: Kevin Lee
"""
import numpy as np                  # For linear algebra computation
import cv2                          # For image filtering tools
import random

# PREPROCESSING: Filtering the image in an effort to remove computational load while maintaining the integrity of the image data.
#                Each "pixel" will then be fed into the neural network.
def preprocessing(screen):
    # Extract 3D array of the game window, every pixel
    # (width[600], height[800], RGB color channel[3])
    image_arr = screen

    # Change orientation of the image from width * height to height * width
    # (width[600], height[800], RGB color channel[3]) ---> (height[800], width[600], RGB color channel[3])
    orientated_image = np.moveaxis(image_arr, 1, 0)

    # Change the values of the color to gray scale
    # (height[800], width[600], RGB color channel[3]) ---> (height[800], width[600], gray scale value[1])
    grayscale_image = cv2.cvtColor(orientated_image, cv2.COLOR_RGB2GRAY) 

    # Reduce the total pixel count by 100x
    # (height[800], width[600]) ---> (height[80], width[60])
    block_size = (10,10)                                        # 10 x 10
    new_width = grayscale_image.shape[1] // block_size[1]       # Divide the width side of the array by 10
    new_height = grayscale_image.shape[0] // block_size[0]      # Divide the height side of the array by 10
    resized_image = cv2.resize(grayscale_image, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # For the neural network to do operations properly, the array should be in a 1 * 4800 shape
    # (height[80], width[60]) ---> (column[1], pixel[4800])
    final_image = resized_image.flatten()

    return(final_image) 

# EVOLUTION: Replace some of the weights so that the model can gradually improve
def evolution(thought_process, neurons, chosen):
    # Run twice to change values of hidden weights and output weights
    for y in range(2):
        if y == 0:
            weights = 'hidden_weights'
        else:
            weights = 'output_weights'
        position = chosen+1
        new_weight = thought_process[weights]
        num_of_elements = int(new_weight.size * 0 * (position*1))   ## THIS SHOULD NOT BE 0, BUT IT WORKS WITH MULTIPLYING BY 0
        random_positions = np.random.choice(new_weight.size, num_of_elements, replace=False)
        new_weight.flat[random_positions] = np.random.rand(num_of_elements)
        thought_process[weights] = new_weight
    return thought_process
