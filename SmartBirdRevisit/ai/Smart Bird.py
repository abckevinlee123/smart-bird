import pygame
import game
import training
import neural_network
import numpy as np  # For array manipulation
# import matplotlib.pyplot as plt # For visualizing images in array format

best_thought_processes = [neural_network.thought_process.format(0, 0, 0, 0, 0, 0) for _ in range(8)]
graphs = 0

def game_start(user_input, random):
    # GAME VARIABLES
    clock = pygame.time.Clock()
    floor = game.FLOOR
    bird = game.Bird(210,350)
    base = game.Base(floor)
    pipes = [game.Pipe(700)]
    win = game.win

    """ 
    NEURAL NETWORK VARIABLES
    """
    if not random:
        model = neural_network.model(random, best_thought_processes[0], user_input)
    model = neural_network.model(random, 0, user_input)
    fitness_score = 0

    # Training parameters
    # epsilon = 1.0                           # Exploration rate
    # min_epsilon = 0.1                       # Minimum exploration rate    
    # epsilon_decay = 0.995                   # Decay rate for exploration
    # gamma = 0.99                            # Discount factor for future rewards
    # batch_size = 32                         # Size of the batch for training
    """ 
    NEURAL NETWORK VARIABLES
    """

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
                break

        pipe_ind = 0
        game.draw_window(win, bird, pipes, base, pipe_ind)

        if len(pipes) > 1 and bird.x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
            pipe_ind = 1 

        if bird.y + bird.img.get_height() >= floor or bird.y < -220:
            run = False
            break

        bird.move()
      
        base.move()

        rem = []
        add_pipe = False
        """
        GRAB SCREEN DATA WITH PREPROCESSING
        """
        # Grabbing the screen data and converting it to a preprocessed array of 4800 pixels
        state = training.preprocessing(pygame.surfarray.array3d(win))
        """
        GRAB SCREEN DATA WITH PREPROCESSING
        """
        for pipe in pipes:
            pipe.move()
            if pipe.collide(bird, win):
                run = False
                break
            
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                """ 
                NEURAL NETWORK SCORING
                """
                fitness_score = fitness_score * 2                                               # Every pipe passed doubles the fitness score
                """ 
                NEURAL NETWORK SCORING
                """
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            pipes.append(Pipe(WIN_WIDTH))

        for r in rem:
            pipes.remove(r)
        
        """ 
        NEURAL NETWORK INPUT/OUTPUT
        """
        q_values = model.forward(state)
        if (q_values[0][0] > q_values[0][1]):
            bird.jump()
        """ 
        NEURAL NETWORK INPUT/OUTPUT
        """
        """ 
        NEURAL NETWORK SCORING
        """
        fitness_score += 1                                                                      # Every forward movement increases the fitness score
        """ 
        NEURAL NETWORK SCORING
        """
        game.draw_window(win, bird, pipes, base, pipe_ind)

    # 
    latest_thought_process = neural_network.thought_process.format(fitness_score, model.hidden_layer.weights, model.hidden_layer.biases, model.output_layer.weights, model.output_layer.biases, user_input)
    return latest_thought_process

if __name__ == '__main__':
    user_input, user_lives = game.menu_screen()
    # The total number of attempts the current generation of birds have
    for x in range(user_lives): 
        latest_thought_process = game_start(user_input, True)
        print("SCORE:",latest_thought_process[0][0], " for the ", x+1, " attempt")
        # Keeping track of the best 3 thought processes
        best_thought_processes.append(latest_thought_process)
        best_thought_processes.sort(key=lambda x: x[0][0], reverse=True)
        best_thought_processes = best_thought_processes[:8]
        
