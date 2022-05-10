from data.shared import*
from time import sleep


def ghost(ghost_selection):

    ghost_sheet_image = p.image.load(getcwd() + '\\sprites\\ghost_sprite_sheet.png')
    ghost_surface_size = (ghost_sheet_image.get_width(), ghost_sheet_image.get_height())
    ghost_size = (int(ghost_surface_size[0] / 12), int(ghost_surface_size[1] / 8))

    ghost_bx = []
    ghost_by = []

    for i in range(0, ghost_surface_size[0], ghost_size[0] * 3):
        ghost_bx.append(i)
    for i in range(0, ghost_surface_size[1], ghost_size[1] * 4):
        ghost_by.append(i)

        class Ghost:
            def __init__(self, ghost_number):
                self.ghost_bey = 0
                if ghost_number > 3:
                    ghost_number -= 4
                    self.ghost_bey = ghost_size[1] * 4
                self.ghost_bex = ghost_size[0] * 3 * ghost_number
                self.surface = p.Surface((ghost_size[0], ghost_size[1]))
                self.size = ghost_size

            def draw_ghost_animation(self, option, location, surface):
                for ii in range(self.ghost_bex, self.ghost_bex + ghost_size[0] * 3, ghost_size[0]):
                    rect = p.Rect(ii, self.ghost_bey + option * ghost_size[1], ghost_size[0], ghost_size[1])
                    image_1 = p.Surface(rect.size)
                    image_1.blit(ghost_sheet_image,  (0, 0), rect)
                    sleep(.1)

                    surface.blit(image_1, location)
                    p.display.flip()

            def draw_single_sprite(self, x_option, y_option, location, surface):
                rect = p.Rect(self.ghost_bex + ghost_size[0] * x_option, self.ghost_bey + ghost_size[1] * y_option, ghost_size[0], ghost_size[1])
                image_1 = p.Surface(rect.size)
                image_1.blit(ghost_sheet_image,  (0, 0), rect)
                surface.blit(image_1, location)

    ghost_sprite = Ghost(ghost_selection)
    return ghost_sprite
