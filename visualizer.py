"""CSC148 Assignment 1 - Visualizer

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module Description ===

This file contains the Visualizer class, which is responsible for interacting
with Pygame, the graphics library we're using for this assignment.
There's quite a bit in this file, but you aren't responsible for most of it.

DO NOT CHANGE ANY CODE IN THIS FILE. You don't need to for this assignment,
and in fact you aren't even submitting this file!
"""
from __future__ import annotations
import random
import time
from typing import Dict, List

import pygame
from algorithms import Direction
import sprites


# Colour constants
WHITE = (255, 255, 255)

# Dimensions for various objects
WIDTH = 900               # Screen width
STAT_WINDOW_HEIGHT = 100  # Space at the top for stats and messages
FLOOR_HEIGHT = 100        # The height of each floor (including the border)
FLOOR_BORDER_HEIGHT = 10  # The height of the border

# FPS based on config speed
FPS = 60


class Visualizer:
    """Visualizer for the current state of a simulation.

    All attributes of this class are private; you are not responsible for
    understanding them, and they are left undocumented.
    """
    def __init__(self,
                 elevators: List[sprites.ElevatorSprite],
                 num_floors: int,
                 visualize: bool) -> None:
        """Initialize this visualization.

        If visualize is False, this instance does nothing.
        """
        self._visualize = visualize
        if not self._visualize:
            return

        self._num_elevators = len(elevators)
        self._num_floors = num_floors

        # pygame stuff
        pygame.init()
        self._clock = pygame.time.Clock()

        self._screen = pygame.display.set_mode(
            (WIDTH, self._total_height()), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._screen.fill(WHITE)

        # Contains all sprites in the simulation
        self._sprite_group = pygame.sprite.Group()
        self._stats_group = pygame.sprite.Group()

        self._setup_sprites(elevators)
        # Initial render.
        self.render()

    def render_header(self, round_num: int) -> None:
        """Render text displaying the round number for this simulation."""
        if not self._visualize:
            return
        self._stats_group.remove(list(self._stats_group))
        self._stats_group.add(sprites.StatLine(0, f'Round {round_num}'))
        for sprite in self._sprite_group:
            if isinstance(sprite, sprites.PersonSprite):
                sprite.image = sprite.load_image()
        self.render()

    def _total_height(self) -> int:
        """Return the screen height for this visualization."""
        return self._num_floors * FLOOR_HEIGHT + STAT_WINDOW_HEIGHT

    def get_y_of_floor(self, floor: int) -> int:
        """Return the y-coordinate of the given floor."""
        assert self._num_floors >= floor >= 1, f'{self._num_floors}, {floor}'
        return (
            self._total_height() -
            (floor - 1) * FLOOR_HEIGHT -
            FLOOR_BORDER_HEIGHT
        )

    def render(self) -> None:
        """Draw the current state of the simulation to the screen.
        """
        if not self._visualize:
            return

        # Need this on OSX due to pygame bug
        pygame.event.peek(0)

        self._screen.fill(WHITE)
        self._sprite_group.draw(self._screen)
        self._stats_group.draw(self._screen)
        self._clock.tick(FPS)
        pygame.display.flip()

    def show_arrivals(self,
                      arrivals: Dict[int, List[sprites.PersonSprite]]) -> None:
        """Show new arrivals."""
        if not self._visualize:
            return

        x = 10
        for floor, people in arrivals.items():
            y = self.get_y_of_floor(floor)
            for person in people:
                person.rect.bottom = y
                person.rect.centerx = x + random.randint(-3, 3)
                self._sprite_group.add(person)
        self.render()

    def show_boarding(self, person: sprites.PersonSprite,
                      elevator: sprites.ElevatorSprite) -> None:
        """Show boarding of the given person onto the given elevator.

        Precondition: the given person is on the same floor as the elevator.
        """
        if not self._visualize:
            return

        from_x = 10
        target_x = elevator.rect.centerx + random.randint(-3, 3)

        for frame in range(21):  # Move in 20 seconds
            person.rect.centerx = from_x + (target_x - from_x) * frame // 20
            self.render()

        elevator.update()
        self.render()

    def show_disembarking(self, person: sprites.PersonSprite,
                          elevator: sprites.ElevatorSprite) -> None:
        """Show disembarking of the given person from the given elevator."""
        if not self._visualize:
            return

        from_x = person.rect.centerx
        target_x = 10

        elevator.update()

        for frame in range(21):  # Move in 20 seconds
            x = from_x + (target_x - from_x) * frame // 20
            person.rect.centerx = x
            self.render()

    def show_elevator_moves(self,
                            elevators: List['Elevator'],
                            directions: List[Direction]) -> None:
        """Show elevator moves. Note that all the elevators move at once."""
        if not self._visualize:
            return

        for _ in range(20):  # Move in 20 seconds
            for elevator, direction in zip(elevators, directions):
                if direction == Direction.UP:
                    step = - FLOOR_HEIGHT / 20
                elif direction == Direction.DOWN:
                    step = FLOOR_HEIGHT / 20
                else:
                    step = 0
                elevator.rect.bottom += step
                for passenger in elevator.passengers:
                    passenger.rect.bottom += step

            self.render()

    def wait(self, wait_time: int) -> None:
        """Wait for the specified amount of time, in seconds.

        Only occurs if self.visualize is true, otherwise there's no need to
        wait.
        """
        if self._visualize:
            time.sleep(wait_time)

    def _setup_sprites(self, elevators: List[sprites.ElevatorSprite]) -> None:
        """Set up the initial sprites for this visualization.

        Position them on the screen and spaces them based on:
            Size of the screen
            Number of each item
        """
        for i in range(1, self._num_floors + 1):
            y = self.get_y_of_floor(i)
            floor = sprites.FloorSprite(WIDTH, FLOOR_HEIGHT, y)
            floor_num = sprites.FloorNum(y - 20, str(i))
            self._sprite_group.add(floor_num)
            self._sprite_group.add(floor)

        for i, elevator in enumerate(elevators):
            elevator.rect.centerx =\
                (i + 1) * WIDTH // (self._num_elevators + 1)
            elevator.rect.bottom = self._total_height() - FLOOR_BORDER_HEIGHT

            self._sprite_group.add(elevator)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['random', 'pygame', 'time', 'algorithms'],
        'generated-members': 'pygame.*'
    })
