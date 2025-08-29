import pygame
import random
import os
import time
import sys

"""
NEURAL NETWORK LIBRARIES
"""
# import neural_network
# import training_simulation

"""
NEURAL NETWORK LIBRARIES
"""
# VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS 
# VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS 
# VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS 
# VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS 

# VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS 
# VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS 
# VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS 
# VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS # VARIABLES FOR LIVES AND GRAPHS 

pygame.font.init()

WIN_WIDTH = 600
WIN_HEIGHT = 800
FLOOR = 730
STAT_FONT = pygame.font.Font("./font/flappy-bird-font.ttf", 25)
END_FONT = pygame.font.SysFont("comicsans", 50)
DRAW_LINES = False

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Smart Bird")

pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")).convert_alpha())
bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (600, 900))
bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird" + str(x) + ".png"))) for x in range(1,4)]
base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")).convert_alpha())

lives_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","lives.png")).convert_alpha(), (160, 56))
neuron_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","neuron.png")).convert_alpha(), (160, 56))
epoch_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","epoch.png")).convert_alpha(), (160, 56))
blank_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","blank.png")).convert_alpha(), (160, 56))

class Bird:
    MAX_ROTATION = 25
    IMGS = bird_images
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0 
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = 7.7
        self.tick_count = 0
        self.height = self.y

    def move(self):
        direction = 1
        if self.vel < 0:
            direction = -1
        if self.vel > -7:
            displacement = (self.vel ** 2) * (0.6) * direction
            self.y -= displacement
        else:
            self.y += 20 *1.25
        self.vel -= 1.1

        if self.y < self.height:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        blitRotateCenter(win, self.img, (self.x, self.y), self.tilt)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200
    VEL = 8

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(pipe_img, False, True)
        self.PIPE_BOTTOM = pipe_img

        self.passed = False

        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))


    def collide(self, bird, win):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if b_point or t_point:
            return True

        return False

class Base:
    VEL = 8
    WIDTH = base_img.get_width()
    IMG = base_img

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def blitRotateCenter(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)

def plot(win):
    plt.imshow(win)
    plt.show()

def draw_window(win, bird, pipes, base, pipe_ind):
    win.blit(bg_img, (0,0))

    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)

    bird.draw(win)

    pygame.display.update()

def draw_menu(bird, base, input, input2, input3):
    win.blit(bg_img, (0,0))

    base.draw(win)

    bird.draw(win)

    IMG_WIDTH = blank_img.get_width()
    IMG_HEIGHT = blank_img.get_height()
    win.blit(neuron_img, (((WIN_WIDTH/2) - IMG_WIDTH -  20), (50)))
    win.blit(blank_img, (((WIN_WIDTH/2) + 20), (50)))

    win.blit(lives_img, (((WIN_WIDTH/2) - IMG_WIDTH -  20), (125)))
    win.blit(blank_img, (((WIN_WIDTH/2) + 20), (125)))

    win.blit(epoch_img, (((WIN_WIDTH/2) - IMG_WIDTH -  20), (200)))
    win.blit(blank_img, (((WIN_WIDTH/2) + 20), (200)))
    
    text = STAT_FONT.render(input,1,(255,255,255))
    text2 = STAT_FONT.render(input2,1,(255,255,255))
    text3 = STAT_FONT.render(input3,1,(255,255,255))
    TXT_WIDTH = text.get_width()
    TXT_HEIGHT = text.get_height()

    win.blit(text, (((WIN_WIDTH/2) + IMG_WIDTH/2 + 22 - (TXT_WIDTH/2)), (49 + (IMG_HEIGHT/2) - (TXT_HEIGHT/2))))
    win.blit(text2, (((WIN_WIDTH/2) + IMG_WIDTH/2 + 22 - (TXT_WIDTH/2)), (124 + (IMG_HEIGHT/2) - (TXT_HEIGHT/2))))
    win.blit(text3, (((WIN_WIDTH/2) + IMG_WIDTH/2 + 22 - (TXT_WIDTH/2)), (199 + (IMG_HEIGHT/2) - (TXT_HEIGHT/2))))

    pygame.display.update()

def menu_screen():
    # MENU
    clock = pygame.time.Clock()
    text = ""
    text2 = ""
    text3 = ""
    menu = True
    entering = 1  # track which field we’re on

    bird = Bird(210,350)
    base = Base(FLOOR)

    while menu:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        if entering == 1:
                            user_neuron_input = int(text)
                            if user_neuron_input < 400:
                                entering = 2  # now move to text2
                            # else:
                                # POPUP
                        elif entering == 2:
                            user_lives_input = int(text2)
                            entering = 3 # now move to text3
                        else:
                            user_epoch_input = int(text3)
                            menu = False
                            run = True
                    except ValueError:
                        text = ""
                        text2 = ""
                        text3 = ""
                elif event.key == pygame.K_BACKSPACE:
                    if entering == 1:
                        text = text[:-1]
                    elif entering == 2:
                        text2 = text2[:-1]
                    else:
                        text3 = text3[:-1]
                elif event.unicode.isdigit():
                    if entering == 1:
                        text += event.unicode
                    elif entering == 2:
                        text2 += event.unicode
                    else:
                        text3 += event.unicode

        base.move()
        draw_menu(bird, base, text, text2, text3)
    return (user_neuron_input, user_lives_input, user_epoch_input)


"""CODE FOR TESTING
class ReplayBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = []
    
    def add(self, experience):
        self.buffer.append(experience)
        if len(self.buffer) > self.capacity:
            self.buffer.pop(0)
    
    def sample(self, batch_size):
        indices = np.random.choice(len(self.buffer), batch_size, replace=False)
        return [self.buffer[idx] for idx in indices]

# Initialize DQN and ReplayBuffer
input_shape = (60, 80)  # Adjust based on your preprocessing
num_actions = 2  # Jump or not jump
dqn = DQN(input_shape=input_shape, num_actions=num_actions)
replay_buffer = ReplayBuffer(capacity=10000)

# Training parameters
epsilon = 1.0
min_epsilon = 0.1
epsilon_decay = 0.995
gamma = 0.99
batch_size = 32

# Training loop
for episode in range(num_episodes):
    # Initialize game environment and state
    state = initialize_game()
    done = False
    
    while not done:
        # Preprocess current state
        processed_state = preprocess(state)
        
        # Forward pass through DQN
        q_values = dqn.forward(processed_state)
        
        # Choose action using epsilon-greedy policy
        action = get_action(q_values, epsilon)
        
        # Execute action in the game and observe next state and reward
        next_state, reward, done = execute_action(action)
        
        # Store transition in replay buffer
        experience = (processed_state, action, reward, preprocess(next_state), done)
        replay_buffer.add(experience)
        
        # Sample random minibatch from replay buffer
        minibatch = replay_buffer.sample(batch_size)
        states, actions, rewards, next_states, terminals = zip(*minibatch)
        
        # Compute targets
        target_q_values = rewards + gamma * np.max(dqn.forward(next_states), axis=1) * (1 - terminals)
        
        # Compute loss and update DQN
        loss = compute_loss(dqn, states, actions, target_q_values)
        dqn.backward(loss)
        
        # Update exploration rate
        if epsilon > min_epsilon:
            epsilon *= epsilon_decay
        
        state = next_state  # Move to next state
    
    # Periodically update target network weights (if using Double DQN)
    if episode % target_update_frequency == 0:
        target_dqn.update_weights(dqn.get_weights())
"""
