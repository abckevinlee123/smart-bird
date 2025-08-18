import numpy as np
import _pickle as pickle

class initial:
    """
    INITIAL:
    instantiating the input values
    """
    # CONSTRUCTOR: takes in the inputs, places in list
    def __init__ (self, x, y, z):
        self.input = [x, y, z]

class layer:
    """
    LAYER:
    instantiating all layers (input, hidden, output)
    math for this layers outputs (aka, the next layer's inputs)
    """
    # CONSTRUCTOR: generates the weights and biases for the next lay
    def __init__ (self, random, n_inputs, n_neurons, n_weights):
        self.inputs = n_inputs
        self.neuron = n_neurons
        self.biases = np.zeros((1, n_neurons))
        self.output = 0
        if random:
            self.weights = np.random.randn(n_inputs, n_neurons) # input nodes, hidden layer nodes, pre-transposed
        else:
            self.weights = n_weights

    # SIGMOID: realigning the output to a number between 0 and 1
    def sigmoid (self, x):
        return 1.0 / (1.0 + np.exp(-x))

    # FORWARD: calculates this particular layer's outputs using the previous layer's inputs
    def forward (self, inputs):
        self.output = self.sigmoid(np.dot(inputs, self.weights) + self.biases)

    # REFORMAT: reformating numpy list of lists into a single list (used specifically for saving the top 8 algorithms)
    def exports (self, array, size1, size2):
        a = []
        for y in range(0, size1):
            for x in range (0, size2):
                a.append(array[y, x])
        return a

    # FINAL REFORMAT: combining 2 lists into 1 (used specifically for saving the top 8 algorithms)
    def export_final (self, array1, size1, array2, size2):
        a = []
        for y in range(0, size1):
            a.append(array1[y])
        for x in range(0, size2):
            a.append(array2[x])
        return a

"""
example code:
"""
# i = initial(2, 1)
# input = i.input
# hidden = layer(2, 6)
# output = layer(6, 1)
# hidden.forward(input)
# output.forward(hidden.output)
# 
# # print(input)
# print(hidden.weights)
# # print(hidden.biases)
# print(hidden.output)

# i = initial(5, 2, 3)
# input = i.input
# hidden1 = layer(3, 5)
# hidden2 = layer(5, 5)
# hidden3 = layer(5, 5)
# output = layer(5, 1)
#
# hidden1.forward(input)
# hidden2.forward(hidden1.output)
# hidden3.forward(hidden2.output)
# output.forward(hidden3.output)


