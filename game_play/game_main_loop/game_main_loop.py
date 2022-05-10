from data.shared import SP_hero, SP_ghost, f_fix_image, screen_size, walk, I_exit_button, I_play_button_blue, I_pause_button_blue, I_pause_button_green, I_play_button_green, f_draw_all_path, f_draw_wall, p, screen, P_base
from game_play.game_main_loop.ghost_bot import C_ghost_bot
from game_play.game_main_loop.hero_class import C_hero
from ast import literal_eval
from os import listdir
from time import sleep
from random import choice


def f_game_main_loop(map_file_name):

    # preparation ________________________________________________

    l_ghosts_sprites = []
    coin_sprite = 0

    P_map = P_base + '\\maps'
    P_map_file = P_map + '\\' + map_file_name + '\\' + map_file_name

    l_map_data = []
    with open(P_map_file, 'r') as map_file:
        for i in map_file:
            l_map_data.append(literal_eval(i))
    l_open_path = l_map_data[0]
    l_ghost_location = l_map_data[1]
    l_gates_location = l_map_data[2]
    hero_location = l_map_data[3]
    grid_color = l_map_data[4][1]
    wall_color = l_map_data[4][0]
    del l_map_data

    l_coin_images = []
    coin_frame = 0
    coin_count = 0
    for i in listdir(P_base + '\\maps\\' + map_file_name):
        if i != map_file_name:
            image = p.image.load(P_base + '\\maps\\' + map_file_name + '\\' + i)
            image = f_fix_image(image, image.get_size(), (0, 0))
            l_coin_images.append(image.convert())
    pause_button_blue = f_fix_image(I_pause_button_blue, (walk, walk), False)
    pause_button_green = f_fix_image(I_pause_button_green, (walk, walk), False)
    play_button_green = f_fix_image(I_play_button_green, (walk, walk), False)
    play_button_blue = f_fix_image(I_play_button_blue, (walk, walk), False)

    l_menu = [
        (I_exit_button, (screen_size[0] - I_exit_button.get_width() - 4, screen_size[1] - I_exit_button.get_height() - 4 - 0 * (walk + 16)), I_exit_button.get_size()),
        (f_fix_image(play_button_green, (40, 40), (1, 1)), (screen_size[0] - play_button_green.get_width() - 4, screen_size[1] - play_button_green.get_height() - 4 - 1 * (walk + 16)), play_button_green.get_size()),
        (pause_button_blue, (screen_size[0] - pause_button_blue.get_width() - 4, screen_size[1] - pause_button_blue.get_height() - 4 - 2 * (walk + 16)), pause_button_blue.get_size())
    ]

    l_ghosts = []
    for i in l_ghost_location:
        l_ghosts.append(C_ghost_bot(i, l_open_path))
    hero = C_hero(hero_location, l_open_path, l_coin_images)
    inp = {'up': False, 'down': False, 'left': False, 'right': False}
    pause_game = False

    screen.fill((0, 0, 0))
    f_draw_wall(screen, wall_color, grid_color)
    f_draw_all_path(screen, l_open_path)
    for ii in l_menu:
        screen.blit(ii[0], ii[1])
    p.display.flip()

    # functions __________________________________________________

    def f_you_win():
        fonts = p.font.get_fonts()
        count = 1
        terminate_count = 0

        screen.fill((0, 0, 0))
        p.display.flip()

        poop = True
        while poop:

            if count == 1:
                screen.fill((0, 0, 0))
                font = p.font.SysFont(fonts[9], 72)
                text = font.render('You won !!!', True, (0, 150, 70))
                text_size = text.get_size()
                screen.blit(text, (screen_size[0] / 2 - text_size[0] / 2, screen_size[1] / 2 - text_size[1] / 2))
                p.display.flip()
            if count == 2:
                screen.fill((0, 0, 0))
                font = p.font.SysFont(fonts[9], 150)
                text = font.render('You won !!!', True, (0, 150, 70))
                text_size = text.get_size()
                screen.blit(text, (screen_size[0] / 2 - text_size[0] / 2, screen_size[1] / 2 - text_size[1] / 2))
                p.display.flip()
                count = 0

            if terminate_count == 10:
                poop = False

            terminate_count += 1
            count += 1

            sleep(.25)

    def f_you_loose():
        for i in range(3):
            p.draw.polygon(screen, (0, 0, 0), (
                (hero.smooth_location[0], hero.smooth_location[1]),
                (hero.smooth_location[0] + walk, hero.smooth_location[1]),
                (hero.smooth_location[0] + walk, hero.smooth_location[1] + walk),
                (hero.smooth_location[0], hero.smooth_location[1] + walk),
            ))
            p.display.flip()
            sleep(.3)
            screen.blit(hero.current_sprite, hero.smooth_location)
            p.display.flip()
            sleep(.3)

    def f_hero():
        for ii in inp:
            if inp[ii]:
                hero.f_pick_direction(ii)
        hero.f_move()

    def f_ghost():
        nonlocal l_ghosts_sprites
        nonlocal running
        for e, ii in enumerate(l_ghosts):
            if ii.smooth_location[0] < hero.smooth_location[0] + 7:
                if ii.smooth_location[0] > hero.smooth_location[0] - 7:
                    if ii.smooth_location[1] < hero.smooth_location[1] + 7:
                        if ii.smooth_location[1] > hero.smooth_location[1] - 7:
                            f_you_loose()
                            running = False
                            f_game_main_loop(map_file_name)
            if ii.fin == walk:
                ii.fin = 0
                ii.location = ii.f_pick_direction()
                ii.target_location = ii.location.copy()
            ii.fin += 2

            if ii.target_location != 0:
                l_ghost_location[e] = ii.move(ii.target_location, ii.smooth_location)
            l_ghosts_sprites = l_ghost_location

    def f_coin():
        nonlocal coin_count, coin_frame, coin_sprite
        if coin_count == 15:
            coin_frame += 1
            coin_count = 0
            f_draw_all_path(screen, l_open_path)
        if coin_frame > len(l_coin_images) - 1:
            coin_frame = 0
        if coin_sprite != 0:
            screen.blit(coin_sprite[0], coin_sprite[1])
        coin_sprite = l_coin_images[coin_frame], (0, 0)

    def f_input():
        nonlocal running, inp, pause_game

        for event in p.event.get():
            if p.mouse.get_pos()[0] > screen_size[0] - 120:
                if p.mouse.get_pressed() == (1, 0, 0):
                    for i in l_menu:
                        if p.mouse.get_pos()[0] > i[1][0]:
                            if p.mouse.get_pos()[0] < i[1][0] + i[2][0]:
                                if p.mouse.get_pos()[1] > i[1][1]:
                                    if p.mouse.get_pos()[1] < i[1][1] + i[2][1]:

                                        if i[0] == l_menu[0][0]:
                                            running = False
                                        if i[0] == l_menu[1][0]:
                                            if pause_game:
                                                pause_game = False
                                                screen.blit(pause_button_blue, l_menu[2][1])
                                                screen.blit(play_button_green, i[1])

                                        if i[0] == l_menu[2][0]:
                                            if not pause_game:
                                                pause_game = True
                                                screen.blit(pause_button_green, l_menu[2][1])
                                                screen.blit(play_button_blue, l_menu[1][1])
                                                p.display.flip()

            if event.type == p.KEYDOWN:

                if event.key == p.K_UP:
                    for ii in inp:
                        if ii == 'up':
                            inp[ii] = True
                        if ii != 'up':
                            inp[ii] = False
                if event.key == p.K_DOWN:
                    for ii in inp:
                        if ii == 'down':
                            inp[ii] = True
                        if ii != 'down':
                            inp[ii] = False
                if event.key == p.K_LEFT:
                    for ii in inp:
                        if ii == 'left':
                            inp[ii] = True
                        if ii != 'left':
                            inp[ii] = False
                if event.key == p.K_RIGHT:
                    for ii in inp:
                        if ii == 'right':
                            inp[ii] = True
                        if ii != 'right':
                            inp[ii] = False

            if event.type == p.KEYUP:
                if event.key == p.K_UP:
                    inp['up'] = False
                if event.key == p.K_DOWN:
                    inp['down'] = False
                if event.key == p.K_LEFT:
                    inp['left'] = False
                if event.key == p.K_RIGHT:
                    inp['right'] = False

                if event.key == p.K_ESCAPE:
                    running = False
            if event.type == p.QUIT:
                running = False

    # game_mail_loop ________________________________________________

    running = True
    while running:
        f_input()
        if not pause_game:
            f_ghost()
            f_coin()
            coin_count += 1
            f_hero()

            if type(l_ghost_location[0][0]) != int:
                for i in l_ghosts_sprites:
                    screen.blit(i[0], i[1])

            p.draw.polygon(screen, (0, 0, 0), (
                (hero.old_location[0], hero.old_location[1]),
                (hero.old_location[0] + walk, hero.old_location[1]),
                (hero.old_location[0] + walk, hero.old_location[1] + walk),
                (hero.old_location[0], hero.old_location[1] + walk),
            ))

            screen.blit(hero.current_sprite, hero.smooth_location)

            if hero.coin_count == len(l_open_path):
                f_you_win()
                running = False
                f_game_main_loop(choice(listdir(P_base + '\\maps')))

            p.display.flip()
            sleep(.00101)

    screen.fill((0, 0, 0,))
    p.display.flip()
