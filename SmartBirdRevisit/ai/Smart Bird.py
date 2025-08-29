import pygame
import numpy as np  # For array manipulation

from lib import game
from lib import utility
from lib import neural_network

# SIMPLY PUT: we have 4800 inputs, which is the preprocessed image of the game. It will be a black and white, lower resolution (but same aspect ratio) of the game, going into the system every frame. That is then put into the neural network with however many user_input weights there are. Initially, the weights will be randomly generated. The first epoch will do horribly, but hopefully there will be gradual improvements every epoch. We keep track of the 8 best performing "thought_processes" and then continue to "evolve" the top 3. The top 3 will evolve based on their position. The no.1 will have fewer changes, as its already succeeding, and we want to avoid changing the good things. The no.2 will have more than no.1, and no.3 more than no.2.

# Initialize:
best_thought_processes = [neural_network.thought_process.format(0, 0, 0, 0, 0, 0) for _ in range(8)]
firsttime = True

# Game logic:
def game_start(user_input, random, selected, best_score):
    # GAME VARIABLES
    clock = pygame.time.Clock()
    floor = game.FLOOR
    bird = game.Bird(210,350)
    base = game.Base(floor)
    pipes = [game.Pipe(700)]
    win = game.win

    """ CHOOSING BETWEEN A PRE-EXISTING MODEL VS. STARTING NEW """
    if not random and best_score > 25: # Keep generating random unless its above 40
        model = neural_network.model(random, evolved_thought_processes, user_input)
    else:
        model = neural_network.model(True, 0, user_input)
    """ CHOOSING BETWEEN A PRE-EXISTING MODEL VS. STARTING NEW """
    """ FITNESS SCORE, THE REWARD/PUNISHMENT METRIC FOR TRAINING """
    fitness_score = 0
    """ FITNESS SCORE, THE REWARD/PUNISHMENT METRIC FOR TRAINING """

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
        """ GRAB SCREEN DATA WITH PREPROCESSING """
        state = utility.preprocessing(pygame.surfarray.array3d(win))
        """ GRAB SCREEN DATA WITH PREPROCESSING """
        for pipe in pipes:
            pipe.move()
            if pipe.collide(bird, win):
                run = False
                break
            
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                """ NEURAL NETWORK SCORING 500 PTS FOR PASSING PIPES """
                fitness_score = fitness_score + 500
                """ NEURAL NETWORK SCORING 500 PTS FOR PASSING PIPES """
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            pipes.append(game.Pipe(WIN_WIDTH))

        for r in rem:
            pipes.remove(r)

        """ DETERMINING NEURAL NETWORK INPUT/OUTPUT """
        q_values = model.forward(state)
        if (q_values[0][0] > q_values[0][1]):
            bird.jump()
        """ DETERMINING NEURAL NETWORK INPUT/OUTPUT """
        """ INCREASE SCORING FOR EVERY SECOND THE BIRD STAYS ALIVE """
        fitness_score += 1                                                                      # Every forward movement increases the fitness score
        """ INCREASE SCORING FOR EVERY SECOND THE BIRD STAYS ALIVE """
        game.draw_window(win, bird, pipes, base, pipe_ind)

    thought_process_in_action = neural_network.thought_process.format(fitness_score, model.hidden_layer.weights, model.hidden_layer.biases, model.output_layer.weights, model.output_layer.biases, user_input)
    return thought_process_in_action

if __name__ == '__main__':
    user_input, user_lives, user_epoch = game.menu_screen()
    selected = 0;
    # The total number of attempts the current generation of birds have
    for x in range(user_epoch):
        if x >= 1:
            firsttime = False
        print("Epoch ", x+1)
        for y in range(user_lives):
            #   selected = (y % 3)  # Choose the top 3 thought_processes to undergo evolution
            evolved_thought_processes = utility.evolution(best_thought_processes[selected], user_input, selected)
            latest_thought_process = game_start(user_input, firsttime, selected, best_thought_processes[selected]['fitness_score'])
            print("SCORE:",latest_thought_process['fitness_score'], " for the ", y+1, " attempt")
            # Keeping track of the best 3 thought processes
            best_thought_processes.append(latest_thought_process)
            best_thought_processes.sort(key=lambda x: x['fitness_score'], reverse=True)
            best_thought_processes = best_thought_processes[:8]
            neural_network.thought_process.save(best_thought_processes)
