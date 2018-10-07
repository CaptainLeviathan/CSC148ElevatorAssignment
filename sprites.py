"""CSC148 Assignment 1 - Sprites

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module Description ===

This file contains the different Sprite classes, used for the visualization
with Pygame, the graphics library we're using for this assignment.
There's quite a bit in this file, but you aren't responsible for most of it.

DO NOT CHANGE ANY CODE IN THIS FILE. You don't need to for this assignment,
and in fact you aren't even submitting this file!

The two classes whose documentation you are required to read are ElevatorSprite
and PersonSprite, as you'll be implementing their subclasses.
You can completely ignore the other Sprite classes in this file.
"""
import random
from typing import Any
import pygame


# Images for people
FIGURES = [f'people/person{i}.png' for i in range(1, 6)]


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)


# Dimensions for various objects
WIDTH = 900               # Screen width
STAT_WINDOW_HEIGHT = 100  # Space at the top for stats and messages
FLOOR_HEIGHT = 100        # The height of each floor (including the border)
FLOOR_BORDER_HEIGHT = 10  # The height of the border

ELEVATOR_HEIGHT = 66      # Elevator height
ELEVATOR_WIDTH = 44       # Elevator width

PERSON_HEIGHT = 50        # Person height
PERSON_WIDTH = 32         # Person width

# Fonts
FONT_HEIGHT = 30
pygame.init()
COMIC_SANS = pygame.font.SysFont('Comic Sans MS', FONT_HEIGHT)


###############################################################################
# Sprites
###############################################################################
class ElevatorSprite(pygame.sprite.Sprite):
    """Sprite representing an elevator.

    === Attributes ===
    image: the Pygame surface on which to draw this sprite
    rect: the rectangle representing the dimensions of this sprite
    """
    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self) -> None:
        """Initialize a new ElevatorSprite."""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([ELEVATOR_WIDTH, ELEVATOR_HEIGHT])
        self.image.fill(GREEN)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

    def update(self) -> None:
        """Update this elevator's image based on its fullness."""
        pygame.draw.rect(self.image, GREEN,
                         [0, 0, ELEVATOR_WIDTH, ELEVATOR_HEIGHT])
        pygame.draw.rect(self.image, DARK_GREEN,
                         [0, ELEVATOR_HEIGHT * (1 - self.fullness()),
                          ELEVATOR_WIDTH, ELEVATOR_HEIGHT])

    def fullness(self) -> float:
        """Return the fraction that this elevator is filled.

        The value returned should be a float between 0.0 (completely empty) and
        1.0 (completely full).
        """
        raise NotImplementedError


class PersonSprite(pygame.sprite.Sprite):
    """Sprite representing a person.

    === Attributes ===
    height: the height of the person sprite
    width: the width of the person sprite
    image: the Pygame surface on which to draw this sprite
    rect: the rectangle representing the dimensions of this sprite

    === Representation Invariants ===
    height >= 0
    width >= 0
    """
    height: int
    width: int
    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self) -> None:
        """Initialize a new person sprite."""
        super().__init__()
        self.width, self.height = PERSON_WIDTH, PERSON_HEIGHT
        self.image = self.load_image()
        self.rect = self.image.get_rect()
        self.rect.bottom = 0
        self.rect.centerx = random.randint(-2, 2)

    def load_image(self) -> Any:
        """Load the image for this sprite and redraws it
        Lower indices are happier :)
        """
        image = pygame.image.load(FIGURES[self.get_anger_level()])
        return pygame.transform.scale(image, (self.width, self.height))

    def get_anger_level(self) -> int:
        """Return the anger level of this sprite.

        This determines the image used to render this sprite.

        Anger level must be an integer between 0 and 4, inclusive.
        (0 means not at all angry, 4 is very angry)
        """
        raise NotImplementedError


class FloorSprite(pygame.sprite.Sprite):
    """Sprite that draws a floor of the building.
    """
    def __init__(self, width: int, height: int, y: int) -> None:
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        pygame.draw.rect(self.image, BLUE, [0, 0, width, FLOOR_BORDER_HEIGHT])
        self.rect = self.image.get_rect()
        self.rect.top = y


class FloorNum(pygame.sprite.Sprite):
    """Text Sprite to Label the floor number.
    """
    def __init__(self, floor_y: int, text: str) -> None:
        super().__init__()
        self.floor_font = COMIC_SANS
        self.image = self.floor_font.render(text, True, BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = floor_y
        self.rect.right = WIDTH - 20


class StatLine(pygame.sprite.Sprite):
    """Text Sprite for displaying some text.
    """
    def __init__(self, y: int, text: str):
        super().__init__()
        self.floor_font = COMIC_SANS
        self.image = self.floor_font.render(text, True, BLACK)
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = 5
