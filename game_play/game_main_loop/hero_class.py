from data.shared import p, walk, SP_hero, screen_size
from numpy import tile, array


class C_hero:
    def __init__(self, hero_location, l_open_path, l_coin_images):
        self.location = hero_location
        self.target_location = [0, 0]
        self.old_location = [0, 0]
        self.smooth_location = hero_location.copy()
        self.l_open_path = l_open_path
        self.in_motion = False
        self.xy = [0, 0]
        self.count = 0
        self.speed = 2
        self.frames = [i for i in range(0, int(walk / self.speed), int(walk / self.speed / 4))]
        self.current_frame = 0

        self.coin_count = 1
        self.grid = tile(array([0]), (int(screen_size[1] / 40), int((screen_size[0] - 120) / 40)))
        for e, i in enumerate(l_open_path):
            self.grid[int(i[1] / 40)][int(i[0] / 40)] = 1
        self.grid[int(self.location[1] / 40), int(self.location[0] / 40)] += 1

        self.l_coin_images = l_coin_images
        for i in self.l_coin_images:
            i.convert()
        self.current_sprite = SP_hero.image_grid[0][0].copy()

    def f_pick_direction(self, inp):

        if not self.in_motion:

            if inp == 'up':
                if [self.location[0], self.location[1] - walk] in self.l_open_path:
                    self.in_motion = True
                    self.target_location = [self.location[0], self.location[1] - walk]
                    self.xy[1] = -self.speed
                    self.xy[0] = 0
            if inp == 'down':
                if [self.location[0], self.location[1] + walk] in self.l_open_path:
                    self.in_motion = True
                    self.target_location = [self.location[0], self.location[1] + walk]
                    self.xy[1] = self.speed
                    self.xy[0] = 0
            if inp == 'left':
                if [self.location[0] - walk, self.location[1]] in self.l_open_path:
                    self.in_motion = True
                    self.target_location = [self.location[0] - walk, self.location[1]]
                    self.xy[0] = -self.speed
                    self.xy[1] = 0
            if inp == 'right':
                if [self.location[0] + walk, self.location[1]] in self.l_open_path:
                    self.in_motion = True
                    self.target_location = [self.location[0] + walk, self.location[1]]
                    self.xy[0] = self.speed
                    self.xy[1] = 0

    def f_move(self):

        self.old_location = self.smooth_location.copy()

        if self.in_motion:
            self.count += 1
            for e, i in enumerate(self.frames):
                if i == self.count:
                    self.current_frame = e

            self.smooth_location[0] += self.xy[0]
            self.smooth_location[1] += self.xy[1]

            if self.xy[0] < 0:
                self.current_sprite = SP_hero.image_grid[2][self.current_frame]
            if self.xy[0] > 0:
                self.current_sprite = SP_hero.image_grid[3][self.current_frame]
            if self.xy[1] < 0:
                self.current_sprite = SP_hero.image_grid[1][self.current_frame]
            if self.xy[1] > 0:
                self.current_sprite = SP_hero.image_grid[0][self.current_frame]

            if self.count == walk / self.speed:
                self.count = 0
                self.current_sprite = SP_hero.image_grid[0][0]
                self.location = self.target_location
                self.in_motion = False

                y, x = int(self.location[1] / 40), int(self.location[0] / 40)
                if self.grid[y, x] == 1:
                    self.grid[y, x] = 2
                    self.coin_count += 1
                    for i in self.l_coin_images:
                        p.draw.polygon(i, (0, 0, 0), (
                            (x * 40, y * 40),
                            (x * 40 + 40, y * 40),
                            (x * 40 + 40, y * 40 + 40),
                            (x * 40, y * 40 + 40)
                        ))

