"""
Tools necessary to aid in the creation and teaching of the neural network
Author: Kevin Lee
"""
import numpy as np
import pickle

class layer:
    """
    LAYER:
    Given certain parameters, design a layer.
    """
    # CONSTRUCTOR: generate the layer structure given the previous layer's no. of outputs(inp), no. of neurons(neu), possibly the previous weights (pre_wei), and possibly the pre-determined biases(est_bia)
    def __init__ (self, random, no_inputs, no_neurons, pre_weights, est_biases):
        self.inputs = no_inputs
        self.neurons = no_neurons
        self.output = 0
        if random:
            # WEIGHTS: Create an array of arrays (according to the number of parameters) in normal distribution:
            # np.random.randn(2, 4)
            # array([[-1.59022344, -0.05409669, -0.40128521,  0.62704859], 
            # [ 0.90419252,  0.83106465, -0.54859216,  1.50170964]])
            self.weights = np.random.randn(self.inputs, self.neurons)

            # BIASES: Unless otherwise pre-established, there should be NO biases being randomly generated:
            # np.zeros((2,4)) <-- NEED BOTH PARENTHESIS, np.zeros() REQUIRES A TUPLE
            # array([[0., 0., 0., 0.],
            # [0., 0., 0., 0.]])
            self.biases = np.zeros((1, self.neurons))
        else:
            self.weights = pre_weights
            self.biases = est_biases

    # SIGMOID: realigning the output to a number between 0(when x is negative) and 1(when x is positive), with y = 0.5 when x = 0
    def sigmoid (self, x):
        return 1.0 / (1.0 + np.exp(-x))

    # RELU: piece-wise function for the output being either the chosen number or 0 (if the number is less than 0), less computationally draining than sigmoid and avoid vanishing gradient problem
    def relu (self, x):
        return np.maximum(x, 0)

    # LEAKY RELU: piece-wise function for the output being either the chosen number or 
    def lrelu(self, x):
        return np.maximum(x, 0.01*x)

    # FORWARD: calculates this particular layer's outputs using the previous layer's inputs
    def forward (self, inputs):
        self.output = self.lrelu(np.dot(inputs, self.weights) + self.biases)
        return self.output

class model:
    """
    MODEL:
    Creates the layers and generates the layer outputs
    """
    # CONSTRUCTOR: using the model details, construct the neural network model taking in 4800 pixels as inputs, the number of nodes the users wants, and then an output layer with yes or now (2 nodes)
    def __init__(self, random, best_thought_process, user_input):
        if random:
            # HIDDEN LAYER: 4800 inputs which is, user_input number of neurons, no pre_weights, no est_biases
            self.hidden_layer = layer(True, 4800, user_input, 0, 0)
            self.output_layer = layer(True, user_input, 2, 0, 0)
        else:
            # print("HW:",best_thought_process['hidden_weights'])
            # print("OW:",best_thought_process['output_weights'])
            self.hidden_layer = layer(False, 4800, user_input, best_thought_process['hidden_weights'], best_thought_process['hidden_biases'])
            self.output_layer = layer(False, user_input, 2, best_thought_process['output_weights'], best_thought_process['output_biases'])

    # FORWARD: Given the state of the game, calculate the output of the neural network
    def forward(self, state):
        input_image = state
        hidden_output = self.hidden_layer.forward(input_image)
        output = self.output_layer.forward(hidden_output)
        return output

class thought_process:
    def format (fitness_score, hidden_weights, hidden_biases, output_weights, output_biases, user_input):
        form = [  ('fitness_score', np.int32), 
                    ('hidden_weights', np.float64, (4800,user_input)), 
                    ('hidden_biases', np.float64, (1,user_input)), 
                    ('output_weights', np.float64, (user_input,2)), 
                    ('output_biases', np.float64, (1,2))]
        thought_process = np.empty((), dtype=form)
        thought_process['fitness_score'] = fitness_score
        thought_process['hidden_weights'] = hidden_weights
        thought_process['hidden_biases'] = hidden_biases
        thought_process['output_weights'] = output_weights
        thought_process['output_biases'] = output_biases
        return thought_process

    def save (thought_processes):
        with open("test.pkl", "wb") as f:
            pickle.dump(thought_processes, f)

    def load ():
        with open("test.pkl", "rb") as f:
            return pickle.load(f)
