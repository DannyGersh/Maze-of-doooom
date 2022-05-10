import pygame as p
from os import environ, getcwd, chdir
from sprites.general import SpriteSheet

# This is the data that is shared between
# all files of the game.

# l_ stands for list
# P_ stands for path
# I_ stands for image
# f_ stand for function
# SP_ stands for sprite sheet list of an image

# Every game play scenario is a function that returns
# true or false to determine if the game continues.
# they are stored in the game play folder.

p.init()
p.font.init()

# paths __________________________________________________________________________________
chdir('..')
#P_base = getcwd() + '\maze of dooomm'
P_base = __file__[0:-14]
print("\n\n" + P_base + "\n\n")

# screen __________________________________________________________________________________
environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (150, 100)
screen_size = (1400, 800)
screen = p.display.set_mode(screen_size)

# variables __________________________________________________________________________________
walk = 40
fonts = p.font.get_fonts()
wall_color = (170, 150, 0)
grid_color = (200, 200, 0)

# functions ____________________________________________________________________________________________


def f_draw_wall(surface, local_wall_color, local_grid_color):
        p.draw.polygon(surface, local_wall_color, (
            (0, 0),
            (screen_size[0] - 120, 0),
            (screen_size[0] - 120, screen_size[1]),
            (0, screen_size[1])
        ))

        for ii in range(0, screen_size[0] - 80, walk):
            p.draw.line(screen, local_grid_color, (ii, 0), (ii, screen_size[1]), 4)
        for ii in range(0, screen_size[1], walk):
            p.draw.line(screen, local_grid_color, (0, ii), (screen_size[0] - 120, ii), 4)


def f_draw_all_path(surface, l_path):
    for i in l_path:
        f_draw_path(surface, i[0], i[1])


def f_draw_brick(color_wall, color_grid, surface, x, y):
    p.draw.polygon(surface, color_wall, (
        (x, y),
        (x + walk, y),
        (x + walk, y + walk),
        (x, y + walk)))
    p.draw.polygon(surface, color_grid, (
        (x, y),
        (x + walk, y),
        (x + walk, y + walk),
        (x, y + walk)), 4)


def f_draw_path(s, x, y):
    p.draw.polygon(s, (0, 0, 0), (
        (x, y),
        (x + walk, y),
        (x + walk, y + walk),
        (x, y + walk)))


def f_load_image(name, scale, color_key):
    image = p.image.load(name).convert()
    if color_key:
        # noinspection PyArgumentList
        image.set_colorkey(p.Surface.get_at(image, (0, 0)))
    if scale:
        image = p.transform.scale(image, scale)
    return image


# main menus __________________________________________________________________________________


def f_draw_options(surface, options, chosen_option):
    for e, i in enumerate(options):
        if e == chosen_option:
            font = p.font.SysFont(fonts[9], 72)
            text = font.render('-     ' + i + '     -', True, (250, 250, 0))
            surface.blit(text, (
                screen_size[0] / 2 - text.get_width() / 2,
                screen_size[1] / 2 - (text.get_height() + 30) / 2 * e
            ))
            continue
        font = p.font.SysFont(fonts[9], 72)
        text = font.render(i, True, (0, 150, 70))
        surface.blit(text, (
            screen_size[0] / 2 - text.get_width() / 2,
            screen_size[1] / 2 - (text.get_height() + 30) / 2 * e
        ))


def f_draw_minor_text(surface):
    font = p.font.SysFont(fonts[9], 30)
    text = font.render('* Redistribution of crooked Cow Production LTD *', True, (130, 130, 130))
    surface.blit(text, (screen_size[0] / 2 - text.get_width() / 2, screen_size[1] / 1.5))


def f_draw_title(surface):
    font = p.font.SysFont(fonts[9], 120)
    text = font.render('Maze of Doooooom', True, (150, 0, 0))
    surface.blit(text, (
        screen_size[0] / 2 - text.get_width() / 2,
        screen_size[1] / 12
        )
    )


# images _________________________________________________________________________

def f_fix_image(image, size, colorkey_location):
    image = p.transform.scale(image, size)
    if colorkey_location:
        image.set_colorkey(image.get_at(colorkey_location))
    return image


#I_color_palate = p.image.load(P_base + '\\sprites\\images\\color_palate.png').convert()
I_color_palate = p.image.load(P_base + '\\\sprites\\\images\\\color_palate.png').convert()

I_exit_button = p.image.load(P_base + '\\sprites\\images\\exit_button.jpg').convert()
I_galochka = p.image.load(P_base + '\\sprites\\images\\galochka.png').convert()
I_galochka_2 = p.image.load(P_base + '\\sprites\\images\\galochka.png').convert()
I_galochka_gray = p.image.load(P_base + '\\sprites\\images\\galochka_gray.png').convert()

I_pause_button_blue = p.image.load(P_base + '\\sprites\\images\\pause_button_blue.jpg').convert()
I_pause_button_green = p.image.load(P_base + '\\sprites\\images\\pause_button_green.jpg').convert()
I_play_button_blue = p.image.load(P_base + '\\sprites\\images\\play_button_blue.jpg').convert()
I_play_button_green = p.image.load(P_base + '\\sprites\\images\\play_button_green.jpg').convert()
I_quit = p.image.load(P_base + '\\sprites\\images\\quit.png').convert()
I_reset = p.image.load(P_base + '\\sprites\\images\\reset.png').convert()
I_save = p.image.load(P_base + '\\sprites\\images\\save.png').convert()
I_X = p.image.load(P_base + '\\sprites\\images\\X.png').convert()

I_up_arrow = p.image.load(P_base + '\\sprites\\images\\up_arrow.jpg').convert()
I_lowlight_up_arrow = p.image.load(P_base + '\\sprites\\images\\lowlight_up_arrow.jpg').convert()
I_down_arrow = p.image.load(P_base + '\\sprites\\images\\down_arrow.jpg').convert()
I_lowlight_down_arrow = p.image.load(P_base + '\\sprites\\images\\lowlight_down_arrow.jpg').convert()

I_X = f_fix_image(I_X, (40, 40), (0, 0)).convert()
I_save = f_fix_image(I_save, (40, 40), (1, 1)).convert()
I_reset = f_fix_image(I_reset, (40, 40), (1, 1)).convert()
I_galochka = f_fix_image(I_galochka, (40, 40), (1, 1)).convert()
I_quit = f_fix_image(I_quit, (40, 40), (1, 1)).convert()
I_pause_button_blue = f_fix_image(I_pause_button_blue, (40, 40), (1, 1)).convert()
I_exit_button = f_fix_image(I_exit_button, (40, 40), (1, 1)).convert()
I_pause_button_green = f_fix_image(I_pause_button_green, (40, 40), (1, 1)).convert()
I_play_button_blue = f_fix_image(I_play_button_blue, (40, 40), (1, 1)).convert()
I_color_palate = f_fix_image(I_color_palate, (100, 250), (0, 0)).convert()

I_coin_sprite_sheet = p.image.load(P_base + '\\sprites\\sprite_sheets\\coin_sprite_sheet.png').convert()
I_gate_sprite_sheet = p.image.load(P_base + '\\sprites\\sprite_sheets\\gate_sprite_sheet.png').convert()
I_ghost_sprite_sheet = p.image.load(P_base + '\\sprites\\sprite_sheets\\ghost_sprite_sheet.png').convert()
I_hero_sprite_sheet = p.image.load(P_base + '\\sprites\\sprite_sheets\\hero_sprite_sheet.png').convert()

# sprites grid __________________________________________________________________________________________
SP_coin = SpriteSheet(I_coin_sprite_sheet, (10, 1))
SP_gate = SpriteSheet(I_gate_sprite_sheet, (4, 4))
SP_ghost = SpriteSheet(I_ghost_sprite_sheet, (3, 4))
SP_hero = SpriteSheet(I_hero_sprite_sheet, (4, 4))

for i in SP_hero.image_grid:
    for ii in i:
        ii.set_colorkey(ii.get_at((1, 1)))
for i in SP_ghost.image_grid:
    for ii in i:
        ii.set_colorkey(ii.get_at((1, 1)))
for i in SP_coin.image_grid:
    for e, ii in enumerate(i):
        SP_coin.image_grid[0][e] = f_fix_image(ii, (15, 15), (0, 0))
