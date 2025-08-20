import numpy
import pickle
import neural_network

tp = neural_network.thought_process.load()
print(tp[0]['hidden_weights'].flat[-1])
print(tp[1]['hidden_weights'].flat[-1])
print(tp[2]['hidden_weights'].flat[-1])
print(tp[3]['hidden_weights'].flat[-1])
print(tp[4]['hidden_weights'].flat[-1])
print(tp[5]['hidden_weights'].flat[-1])
print(tp[6]['hidden_weights'].flat[-1])
print(tp[7]['hidden_weights'].flat[-1])
