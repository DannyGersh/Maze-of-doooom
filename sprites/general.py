from data.shared import p


class SpriteSheet:
    def __init__(self, image, grid):
        self.image = image
        self.image.set_colorkey(self.image.get_at((1, 1)))
        self.size = (self.image.get_width() / grid[0], self.image.get_height() / grid[1])

        x, y = [], []
        for i in range(grid[1]):
            for ii in range(grid[0]):
                surface = p.Surface(self.size)
                rect = p.Rect(ii * self.size[0], i * self.size[1], self.size[0], self.size[1])
                surface.blit(self.image, (0, 0), rect)
                x.append(surface.convert())
            y.append(x)
            x = []
        self.image_grid = y
        del(x, y)
