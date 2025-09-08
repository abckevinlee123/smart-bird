import pygame
import random
import os
import time
import sys

# game_refactored.py
import pygame
import random
import os
import sys

pygame.font.init()

# --- Constants ---
WIN_WIDTH = 600
WIN_HEIGHT = 800
FLOOR_Y = 730
FPS = 30

STAT_FONT = pygame.font.Font("./font/flappy-bird-font.ttf", 25)
END_FONT = pygame.font.SysFont("comicsans", 50)

DRAW_LINES = False

# --- Window setup ---
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Smart Bird")

# --- Image assets ---
pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")).convert_alpha())
bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "bg.png")).convert_alpha(), (WIN_WIDTH, 900))
bird_images = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", f"bird{x}.png")))
    for x in range(1, 4)
]
base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")).convert_alpha())

lives_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "lives.png")).convert_alpha(), (160, 56))
neuron_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "neuron.png")).convert_alpha(), (160, 56))
epoch_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "epoch.png")).convert_alpha(), (160, 56))
blank_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "blank.png")).convert_alpha(), (160, 56))


# --- Classes ---
class Bird:
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = y
        self.img_count = 0
        self.img = bird_images[0]

    def jump(self):
        self.velocity = 7.7
        self.tick_count = 0
        self.height = self.y

    def update_position(self):
        direction = 1 if self.velocity >= 0 else -1
        displacement = (self.velocity ** 2) * 0.6 * direction if self.velocity > -7 else 20 * 1.25
        self.y -= displacement
        self.velocity -= 1.1

        if self.y < self.height and self.tilt < self.MAX_ROTATION:
            self.tilt = self.MAX_ROTATION
        elif self.y >= self.height and self.tilt > -90:
            self.tilt -= self.ROT_VEL

    def draw(self, window):
        self.img_count += 1
        if self.img_count <= self.ANIMATION_TIME:
            self.img = bird_images[0]
        elif self.img_count <= self.ANIMATION_TIME * 2:
            self.img = bird_images[1]
        elif self.img_count <= self.ANIMATION_TIME * 3:
            self.img = bird_images[2]
        elif self.img_count <= self.ANIMATION_TIME * 4:
            self.img = bird_images[1]
        else:
            self.img = bird_images[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = bird_images[1]
            self.img_count = self.ANIMATION_TIME * 2

        blit_rotate_center(window, self.img, (self.x, self.y), self.tilt)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200
    VELOCITY = 8

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

    def update_position(self):
        self.x -= self.VELOCITY

    def draw(self, window):
        window.blit(self.PIPE_TOP, (self.x, self.top))
        window.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide_with_bird(self, bird, window):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        return bird_mask.overlap(top_mask, top_offset) or bird_mask.overlap(bottom_mask, bottom_offset)


class Base:
    VELOCITY = 8
    WIDTH = base_img.get_width()
    IMG = base_img

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def update_position(self):
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, window):
        window.blit(self.IMG, (self.x1, self.y))
        window.blit(self.IMG, (self.x2, self.y))


# --- Utility functions ---
def blit_rotate_center(surface, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)
    surface.blit(rotated_image, new_rect.topleft)


def draw_window(window, bird, pipes, base, active_pipe_index):
    window.blit(bg_img, (0, 0))
    for pipe in pipes:
        pipe.draw(window)
    base.draw(window)
    bird.draw(window)
    pygame.display.update()


def show_menu():
    clock = pygame.time.Clock()
    inputs = ["", "", ""]
    active_field = 0

    bird = Bird(210, 350)
    base = Base(FLOOR_Y)
    menu_active = True

    while menu_active:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        if active_field < 2:
                            active_field += 1
                        else:
                            num_neurons, num_attempts, num_epochs = map(int, inputs)
                            menu_active = False
                    except ValueError:
                        inputs = ["", "", ""]
                elif event.key == pygame.K_BACKSPACE:
                    inputs[active_field] = inputs[active_field][:-1]
                elif event.unicode.isdigit():
                    inputs[active_field] += event.unicode

        base.update_position()
        draw_menu_screen(bird, base, inputs)

    return num_neurons, num_attempts, num_epochs


def draw_menu_screen(bird, base, inputs):
    window = win
    window.blit(bg_img, (0, 0))
    base.draw(window)
    bird.draw(window)

    img_positions = [(neuron_img, inputs[0], 50), (lives_img, inputs[1], 125), (epoch_img, inputs[2], 200)]

    for img, text_input, y_pos in img_positions:
        window.blit(img, ((WIN_WIDTH / 2) - img.get_width() - 20, y_pos))
        window.blit(blank_img, ((WIN_WIDTH / 2) + 20, y_pos))
        rendered_text = STAT_FONT.render(text_input, 1, (255, 255, 255))
        txt_x = ((WIN_WIDTH / 2) + img.get_width() / 2 + 22 - rendered_text.get_width() / 2)
        txt_y = (y_pos + img.get_height() / 2 - rendered_text.get_height() / 2)
        window.blit(rendered_text, (txt_x, txt_y))

    pygame.display.update()