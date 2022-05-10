from data.shared import p, P_base, fonts, screen_size, screen, f_draw_options, f_draw_title, f_draw_minor_text
from game_play.draw_map.draw_map import f_draw_map_loop
from game_play.game_main_loop.game_main_loop import f_game_main_loop
from game_play.load_map.load_map import f_load_map
from os import listdir
from random import choice

options = ['Quit', 'Load Map', 'Draw Map', 'Random Map']
chosen_option = 3

options_sizes = []

for e, i in enumerate(options):
    font = p.font.SysFont(fonts[9], 72)
    text = font.render(i, True, (0, 150, 70))

    text_x = screen_size[0] / 2 - text.get_width() / 2
    text_y = screen_size[1] / 2 - (text.get_height() + 30) / 2 * e

    options_sizes.append([i, text_x, text_y])


def draw_all_text():
    screen.fill((0, 0, 0))

    f_draw_options(screen, options, chosen_option)
    f_draw_title(screen)
    f_draw_minor_text(screen)

    screen.blit(screen, (0, 0))


main_menu_running = True

while main_menu_running:

    draw_all_text()
    p.display.flip()

    for event in p.event.get():

        if event.type == p.KEYUP:

            if event.key == p.K_UP:
                chosen_option += 1
                if chosen_option == len(options):
                    chosen_option = 0
            if event.key == p.K_DOWN:
                chosen_option -= 1
                if chosen_option == -1:
                    chosen_option = len(options) - 1

            if event.key == p.K_ESCAPE:
                main_menu_running = False

        draw_all_text()
        p.display.flip()

        if event.type == p.KEYUP:
            if event.key == p.K_RETURN:

                if chosen_option == 3:
                    l_maps = listdir(P_base + '\\maps')
                    chosen_map = choice(l_maps)
                    f_game_main_loop(chosen_map)

                if chosen_option == 2:
                    main_menu_running = f_draw_map_loop(False)

                if chosen_option == 1:
                    main_menu_running = f_load_map()

                if chosen_option == 0:
                    main_menu_running = False

        if event.type == p.QUIT:
            main_menu_running = False

p.quit()
