"""
The classic game of flappy bird. Make with python
and pygame. Features pixel perfect collision using masks :o

Date Modified:  Jul 30, 2019
Author: Tech With Tim
Estimated Work Time: 5 hours (1 just for that damn collision)
"""
import pygame
import random
import os
import time
import neat
import pickle
import math

pygame.init()
COUNT = 0
WIN_WIDTH = 600
WIN_HEIGHT = 800
FLOOR = 700
CEILING = 0
DRAW_LINES = True
GAME_OVER = False
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

pipe_img = pygame.transform.scale2x(pygame.image.load("imgs/pipe.png").convert_alpha())
bg_img = pygame.transform.scale(pygame.image.load("imgs/bg.png").convert_alpha(), (600, 900))
bird_imgs = [pygame.transform.scale2x(pygame.image.load("imgs/bird" + str(x) + ".png")) for x in range(1,4)]
base_img = pygame.transform.scale2x(pygame.image.load("imgs/base.png").convert_alpha())

class Bird:
    """
    Bird class representing the flappy bird
    """
    MAX_ROTATION = 25
    IMGS = bird_imgs
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        """
        Initialize the object
        :param x: starting x pos (int)
        :param y: starting y pos (int)
        :return: None
        """
        self.x = x
        self.y = y
        self.tilt = 0  # degrees to tilt
        self.tick_count = 0
        self.vel = 7
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        """
        make the bird jump
        :return: None
        """
        self.vel = 7
        self.tick_count = 0
        self.height = self.y

    def move(self):
        """
        make the bird move
        :return: None
        """
        neg = 1
        if self.vel < 0:
            neg = -1
        # The equation for the arc the bird makes when jumping
        if self.vel > -7:
            displacement = (self.vel ** 2) * (0.5) * neg
            self.y -= displacement
        # Terminal velocity, to not make the game impossible when falling too much
        else:
            self.y += 35
        self.vel -= 1  # Counter for the arc to switch from a positive curve to a negative curve
        self.tick_count += 1
        if self.y < self.height:  # tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:  # tilt down
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        """
        draw the bird
        :param win: pygame window or surface
        :return: None
        """
        self.img_count += 1

        # For animation of bird, loop through three images
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

        # so when bird is nose diving it isn't flapping
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        # tilt the bird
        blitRotateCenter(win, self.img, (self.x, self.y), self.tilt)

    def get_mask(self):
        """
        gets the mask for the current image of the bird
        :return: None
        """
        return pygame.mask.from_surface(self.img)

class Pipe():
    """
    represents a pipe object
    """
    GAP = 200
    VEL = 5

    def __init__(self, x):
        """
        initialize pipe object
        :param x: int
        :param y: int
        :return" None
        """
        self.x = x 
        self.height = 0

        # where the top and bottom of the pipe is
        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(pipe_img, False, True)
        self.PIPE_BOTTOM = pipe_img

        self.passed = False

        self.set_height()

    def set_height(self):
        """
        set the height of the pipe, from the top of the screen
        :return: None
        """
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        """
        move pipe based on vel
        :return: None
        """
        self.x -= self.VEL

    def draw(self, win):
        """
        draw both the top and bottom of the pipe
        :param win: pygame window/surface
        :return: None
        """
        # draw top
        win.blit(self.PIPE_TOP, (self.x, self.top))
        # draw bottom
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird, win):
        """
        returns if a point is colliding with the pipe
        :param bird: Bird object
        :return: Bool
        """
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
    """
    Represnts the moving floor of the game
    """
    VEL = 5
    WIDTH = base_img.get_width()
    IMG = base_img

    def __init__(self, y):
        """
        Initialize the object
        :param y: int
        :return: None
        """
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        """
        move floor so it looks like its scrolling
        :return: None
        """
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        """
        Draw the floor. This is two images that move together.
        :param win: the pygame surface/window
        :return: None
        """
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

    def collide(self, bird, win):
        """
        returns if a point is colliding with the pipe
        :param bird: Bird object
        :return: Bool
        """
        bird_mask = bird.get_mask()
        floor_mask = pygame.mask.from_surface(self.IMG)
        floor_offset = (self.x1 - bird.x, self.y - round(bird.y))

        f_point = bird_mask.overlap(floor_mask, floor_offset)

        if f_point:
            return True
        return False

class Line:
    global CEILING, FLOOR

    def draw(self, bird, pipes, buffer, win):
        if DRAW_LINES:
            # 90deg line
            pygame.draw.line(win, (255, 0, 0), (bird.x + bird.img.get_width() / 2, bird.y + bird.img.get_height() / 2),
                             (pipes[buffer].x + pipes[buffer].PIPE_TOP.get_width() / 2, pipes[buffer].height), 5)
            pygame.draw.line(win, (255, 0, 0), (bird.x + bird.img.get_width() / 2, bird.y + bird.img.get_height() / 2),
                             (pipes[buffer].x + pipes[buffer].PIPE_BOTTOM.get_width() / 2, pipes[buffer].bottom), 5)

class Score:
    global EPISODE, ALGO_NUMBER

    def __init__(self):
        self.font = pygame.font.Font('freesansbold.ttf', 40)
        self.x = 10
        self.y1 = 10
        self.y2 = 60

    def update(self, tracker, score):
        self.tracker_display = self.font.render("TRACK: " + str(tracker), True, (255, 255, 255))
        self.score_display = self.font.render("SCORE: " + str(score), True, (255, 255, 255))

    def draw(self, win):
        win.blit(self.tracker_display, (self.x, self.y1))
        win.blit(self.score_display, (self.x, self.y2))

def blitRotateCenter(surf, image, topleft, angle):
    """
    Rotate a surface and blit it to the window
    :param surf: the surface to blit to
    :param image: the image surface to rotate
    :param topLeft: the top left position of the image
    :param angle: a float value for angle
    :return: None
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
    surf.blit(rotated_image, new_rect.topleft)

def draw_window(win, bird, pipes, base, line, buffer, score):
    """
    draws the windows for the main game loop
    :param win: pygame window surface
    :param bird: a Bird object
    :param pipes: List of pipes
    :param score: score of the game (int)
    :param gen: current generation
    :param pipe_ind: index of closest pipe
    :return: None
    """
    global CEILING, FLOOR

    # draw background
    win.blit(bg_img, (0,0))

    # draw lines from bird to pipe
    line.draw(bird, pipes, buffer, win)

    # draw bird
    bird.draw(win)

    # draw pipes
    for pipe in pipes:
        pipe.draw(win)

    #draw ground
    base.draw(win)

    #draw scoreboard
    score.draw(win)

    pygame.display.update()

def run():
    """
    runs the simulation of the current population of
    birds and sets their fitness based on the distance they
    reach in the game.
    """
    global WIN, COUNT, CEILING, GAME_OVER
    if not GAME_OVER:
        DOUBLE_JUMP = False
        win = WIN
        bird = Bird(230,350)
        base = Base(FLOOR)
        pipes = [Pipe(700)]
        line = Line()
        score = Score()
        buffer = len(pipes) - 1

        fitness_score = 0
        fitness_value = 0
        fitness_tracker = 0
        singleton = False
        
    clock = pygame.time.Clock()

    while not GAME_OVER:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break
            if event.type == pygame.KEYDOWN:
                DOUBLE_JUMP = True
                break

        bird.move()
        if DOUBLE_JUMP:
            bird.jump()
        DOUBLE_JUMP = False

        base.move()
        if base.collide(bird, win):
            GAME_OVER = True
        if bird.y < CEILING:
            GAME_OVER = True

        add_pipe = False
        for pipe in pipes:
            pipe.move()
            # check for collision
            if pipe.collide(bird, win):
                GAME_OVER = True
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
        if add_pipe:
            pipes.append(Pipe(WIN_WIDTH))
            buffer = len(pipes) - 2

        if bird.x > (pipes[buffer].x + pipes[buffer].PIPE_BOTTOM.get_width() - 20):
            buffer = len(pipes) - 1

        # displaying the score, the episode, and the algorithm number
        score.update(fitness_tracker, fitness_score)

        draw_window(WIN, bird, pipes, base, line, buffer, score)

######## --EVERYTHING ABOVE IS STRICTLY GAME CODE-- ########################################################################################################################

        if add_pipe:
            # passing a pipe is a bigger incentive, and will double the fitness
            fitness_score += 2 * fitness_tracker

        if GAME_OVER:
            # update the fitness score every time the game ends
            fitness_score += fitness_tracker
            # grab the weight 18 weights, put them into one list = (c)
            print(fitness_score)

        if len(pipes) > 2:
            if bird.x < (pipes[len(pipes) - 1].x) + 25:
                bird_from_top = 1
                bird_from_bot = 1

        bird_from_pipe = (pipes[len(pipes) - 1].x - (bird.x + bird.img.get_width() / 2))
        bird_from_top = (bird.y + bird.img.get_height() / 2) - (pipes[len(pipes) - 1].height)
        bird_from_bot = (pipes[len(pipes) - 1].bottom) - (bird.y + bird.img.get_height() / 2)

        distance_score = bird_from_pipe
        height_score = bird_from_top - bird_from_bot
        distance_score_calc = -((1 / 300) * (distance_score ** 2)) + 400
        height_score_calc = -((1 / 4000) * (height_score ** 2)) + 100
        if distance_score_calc < 0:
            distance_score_calc = 0
        if height_score_calc < 0:
            height_score_calc = 0
        fitness_tracker = int(distance_score_calc + height_score_calc)

"""
Passing a pipe is +1 reward, dying is -1 reward, anything else leaves the agent unaffected

"""

run()
while True:
    if GAME_OVER:
        print("restarting...")
        GAME_OVER = False
        run()

