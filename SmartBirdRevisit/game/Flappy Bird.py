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
pygame.font.init()  # init font

WIN_WIDTH = 600
WIN_HEIGHT = 800
FLOOR = 730
STAT_FONT = pygame.font.Font("./font/flappy-bird-font.ttf", 70)

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")).convert_alpha())
bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (600, 900))
bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird" + str(x) + ".png"))) for x in range(1,4)]
base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")).convert_alpha())
restart_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","restart.png")).convert_alpha(), (214, 75))

pygame.display.set_icon(bird_images[1])

class Bird:
    """
    Bird class representing the flappy bird
    """
    MAX_ROTATION = 25
    IMGS = bird_images
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
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        """
        make the bird jump
        :return: None
        """
        self.vel = 7.7
        self.tick_count = 0
        self.height = self.y

    def move(self):
        """
        make the bird move
        :return: None
        """
        direction = 1
        if self.vel < 0:
            direction = -1
        # The equation for the arc the bird makes when jumping
        if self.vel > -7:
            displacement = (self.vel ** 2) * (0.6) * direction
            self.y -= displacement
        # Terminal velocity, to not make the game impossible when falling too much
        else:
            self.y += 20 *1.25
        self.vel -= 1.1  # Counter for the arc to switch from a positive curve to a negative curve

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


class Pipe:
    """
    represents a pipe object
    """
    GAP = 200
    VEL = 8

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
    VEL = 8
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

def draw_window(win, bird, pipes, base, score, pipe_ind, run):
    """
    draws the windows for the main game loop
    :param win: pygame window surface
    :param bird: a Bird object
    :param pipes: List of pipes
    :param score: score of the game (int)
    :param pipe_ind: index of closest pipe
    :return: None
    """
    # draw background
    win.blit(bg_img, (0,0))

    # draw pipe/s
    for pipe in pipes:
        pipe.draw(win)

    # draw base
    base.draw(win)

    # draw bird
    bird.draw(win)

    # draw score
    if run:
        score_label = STAT_FONT.render(str(score),1,(0,0,0))
        temp_width = score_label.get_width()-6
        temp_height = score_label.get_height()
        temp = (temp_width, temp_height)
        temp_surface = pygame.Surface(temp)
        temp_surface.fill((255, 255, 255))
        temp_surface.blit(score_label, (0, 0))
        win.blit(temp_surface, ((WIN_WIDTH/2) - (score_label.get_width()/2), 75))
    pygame.display.update()

def restart_button(width, height):
    """
    draws the restart button to loop once more
    :return: None
    """
    win.blit(restart_img, ((WIN_WIDTH/2) - (width/2), 500))
    pygame.display.update()

def game_start():
    bird = Bird(210,350)
    base = Base(FLOOR)
    clock = pygame.time.Clock()
    pipes = [Pipe(700)]
    score = 0
    idle = True
    run = False
    dead = False
    
    while idle:
        clock.tick(30)
        # QUIT: Procedure to quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
                break
            # START: Procedure to star the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
                    idle = False
                    run = True
                    break
        base.move()
        draw_window(win, bird, pipes, base, score, 0, run)
    
    while run:
        clock.tick(30)
        # QUIT: Procedure to quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
                break
            # BIRD: Movement for the bird
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        # UNSURE
        pipe_ind = 0
        draw_window(win, bird, pipes, base, score, pipe_ind, run)
        if len(pipes) > 1 and bird.x > pipes[0].x + pipes[0].PIPE_TOP.get_width():  # determine whether to use the first or second
            pipe_ind = 1 

        # FLOOR: collision for floor
        if bird.y + bird.img.get_height() >= FLOOR or bird.y < -100:
            run = False
            dead = True
            break

        # BIRD: Moving the bird
        bird.move()

        # BASE: Moving the floor            
        base.move()

        # PIPE: Moving the pipes, checking for collision
        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            # check for collision
            if pipe.collide(bird, win):
                run = False
                dead = True
                break
            
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            pipes.append(Pipe(WIN_WIDTH))
            score += 1

        for r in rem:
            pipes.remove(r)

        # DRAW: Create the art
        # draw_window(win, bird, pipes, base, score, pipe_ind, run)
    
    while dead:
        width = restart_img.get_width()
        height = restart_img.get_height()
        clock.tick(30)
        # QUIT: Procedure to quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
                break
            # RESTART: Procedure to restart the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (WIN_WIDTH/2) - (width/2) <= mouse[0] <= (WIN_WIDTH/2) + (width/2) and 500 <= mouse[1] <= 500 + (height):
                    dead = False
                    break
        mouse = pygame.mouse.get_pos() 
        restart_button(width, height)

    return(True)


if __name__ == '__main__':
    while game_start():
        game_start()