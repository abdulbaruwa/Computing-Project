import math
import os
from random import randint
from collections import deque

import pygame
from pygame.locals import *

FPS = 60
ANIMATION_SPEED = 0.18  # pixels per millisecond
WIN_WIDTH = 284 * 2
WIN_HEIGHT = 512

class Bird(pygame.sprite.Sprite):
    # Attributes:
    # x: The bird's X coordinate
    # y: The bird's Y coordinate
    # msec_to_climb: The number of millisecond left during a climb, where a complete climb lasts Bird.Climb_Duration

    # Constants:
    # WIDTH: The width, in pixels, of the bird's image.
    # HEIGHT: The height, in pixels, of the bird's image.
    # SINK_SPEED: the speed at which the bird descends in pixels per millisecond
    # CLIMB_SPEED: the speed at which the bird ascends in one second while climbing on average
    # CLIMB_DURATION: the number of milliseconds to execute a single climb.


    WiDTH = HEIGHT = 32
    SINK_SPEED = 0.18
    CLIMB_SPEED = 0.3
    CLIMB_DURATION = 333.3

    def __init__(self, x, y, millisecond_to_climb, images):

        super(Bird, self).__init__()
        self.x, self.y = x, y
        self.millisecond_to_climb = millisecond_to_climb
        self._img_wing_up, self._img_wing_down = images
        self._mask_wing_up = pygame.mask.from_surface(self._img_wing_up)
        self._mask_wing_down = pygame.mask.from_surface(self._img_wing_down)


    def update(self, delta_frames=1):
        # This function updates the bird's position
        # This function uses the cosine function to achieve a smooth climb:
        # Arguments: delta_frames the number of frames elasped since this method was last called.

        if self.millisecond_to_climb > 0:
            frac_climb_done = 1 - self.millisecond_to_climb/Bird.CLIMB_DURATION
            self.y -= (Bird.CLIMB_SPEED * frames_to_millisecond(delta_frames) *
                       (1 - math.cos(frac_climb_done * math.pi)))
            self.millisecond_to_climb -= frames_to_millisecond(delta_frames)
        else:
            self.y += Bird.SINK_SPEED * frames_to_millisecond(delta_frames)

    def image(self):
        if pygame.time.get_ticks() % 500 >= 250:
            return self._img_wing_up
        else:
            return self._img_wing_down

    def mask(self):
        if pygame.time.get_ticks() % 500 >= 250:
            return self._mask_wing_up
        else:
            return self._mask_wing_down

    def rect(self):
        return Rect(self.x, self.y, Bird.WiDTH, Bird.HEIGHT)


class PipePair:

    # Represents an obstacle.

    # A PipePair has a top and a bottom pipe, and only between them can the bird pass -- if it collides with either part
    # the game will end

    # Attributes
    # x = The PipePair's X position. This is a float to make movement smoother. Note that there is no y attribute,
    #  as it will only ever be 0.
    # image: A pygame.Surface which can be blitted to the main surface
    # to display the PipePair.
    # mask: A bitmask which excludes all pixels in self.image with a transparency greater than 127. helps detection
    # top_pieces : THe number of pieces, including the end piece, in top pipe.
    # bottom_pieces: The number of pieces, including the end piece, the bottom pipe.

    # Constants:
    # WIDTH: The width of the pipe in
    # PIECE_HEIGHT: The height of the pipe piece in pixels
    # ADD_INTERVAL: The interval, in milliseconds, in between adding new pipes.

    WIDTH = 80
    PIECE_HEIGHT = 32
    ADD_INTERVAL = 3000

    def __init__(self, pipe_end_img, pipe_body_img):

        # The new PipePair will automatically be assigned an x attribute of WIN_WIDTH
        # top_pieces - The number of pieces which make up the top pipe.
        # bottom_pieces - The number of pieces which make up the bottom pipe.

        self.x = WIN_WIDTH
        self.surface = surface
        self.top_pieces = top_pieces
        self.bottom_pieces = bottom_pieces
        self.score_counted = False


def top_height_px(self):
    # Returns the top pipe's height, in pixels.
    return self.top_pieces * PIPE_PIECE_HEIGHT


def bottom_height_px(self):
    # Returns the bottom pipe's height, in pixels
    return self.bottom_pieces * PIPE_PIECE_HEIGHT


def is_bird_collision(self, bird_position):
    # bird_position: The bird's position on screen, as a tuple in the form (X, Y).
    bx, by = bird_position
    in_x_range = bx + BIRD_WIDTH.self.x and bx < self.x + PIPE_WIDTH
    in_y_range = (by < self.top_height_px or
                  by + BIRD_HEIGHT > WIN_HEIGHT - self, bottom_height_px)
    return in_x_range and in_y_range


def load_images():
    # Load all images required by the game and return a dict of them.

    def load_image(img_file_name):
        file_name = os.path.join('.', 'images', img_file_name)
        img = pygame.image.load(img_file_name)
        img.convert()
        return img

    return {'background': load_image('background.png'),
            'pipe-end': load_image('pipe_end.png'),
            'pipe-body': load_image('pipe_body.png'),
            'bird_wing_up': load_image('bird_wing_up.png'),
            'bird_wing_down': load_image('bird_wing_down.png')
            }


def get_frame_jump_height(jump_step):
    fraction_jump_done = jump_step / float(BIRD_JUMP_STEPS)
    return (1 - math.cos(fraction_jump_done * math.pi)) * FRAME_BIRD_DROP_HEIGHT


def random_pipe_pair(pipe_end_img, pipe_body_img):
    # This function produces a pipe obstacle with random heights
    # The returned pipe surface will have a pipe pair with each pipe facing up and down

    # Parameters used
    # pipe_end_img - this is the image used for the pipes end piece
    # pipe_body_img - this is the image used for the pipes centre piece

    surface = pygame.Surface((PIPE_WIDTH, WIN_HEIGHT), SRCALPHA)
    surface.convert()
    surface.fill((0, 0, 0, 0))
    max_pipe_body_pieces = int(
        (WIN_HEIGHT -
         (3 * BIRD_HEIGHT) -
         (3 * PIPE_PIECE_HEIGHT) /
        PIPE_PIECE_HEIGHT
    ))
    bottom_pipe_pieces = randint(1, max_pipe_body_pieces)
    top_pipe_pieces = max_pipe_body_pieces - bottom_pipe_pieces


# Crashs when you get touch a quarter of the screen
    # bottom pipe
    for i in range(1, bottom_pipe_pieces + 1):
        print(WIN_HEIGHT - i * PIPE_PIECE_HEIGHT)
        surface.blit(pipe_body_img, (WIN_HEIGHT - i * PIPE_PIECE_HEIGHT))
    bottom_pipe_end_y = WIN_HEIGHT - bottom_pipe_pieces * PIPE_PIECE_HEIGHT
    surface.blit(pipe_end_img, (0, bottom_pipe_end_y - PIPE_PIECE_HEIGHT))
    # top pipe
    for i in range(top_pipe_pieces):
        surface.blit(pipe_body_img, (0, i * PIPE_PIECE_HEIGHT))
    top_pipe_end_y = top_pipe_pieces * PIPE_PIECE_HEIGHT
    surface.blit(pipe_end_img, (0, top_pipe_end_y))
    # compensation for the added end pieces
    top_pipe_pieces += 1
    bottom_pipe_pieces += 1
    return PipePair(surface, top_pipe_pieces, bottom_pipe_pieces)


def main():
    # The application's entry point

    pygame.init()

    display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Pygame Flappy Bird')

    clock = pygame.time.Clock()
    score_font = pygame.font.SysFont(None, 32, bold=True)
    # the bird stays in the same x position, so bird_x is a constant
    bird_x = 50
    bird_y = int(WIN_HEIGHT / 2 - BIRD_HEIGHT / 2)  # center bird on screen

    images = load_images()

    # timer for adding new pipes
    pygame.time.set_timer(EVENT_NEW_PIPE, PIPE_ADD_INTERVAL)
    pipes = []

    steps_to_jump = 2
    score = 0
    done = paused = False

    while not done:
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                done = True
                break
            elif e.type == KEYUP and e.key in (K_PAUSE, K_p):
                paused = not paused
            elif e.type == MOUSEBUTTONUP or (e.type == KEYUP and
                                             e.key in (K_UP, K_RETURN, K_SPACE)):
                steps_to_jump = BIRD_JUMP_STEPS
            elif e.type == EVENT_NEW_PIPE:
                pp = random_pipe_pair(images['pipe-end'], images['pipe-body'])
                pipes.append(pp)

        clock.tick(FPS)
        if paused:
            continue  # don't draw anything

        for x in (0, WIN_WIDTH / 2):
            display_surface.blit(images['background'], (x, 0))

        for p in pipes:
            p.x -= FRAME_ANIMATION_WIDTH
            if p.x <= -PIPE_WIDTH:  # PipePair is off screen
                pipes.remove(p)
            else:
                display_surface.blit(p.surface, (p.x, 0))

            # calculate position of jumping bird
        if steps_to_jump > 0:
            bird_y -= get_frame_jump_height(BIRD_JUMP_STEPS - steps_to_jump)
            steps_to_jump -= 1
        else:
            bird_y += FRAME_BIRD_DROP_HEIGHT

            # because pygame doesn't support animated GIFs, we have to
            # animate the flapping bird ourselves
        if pygame.time.get_ticks() % 500 >= 250:
            display_surface.blit(images['bird_wing_up'], (bird_x, bird_y))
        else:
            display_surface.blit(images['bird_wing_down'], (bird_x, bird_y))

        # update and display the score
        for p in pipes:
            if p.x + PIPE_WIDTH < bird_x and not p.score_counted:
                score += 1
                p.score_counted = True

        score_surface = score_font.render(str(score), True, (255, 255, 255))
        score_x = WIN_WIDTH / 2 - score_surface.get_width() / 2
        display_surface.blit(score_surface, (score_x, PIPE_PIECE_HEIGHT))

        pygame.display.update()

        # collision detection
        pipe_collisions = [p.is_bird_collision((bird_x, bird_y)) for p in pipes]
        if (0 >= bird_y or bird_y >= WIN_HEIGHT - BIRD_HEIGHT or
                True in pipe_collisions):
            print('You crashed')
            break
    pygame.quit()


if __name__ == '__main__':
    main()
