from data.shared import getcwd, p
from time import sleep


def coin(scale_size):

    hero_sheet_image = p.image.load(getcwd() + '\\sprites\\coin\\coin_sprite_sheet.png').convert()
    hero_sheet_image.set_colorkey(hero_sheet_image.get_at((0, 0)))
    hero_sheet_image = p.transform.scale(hero_sheet_image, scale_size)
    hero_sheet_size = (hero_sheet_image.get_size())
    hero_size = (int(hero_sheet_size[0] / 10), hero_sheet_size[1])

    class Gate:
        def __init__(self):
                self.hero_size = hero_size

        def draw_coin_animation(self, option, location, surface):
                for ii in range(0, hero_sheet_size[0], hero_size[0]):
                    rect = p.Rect(ii, hero_size[1] * option, hero_size[0], hero_size[1])
                    image_1 = p.Surface(rect.size)
                    image_1.blit(hero_sheet_image,  (0, 0), rect)
                    sleep(.1)

                    surface.blit(image_1, location)
                    p.display.flip()

        def draw_single_sprite(self, option, location, surface):
                rect = p.Rect(option * hero_size[0], 0, hero_size[0], hero_size[1])
                image_1 = p.Surface(rect.size)
                image_1.blit(hero_sheet_image,  (0, 0), rect)

                surface.blit(image_1, location)
                p.display.flip()

    hero_sprite = Gate()
    return hero_sprite


