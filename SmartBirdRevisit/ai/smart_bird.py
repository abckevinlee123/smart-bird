import pygame
import numpy as np  # For array manipulation
import matplotlib.pyplot as plt

from lib import game
from lib import utility
from lib import neural_network

FPS = 30
POPULATION_SIZE = 8

# Game logic:

class Simulation:
    def __init__(self, num_neurons):
        self.num_neurons = num_neurons
        self.best_thought_processes = [
            {'fitness_score': 0} for _ in range (POPULATION_SIZE)
        ]
        self.first_run = True
        self.window = game.win
        # --- Matplotlib Setup ---
        plt.ion() # Turn on interactive mode (VERY IMPORTANT)

        # Create the figure and two subplots side-by-side
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 5))
        self.fig.show()

    def run_epoch(self, num_attempts):
        for attempt_index in range(num_attempts):
            selected_index = attempt_index % 3  # Cycle through top 3 for evolution
            if self.first_run:
                evolved_process = None
            else:
                evolved_process = utility.evolve_thought_process(
                    self.best_thought_processes[selected_index],
                    self.num_neurons,
                    selected_index,
                    self.best_thought_processes[selected_index]['fitness_score']
                )
            latest_process = self.run_single_simulation(evolved_process)
            self.update_best_processes(latest_process)
            # --- Update the Combined Plot ---
            utility.visualize_thought_process(
                self.fig, 
                self.ax1, 
                self.ax2, 
                latest_process
            )

            print(f"Attempt {attempt_index + 1}: Score {latest_process['fitness_score']}")

    def run_single_simulation(self, thought_process):
        clock = pygame.time.Clock()
        bird = game.Bird(210, 350)
        base = game.Base(game.FLOOR_Y)
        pipes = [game.Pipe(700)]
        fitness_score = 0
        running = True

        if self.first_run:
            model = neural_network.model(True, 0, self.num_neurons)  # Start fresh random model
        else:
            model = neural_network.model(False, thought_process, self.num_neurons)

        while running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            active_pipe_index = 0
            if len(pipes) > 1 and bird.x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                active_pipe_index = 1

            if bird.y + bird.img.get_height() >= game.FLOOR_Y or bird.y < -220:
                break

            bird.update_position()
            base.update_position()

            should_add_pipe = False
            pipes_to_remove = []

            screen_state = utility.preprocess_screen(pygame.surfarray.array3d(self.window))

            for pipe in pipes:
                pipe.update_position()
                if pipe.collide_with_bird(bird, self.window):
                    running = False
                    break

                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    pipes_to_remove.append(pipe)

                if not pipe.passed and pipe.x < bird.x:
                    fitness_score += 500  # Reward for passing a pipe
                    pipe.passed = True
                    should_add_pipe = True

            if should_add_pipe:
                pipes.append(game.Pipe(game.WIN_WIDTH))

            for pipe in pipes_to_remove:
                pipes.remove(pipe)

            # Neural network decides whether to jump
            q_values = model.forward(screen_state)
            if q_values[0][0] > q_values[0][1]:
                bird.jump()

            fitness_score += 1  # Increment score for survival
            game.draw_window(self.window, bird, pipes, base, active_pipe_index)

        thought_process_record = neural_network.thought_process.format(
            fitness_score,
            model.hidden_layer.weights,
            model.hidden_layer.biases,
            model.output_layer.weights,
            model.output_layer.biases,
            self.num_neurons
        )
        return thought_process_record

    def update_best_processes(self, new_process):
        self.best_thought_processes.append(new_process)
        self.best_thought_processes.sort(key=lambda x: x['fitness_score'], reverse=True)
        self.best_thought_processes = self.best_thought_processes[:POPULATION_SIZE]
        neural_network.thought_process.save(self.best_thought_processes)


if __name__ == '__main__':
    num_neurons, num_attempts, num_epochs = game.show_menu()
    simulation = Simulation(num_neurons)
    for epoch_index in range(num_epochs):
        print(f"Epoch {epoch_index + 1}")
        simulation.run_epoch(num_attempts)
        simulation.first_run = False
