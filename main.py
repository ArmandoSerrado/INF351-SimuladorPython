import pygame, sys
from pygame.locals import *
import numpy as np
from dataclasses import dataclass
import copy

@dataclass
class COLOR:
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    RED = (255,0,0)
    YELLOW = (255,255,0)
    BLUE = (0,0,255)
    DARKBLUE = (0,0,50)
    PINK = (255,100,200)
    BROWN = (102,57,49)
    GREEN = (0,255,0)
    DARKGREEN = (0,50,0)
# COLOR = Color

TILECOLOR = {
    '.' : COLOR.BLACK, # GROUND
    'W' : COLOR.WHITE, # WALL
    'D' : COLOR.BROWN, # DOOR
    'K' : COLOR.YELLOW, # KEY
    'P' : COLOR.BLUE, # PLAYER
    'E' : COLOR.RED, # Enemy
    'B' : COLOR.PINK # Bullet
}

pygame.init()
clock = pygame.time.Clock()

TILEGRID = np.matrix(
    [['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'D', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', '.', '.', '.', '.', '.','.', '.', '.', '.', '.', 'W', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', '.', '.', '.', '.', '.','.', '.', '.', '.', '.', 'D', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', '.', '.', '.', '.', '.','.', '.', '.', '.', '.', 'W', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', 'W', 'W', 'W', 'W', 'W','W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', 'W', '.', 'W', '.', 'W','.', 'W', '.', 'W', '.', 'W', '.', 'W', '.', 'W', '.', 'W', '.', 'W', '.', 'W', '.', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', 'W', '.', '.', '.', '.','.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', '.', '.', 'W', 'W', 'W', 'W', '.', '.', '.', '.', '.', '.', 'W', '.', '.', '.', '.','.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W'],
       ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', '.', '.', '.', 'W', '.', '.', '.', '.','.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', '.', 'W', 'W', 'W', 'W', '.', '.', 'W', 'W', 'W', 'W', '.', '.', '.', 'W', '.', '.', '.', '.','.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
       ['W', 'W', '.', '.', 'W', '.', '.', 'W', 'W', 'W', 'W', '.', '.', 'W', '.', '.', '.', 'W', '.', '.', '.', '.','.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
       ['W', 'W', '.', '.', 'W', 'W', '.', '.', '.', '.', '.', '.', '.', 'W', '.', '.', '.', 'W', '.', '.', '.', '.','.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
       ['W', 'W', 'W', '.', '.', 'W', '.', '.', '.', '.', '.', '.', '.', 'W', '.', '.', '.', 'W', '.', '.', '.', '.','.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', '.', '.', 'D', '.', '.', '.', '.', '.', '.', '.', 'D', '.', '.', '.', 'D', '.', '.', '.', '.','.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', '.', '.', 'W', '.', '.', '.', '.', '.', '.', '.', 'W', '.', '.', '.', 'W', '.', '.', '.', '.','.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W'],
       ['W', 'W', '.', '.', 'W', 'W', '.', '.', '.', '.', '.', '.', '.', 'W', '.', 'W', '.', 'W', 'W', 'W', 'W', 'W','W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', '.', '.', 'W', '.', '.', 'W', 'W', 'W', 'W', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W','W', 'W', 'W', 'W', 'W', 'W', 'W', 'D', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W','W', 'W', 'W', 'W', 'W', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W','W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W','W', 'W', 'W', 'W', 'W', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W','W', 'W', 'W', 'W', 'W', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W','W', 'W', 'W', 'W', 'W', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W','W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W','W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']])
TILEGRID = np.rot90(np.fliplr(TILEGRID))

TILEGRID_copy = copy.deepcopy(TILEGRID)

# Grid Cells
CELL_SIZE = 54
CELL_OFFSET = 2

# Collision Layers
ENEMIES = []
ENVIROMENT = [] # KEYS

class Entity:
    def __init__(self) -> None:
        self._position = np.array((0,0))
        self._type = "ENTITY"
        self._color = COLOR.WHITE
        self.is_alive = True

    # Process Functions
    def process(self) -> None:
        pass
    def process_input(self, event) -> None:
        pass

    def _is_colliding(self, entity):
        if (self._position[0] == entity.get_position()[0] and 
            self._position[1] == entity.get_position()[1]):
            return True
        return False

    # Getters and Setters
    def get_position(self):
        return self._position
    def set_position(self, position):
        self._position = np.array(position)

    def get_type(self):
        return self._type
    def set_type(self, type):
        self._type = type

    def get_color(self):
        return self._color
    def set_clor(self, color):
        self._color = color

class Mobile(Entity):
    def __init__(self) -> None:
        super().__init__()
        self._direction = np.array((0,0))

    # Process Functions
    def process(self) -> None:
        super().process()
        self.process_physics()
        
    def process_input(self, event) -> None:
        super().process_input(event)

    def process_physics(self) -> None:
        self._move_and_collide()

    
    # Physics Functions
    def _move_and_collide(self) -> None:
        if not self._will_collide():
            self._position += self._direction 

    def _will_collide(self):
        if self.front_tile() != '.':
            return True
        return False
    
    def front_tile(self):
        front_tile_position = self._position + self._direction
        return TILEGRID[front_tile_position[0], front_tile_position[1]]
    
    def self_tile(self):
        return TILEGRID[self._position[0], self._position[1]]

    # Getters and Setters
    def get_direction(self):
        return self._direction
    def set_direction(self, direction):
        self._direction = np.array(direction)

class Enemy(Mobile):
    def __init__(self, position) -> None:
        super().__init__()
        self._type = "ENEMY"
        self._color = COLOR.RED
        self.set_position(position)
        self._cooldown = 0

        self._last_tick = 0
        self._current_tick = 0

    # Process is dependent on tickrate
    def process(self) -> None:
        self._current_tick = pygame.time.get_ticks()
        if self._current_tick - self._last_tick > self._cooldown:
            self._last_tick = pygame.time.get_ticks()
            super().process()

class Enemy_SidetoSide(Enemy):
    def __init__(self, position, direction) -> None:
        super().__init__(position)
        self.set_direction(direction)
        self._cooldown = 300

    def process_physics(self) -> None:
        super().process_physics()
        if self._will_collide():
            self._direction = self._direction * (-1)

class Bullet(Enemy):
    def __init__(self, position, direction, speed, color = COLOR.PINK) -> None:
        super().__init__(position)
        self.set_direction(direction)
        self._color = color

        self._cooldown = speed

    def _move_and_collide(self) -> None:
        if not self._will_collide():
            self._position += self._direction
        else: # Projectile hit wall
            self.is_alive = False

class Cannon(Enemy):
    def __init__(self, position, direction, cooldown = 1000) -> None:
        super().__init__(position)
        self.set_direction(direction)

        self._cooldown = cooldown

    def process(self) -> None:
        self._current_tick = pygame.time.get_ticks()
        if self._current_tick - self._last_tick > self._cooldown:
            self._last_tick = pygame.time.get_ticks()
            super().process()

            ENEMIES.append(Bullet(self._position, self._direction, 200))

    def process_physics(self) -> None:
        return

class Player(Mobile):
    def __init__(self) -> None:
        super().__init__()
        self.collected_keys = 0
        self._color = COLOR.BLUE
        self.died = False

    def process(self) -> None:
        super().process()

        if not self.is_alive and not self.died:
            self.died = True
            self._color = COLOR.DARKBLUE
            ENEMIES.append(Bullet(self._position, (1,0), 200, COLOR.BLUE))
            ENEMIES.append(Bullet(self._position, (1,1), 200, COLOR.BLUE))
            ENEMIES.append(Bullet(self._position, (1,-1), 200, COLOR.BLUE))
            ENEMIES.append(Bullet(self._position, (0,1), 200, COLOR.BLUE))
            ENEMIES.append(Bullet(self._position, (0,-1), 200, COLOR.BLUE))
            ENEMIES.append(Bullet(self._position, (-1,0), 200, COLOR.BLUE))
            ENEMIES.append(Bullet(self._position, (-1,1), 200, COLOR.BLUE))
            ENEMIES.append(Bullet(self._position, (-1,-1), 200, COLOR.BLUE))

    def process_input(self, event) -> None:
        super().process_input(event)
        if self.is_alive:
            if event.key == pygame.K_LEFT:
                self.set_direction((-1,0))
            if event.key == pygame.K_RIGHT:
                self.set_direction((1,0))
            if event.key == pygame.K_UP:
                self.set_direction((0,-1))
            if event.key == pygame.K_DOWN:
                self.set_direction((0,1))

    def process_physics(self) -> None:
        super().process_physics()

        if self.front_tile() == 'D' and self.collected_keys > 0:
            pos = self._position + self._direction 
            TILEGRID[pos[0], pos[1]] = '.'
            self.collected_keys -= 1

        self.set_direction((0,0)) # Stop player after moving

        # Collide with Item
        for item in ENVIROMENT:
            if item.get_type() == "KEY" and self._is_colliding(item):
                ENVIROMENT.remove(item)
                self.collected_keys += 1
            elif item.get_type() == "GOAL" and self._is_colliding(item):
                item.is_alive = False

        # Collide with Enemy
        for enemy in ENEMIES:
            if self._is_colliding(enemy):
                self.is_alive = False

class Key(Entity):
    def __init__(self, position) -> None:
        super().__init__()
        self.set_position(position)
        self._type = "KEY"
        self._color = COLOR.YELLOW

class Goal(Entity):
    def __init__(self, position) -> None:
        super().__init__()
        self._type = "GOAL"
        self.set_position(position)
        self._color = COLOR.GREEN

class Camera(Entity):
    def __init__(self) -> None:
        super().__init__()
        self._projection = np.array((0,0))
        self._view_position = np.array((0,0)) # start drawing from this point

    def process(self) -> None:
        super().process()
        self._view_position = np.array(
            (int(self._position[0] - self._projection[0]/2),
             int(self._position[1] - self._projection[1]/2)))
        self._constrain() # Constrain camera in grid

    def _constrain(self) -> None:
        # shape = TILEGRID.shape
        for i,k in enumerate(self._view_position):
            if k < 0: # if x or y position < 0, set it to 0
                self._view_position[i] = 0
            if k + self._projection[i] > TILEGRID.shape[i]:
                self._view_position[i] = TILEGRID.shape[i] - self._projection[i]


    # Getters and Setters
    def get_projection(self):
        return self._projection
    def set_projection(self, projection):
        self._projection = np.array(projection)

    def get_view_position(self):
        return self._view_position

class Game:
    def __init__(self) -> None:
        # Define Camera with (8,8) projection
        self._camera = Camera()
        self._camera.set_projection((8,8))

        # Fill buffer with black pixels
        self._display_buffer = np.full(
            (self._camera.get_projection()[0], 
            self._camera.get_projection()[1], 
            3),
            COLOR.BLACK)
        
        # Define pygame display
        self._display = pygame.display.set_mode(
            ((CELL_SIZE + CELL_OFFSET) * self._camera.get_projection()[0] + CELL_OFFSET,
             (CELL_SIZE + CELL_OFFSET) * self._camera.get_projection()[1] + CELL_OFFSET),
            0, 32)
        
        self._background_color = (10,75,100)

        self.start()


    def start(self):

        TILEGRID = np.matrix(
    [['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'D', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', '.', '.', '.', '.', '.','.', '.', '.', '.', '.', 'W', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', '.', '.', '.', '.', '.','.', '.', '.', '.', '.', 'D', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', '.', '.', '.', '.', '.','.', '.', '.', '.', '.', 'W', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', 'W', 'W', 'W', 'W', 'W','W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', 'W', '.', 'W', '.', 'W','.', 'W', '.', 'W', '.', 'W', '.', 'W', '.', 'W', '.', 'W', '.', 'W', '.', 'W', '.', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', 'W', '.', '.', '.', '.','.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', '.', '.', 'W', 'W', 'W', 'W', '.', '.', '.', '.', '.', '.', 'W', '.', '.', '.', '.','.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W'],
       ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', '.', '.', '.', 'W', '.', '.', '.', '.','.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', '.', 'W', 'W', 'W', 'W', '.', '.', 'W', 'W', 'W', 'W', '.', '.', '.', 'W', '.', '.', '.', '.','.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
       ['W', 'W', '.', '.', 'W', '.', '.', 'W', 'W', 'W', 'W', '.', '.', 'W', '.', '.', '.', 'W', '.', '.', '.', '.','.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
       ['W', 'W', '.', '.', 'W', 'W', '.', '.', '.', '.', '.', '.', '.', 'W', '.', '.', '.', 'W', '.', '.', '.', '.','.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
       ['W', 'W', 'W', '.', '.', 'W', '.', '.', '.', '.', '.', '.', '.', 'W', '.', '.', '.', 'W', '.', '.', '.', '.','.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', '.', '.', 'D', '.', '.', '.', '.', '.', '.', '.', 'D', '.', '.', '.', 'D', '.', '.', '.', '.','.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', '.', '.', 'W', '.', '.', '.', '.', '.', '.', '.', 'W', '.', '.', '.', 'W', '.', '.', '.', '.','.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W'],
       ['W', 'W', '.', '.', 'W', 'W', '.', '.', '.', '.', '.', '.', '.', 'W', '.', 'W', '.', 'W', 'W', 'W', 'W', 'W','W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', '.', '.', 'W', '.', '.', 'W', 'W', 'W', 'W', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W','W', 'W', 'W', 'W', 'W', 'W', 'W', 'D', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W','W', 'W', 'W', 'W', 'W', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W','W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W','W', 'W', 'W', 'W', 'W', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W','W', 'W', 'W', 'W', 'W', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W','W', 'W', 'W', 'W', 'W', '.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W','W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
       ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W','W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']])
        TILEGRID = np.rot90(np.fliplr(TILEGRID))

        # Initizalize Player
        self._player = Player()
        self._player.set_position((29,2))

        ENVIROMENT.clear()
        ENEMIES.clear()

        # Add Keys
        ENVIROMENT.append(Key((25,10)))
        ENVIROMENT.append(Key((33,9)))
        ENVIROMENT.append(Key((2,27)))
        ENVIROMENT.append(Key((2,28)))
        ENVIROMENT.append(Key((9,25)))
        ENVIROMENT.append(Key((40,22)))

        # Add Enemies
            # First Room
        ENEMIES.append(Enemy_SidetoSide((23,7),(1,0)))
        ENEMIES.append(Enemy_SidetoSide((23,9),(1,0)))
        ENEMIES.append(Enemy_SidetoSide((23,11),(1,0)))
        ENEMIES.append(Enemy_SidetoSide((35,8),(-1,0)))
        ENEMIES.append(Enemy_SidetoSide((35,10),(-1,0)))
            # Second Room
        ENEMIES.append(Enemy_SidetoSide((20,14),(0,-1)))
        ENEMIES.append(Enemy_SidetoSide((21,14),(0,1)))
        ENEMIES.append(Enemy_SidetoSide((22,14),(0,-1)))
        ENEMIES.append(Cannon((14,12),(0,1),1200))
        ENEMIES.append(Cannon((16,12),(0,1),1200))
        ENEMIES.append(Cannon((15,27),(0,-1),1200))
            # Third Room
        ENEMIES.append(Cannon((1,20),(1,0),2000))
        ENEMIES.append(Cannon((3,31),(0,-1),2000))
            # Fourth Room
        ENEMIES.append(Enemy_SidetoSide((7,24),(0,-1)))
        ENEMIES.append(Enemy_SidetoSide((11,24),(0,1)))
            # Fifth Room
        ENEMIES.append(Cannon((18,17),(0,1),1000))
        ENEMIES.append(Cannon((20,17),(0,1),1000))
        ENEMIES.append(Cannon((22,17),(0,1),1000))
        ENEMIES.append(Cannon((24,17),(0,1),1000))
        ENEMIES.append(Cannon((26,17),(0,1),1000))
        ENEMIES.append(Cannon((28,17),(0,1),1000))
        ENEMIES.append(Cannon((30,17),(0,1),1000))
        ENEMIES.append(Cannon((32,17),(0,1),1000))
        ENEMIES.append(Cannon((34,17),(0,1),1000))
        ENEMIES.append(Cannon((36,17),(0,1),1000))
        ENEMIES.append(Cannon((38,17),(0,1),1000))

        self._goal = Goal((29, 33))
        ENVIROMENT.append(self._goal)

        TILEGRID =  copy.deepcopy(TILEGRID_copy)

    def loop(self):
        while True:
            self.event_handler()
            self.process()
            self.draw()
            pygame.display.update()
            clock.tick(20)

    def process(self):
        self._player.process()
        for enemy in ENEMIES:
            enemy.process()
        
        self._camera.set_position(self._player.get_position()) # Set camera on player
        self._camera.process()

        for enemy in ENEMIES:
            if not enemy.is_alive:
                ENEMIES.remove(enemy)
        
        # Restart game if achieved goal
        if not self._goal.is_alive:
            self.start()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: # Restart game
                    self.start()
                self._player.process_input(event)

    def draw(self):
        self._display.fill(self._background_color) # Clear Display

        self._write_buffer()

        view_position = self._camera.get_view_position()
        projection = self._camera.get_projection()
        for i in range(projection[0]):
            for j in range(projection[1]):
                pygame.draw.rect(
                    self._display, 
                    self._display_buffer[i,j], 
                    pygame.Rect(
                        CELL_OFFSET + i * (CELL_SIZE + CELL_OFFSET),
                        CELL_OFFSET + j * (CELL_SIZE + CELL_OFFSET),
                        CELL_SIZE,
                        CELL_SIZE))

    def _write_buffer(self):
        view_position = self._camera.get_view_position()
        projection = self._camera.get_projection()

        # Tiles
        for i,x in enumerate(range(view_position[0], view_position[0] + projection[0])):
            for j,y in enumerate(range(view_position[1], view_position[1] + projection[1])):
                self._display_buffer[i,j] = TILECOLOR[TILEGRID[x, y]] 

        # Enviroment
        for item in ENVIROMENT:
            if self._in_view(item):
                item_position = item.get_position()
                self._display_buffer[item_position[0] - view_position[0], 
                    item_position[1] - view_position[1]] = item.get_color()
                    
        # Player
        if self._in_view(self._player):
            player_pos = self._player.get_position()
            self._display_buffer[player_pos[0] - view_position[0], 
                player_pos[1] - view_position[1]] = self._player.get_color()
                
        # Enemy
        for enemy in ENEMIES:
            if self._in_view(enemy):
                enemy_position = enemy.get_position()
                self._display_buffer[enemy_position[0] - view_position[0], 
                    enemy_position[1] - view_position[1]] = enemy.get_color()
    
    # Checks if entity is inside viewport
    def _in_view(self, entity):
        view_position = self._camera.get_view_position()
        projection = self._camera.get_projection()
        if (entity.get_position()[0] >= view_position[0] and 
            entity.get_position()[0] < view_position[0] + projection[0] and
            entity.get_position()[1] >= view_position[1] and 
            entity.get_position()[1] < view_position[1] + projection[1]):
                return True
        
        return False

game = Game()
game.loop()
