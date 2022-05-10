from data.shared import getcwd, p


def hero():

    hero_sheet_image = p.image.load(getcwd() + '\\sprites\\hero\\hero_sprite_sheet.png').convert()
    hero_sheet_image.set_colorkey(hero_sheet_image.get_at((0, 0)))
    hero_sheet_size = (hero_sheet_image.get_size())
    hero_size = (int(hero_sheet_size[0] / 4), int(hero_sheet_size[1] / 4))

    hero_by = []

    for i in range(0, hero_sheet_size[1], hero_size[1]):
        hero_by.append(i)

        class Hero:
            def __init__(self):
                self.hero_size = hero_size

            def draw_hero_animation(self, option, location, surface):
                for ii in range(0, hero_sheet_size[0], hero_size[0]):
                    rect = p.Rect(ii, hero_size[1] * option, hero_size[0], hero_size[1])
                    image_1 = p.Surface(rect.size)
                    image_1.blit(hero_sheet_image,  (0, 0), rect)

                    surface.blit(image_1, location)
                    p.display.flip()

            def draw_single_sprite(self, option, location, surface):
                rect = p.Rect(option[0] * hero_size[0], option[1] * hero_size[1], hero_size[0], hero_size[1])
                image_1 = p.Surface(rect.size)
                image_1.blit(hero_sheet_image,  (0, 0), rect)

                surface.blit(image_1, location)
                p.display.flip()

    hero_sprite = Hero()
    return hero_sprite

