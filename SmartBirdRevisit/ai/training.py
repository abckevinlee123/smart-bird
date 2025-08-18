"""
Tools necessary to aid in the creation and teaching of the neural network
Author: Kevin Lee
"""
import numpy as np
import cv2 # For image filtering tools
from collections import deque
import random

# PREPROCESSING: Filtering the image in an effort to remove computational load while maintaining the integrity of the image data
def preprocessing(screen):
    # Extract 3D array of the game window (width[600], height[800], RGB color channel[3])
    image_arr = screen
    
    # Change shape order to height x width x color: (width[600], height[800], RGB color channel[3]) ---> (height[800], width[600], RGB color channel[3])
    orientated_image = np.moveaxis(image_arr, 1, 0)
    
    # Change the values of the color to gray scale: (height[800], width[600], RGB color channel[3]) ---> (height[800], width[600], gray scale value[1])
    grayscale_image = cv2.cvtColor(orientated_image, cv2.COLOR_RGB2GRAY) 

    # Reduce the total pixel count by 100x: (height[800], width[600]) ---> (height[80], width[60])
    block_size = (10,10) # 10 x 10 pixel box
    new_width = grayscale_image.shape[1] // block_size[1] # 
    new_height = grayscale_image.shape[0] // block_size[0] # 
    resized_image = cv2.resize(grayscale_image, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # For the neural network to do operations properly, the array should be in a 1 x 4800: (height[80], width[60]) ---> (column[1], pixel[4800])
    final_image = resized_image.flatten()

    return(final_image) 

# REPLACE WEIGHTS: Replace the weights of the neural network with the new weights
# def replace_weights(model, new_weights):


# class replay:
#     """
#     REPLAY:
#     A collection of "experiences" 
#     """
#     # CONSTRUCTOR: An array with size (1, max_size). When full, .pops() the oldest experiences, and appends the most recent collected experience
#     def __init__(self, max_size):
#         self.buffer = deque(maxlen=max_size)
    
#     # ADD: Collects the state (preprocessed game frame), action (bool jump or not), reward (at that instant game frame), next_state (the next game frame), and done (bool game over or not)
#     def add(self, state, action, reward, next_state, done):
#         experience = (state, action, reward, next_state, done)
#         self.buffer.append(experience)
    
#     # SAMPLE: Returns a batch_size number of experiences (an array of the aforementioned states, actions, rewards, etc.) 
#     def sample(self, batch_size):
#         batch = random.sample(self.buffer, batch_size)
#         states, actions, rewards, next_states, dones = map(np.array, zip(*batch))
#         return states, actions, rewards, next_states, dones
    
#     # LEN: Returns buffer size
#     def __len__(self):
#         return len(self.buffer)

# # GET ACTION: Choose between a random value for the neural network to take, or the neural network calculated value
# def get_action(q_value, epsilon):
#     # Random action
#     if np.random.rand() < epsilon:
#         return np.random.randint(len(q_value))
#     # Greedy action
#     else:
#         return q_value

# # TRAIN MODEL: Given 
# def train_model(env, model, target_model, replay_buffer, num_episodes, gamma=0.99, epsilon=1.0, min_epsilon=0.1, epsilon_decay=0.995, batch_size=32):
#     total_rewards = []
#     for episode in range(num_episodes):
#         state = env.reset()
#         total_reward = 0
#         done = False
#         while not done:
#             if np.random.rand() < epsilon:
#                 action = env.action_space.sample()
#             else:
#                 q_values = model.predict(state)
#                 action = np.argmax(q_values)

#             next_state, reward, done, _ = env.step(action)
#             replay_buffer.add(state, action, reward, next_state, done)

#             state = next_state
#             total_reward += reward

#             if len(replay_buffer) > batch_size:
#                 batch = replay_buffer.sample(batch_size)
#                 states, actions, rewards, next_states, dones = zip(*batch)

#                 states = np.array(states)
#                 actions = np.array(actions)
#                 rewards = np.array(rewards)
#                 next_states = np.array(next_states)
#                 dones = np.array(dones)

#                 current_q_values = model.predict(states)
#                 next_q_values = target_model.predict(next_states)

#                 target_q_values = current_q_values.copy()
#                 for i in range(batch_size):
#                     target_q_values[i, actions[i]] = rewards[i] + gamma * np.max(next_q_values[i]) * (1 - dones[i])

#                 model.update(states, target_q_values)

#         total_rewards.append(total_reward)
#         epsilon = max(min_epsilon, epsilon * epsilon_decay)

#         # Update target model
#         if episode % 10 == 0:
#             target_model = deepcopy(model)

#         print(f"Episode: {episode}, Total Reward: {total_reward}, Epsilon: {epsilon}")

#     return total_rewards

# # Hyperparameters
# gamma = 0.99
# epsilon = 1.0
# epsilon_min = 0.01
# epsilon_decay = 0.995
# batch_size = 64
# memory_capacity = 10000
# learning_rate = 0.001
# num_episodes = 1000