import numpy as np
from game_play.game_main_loop.game_main_loop import *
from random import shuffle

# the map is divided to blocks,
# blocks are any squares of the map - whether wall or path.
# self.grid is a numpy grid of all the blocks in the map by representing their B-value.
# B value is a number representing the times a ghost has been to this block.
# 0 means that it is a wall
# 1 means that the ghost visited that place 0 times
# 2 means that the ghost visited that place 1 times
# 3 means that the ghost visited that place 2 times
# and so on ...
#
# it is a method of making the ghost visit the places
# less visited by the ghost.
# each turn the ghost builds a new list of the
# optional blocks it can go to (l_optional_path).
# self.grid[2][1] means x = 1 and y = 2.
# multiply by the blocks size(walk = 40)
# and you get x = 40, y = 80
# this is the exact location of the ghost on the screen
#
# this calls is the bot of the ghost.
# the f_move function calculates where the ghost will go to.


class C_ghost_bot:
    def __init__(self, location, l_open_path):

        # self.location is the start location.
        # self.target_location is the end location.
        # self.smooth_location is the motion location of the sprite(between start and end location).
        self.location = location
        self.target_location = 0
        self.x = location[0]
        self.y = location[1]
        self.smooth_location = self.location.copy()

        # numpy 2d grid of all the map B-values
        self.grid = np.tile(np.array([0]), (int(screen_size[1] / 40), int((screen_size[0] - 120) / 40)))
        # find all the open paths and set's their B value as 1
        for e, i in enumerate(l_open_path):
            self.grid[int(i[1] / 40)][int(i[0] / 40)] = 1

        # self.erase is a black surface to erase the ghost sprite.
        # self.current_ghost_sprite changes 3 times over the movement from start to end location to produce an animation.
        self.current_ghost_sprite = SP_ghost.image_grid[0][0].copy()

        # self.frames_timing decides what sprite to display each time.
        # self.fin ads 1 to itself each sickle of the loop, it starts over when it reaches walk(40).
        # self.current_frame is either 0,1 or 2, to choose the current sprite.
        # self.global_count counts when to reset the grid.
        self.frames_timing = [i for i in range(0, walk, int(walk / 4))]
        self.fin = 0
        self.current_frame = 0
        self.current_ghost_sprite = 0

        self.global_count = 0
        self.l_open_path = l_open_path

    def f_pick_direction(self):
        # define's the location of the ghost in the grid.
        y, x = int(self.location[1] / 40), int(self.location[0] / 40)
        # ads 1 to the grid location of the ghost
        self.grid[y, x] += 1

        l_search_path_4_directions = [
            [y + 1, x],
            [y - 1, x],
            [y, x + 1],
            [y, x - 1]
        ]

        shuffle(l_search_path_4_directions)

        l_optional_path = []
        for i in l_search_path_4_directions:
            if (abs(i[1] - x)) == 1:
                if self.grid[i[0], i[1]] != 0:
                    l_optional_path.append(i)
            if (abs(i[0] - y)) == 1:
                if self.grid[i[0], i[1]] != 0:
                    l_optional_path.append(i)

        # search the B values of the optional paths.
        l_B_values = []
        for i in l_optional_path:
            l_B_values.append(self.grid[i[0], i[1]])

        minimal = 100
        chosen_path = 0
        for e, i in enumerate(l_B_values):
            if i < minimal:
                minimal = i
                chosen_path = l_optional_path[e]
        target_location = [chosen_path[1] * 40, chosen_path[0] * 40]

        self.global_count += 1
        if self.global_count == 100:
            self.global_count = 0
            self.grid = np.tile(np.array([0]), (int(screen_size[1] / 40), int((screen_size[0] - 120) / 40)))
            for e, i in enumerate(self.l_open_path):
                self.grid[int(i[1] / 40)][int(i[0] / 40)] = 1

        return target_location

    def move(self, target_location, location):

        old_location = location.copy()

        for e, i in enumerate(self.frames_timing):
            if i == self.fin:
                self.current_frame = e - 1

        if target_location[0] - location[0] > 0:
            location[0] += 2
            self.current_ghost_sprite = SP_ghost.image_grid[2][self.current_frame]
        if target_location[0] - location[0] < 0:
            location[0] -= 2
            self.current_ghost_sprite = SP_ghost.image_grid[1][self.current_frame]
        if target_location[1] - location[1] > 0:
            location[1] += 2
            self.current_ghost_sprite = SP_ghost.image_grid[0][self.current_frame]
        if target_location[1] - location[1] < 0:
            location[1] -= 2
            self.current_ghost_sprite = SP_ghost.image_grid[3][self.current_frame]

        p.draw.polygon(screen, (0, 0, 0), (
            (old_location[0], old_location[1]),
            (old_location[0] + walk, old_location[1]),
            (old_location[0] + walk, old_location[1] + walk),
            (old_location[0], old_location[1] + walk),
        ))

        return self.current_ghost_sprite, self.smooth_location
