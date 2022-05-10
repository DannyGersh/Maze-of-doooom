from data.shared import*
from os import mkdir, listdir
from shutil import rmtree


def draw_map_menu_loop(l_open_path, l_gates, l_ghosts, hero_location, grid_color, wall_color, map_file_name):

    coin_size = SP_coin.image_grid[0][0].get_size()

    def draw_coins(surface, coin_frame):
        for i in l_open_path:
            if [i[0], i[1]] != hero_location:
                surface.blit(SP_coin.image_grid[0][coin_frame], (i[0] + int(walk / 2 - coin_size[0] / 2), i[1] + int(walk / 2 - coin_size[1] / 2)))

    screen.fill((0, 0, 0))

    acceptable_letters = " 1234567890-=qwertyuiop[]asdfghjkl;\zxcvbnm,./!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:|ZXCVBNM<>?"
    acceptable_letters = [iii for iii in acceptable_letters]

    def draw_text():
        font = p.font.SysFont(fonts[9], 72)
        text = font.render('Name yor map :', True, (0, 150, 70))
        title_location = (screen_size[0] / 2 - text.get_width() / 2, screen_size[1] / 2 - text.get_height() / 2 - 100)
        screen.blit(text, title_location)
        return title_location, text

    title_text_location = draw_text()[0]
    title_text_object = draw_text()[1]

    draw_text()

    copy_screen = screen.copy()
    l_map_names = listdir(P_base + '\\maps\\')
    l_map_name = []
    l_letter_dimension = []
    galochka_location = []
    ex_location = []
    yes_no = False
    overwrite_yes_no = False
    continue_draw_map = True

    if map_file_name:
        l_map_name = list(map_file_name)

    def draw_map_name():

        str_map_name = ''.join(l_map_name)

        font = p.font.SysFont(fonts[9], 72)
        text = font.render(str_map_name, True, (0, 150, 70))
        map_name_text_location = (title_text_location[0], title_text_location[1] + title_text_object.get_height())

        screen.blit(text, map_name_text_location)
        p.display.flip()
    draw_map_name()

    main_loop_running = True
    while main_loop_running:

        for event in p.event.get():

            if event.type == p.KEYUP:
                if event.key != '':

                    if chr(event.key) in acceptable_letters:
                        l_map_name.append(chr(event.key))
                        letter_font = p.font.SysFont(fonts[9], 72)
                        letter_text = letter_font.render(chr(event.key), True, (0, 150, 70))
                        l_letter_dimension.append((letter_text.get_width(), letter_text.get_height()))
                        screen.fill((0, 0, 0))
                        draw_text()
                        yes_no = False

                    if event.key == p.K_BACKSPACE and len(l_map_name) > 0:
                        del(l_map_name[-1])
                        screen.fill((0, 0, 0))
                        draw_text()
                        yes_no = False

                    if event.key == p.K_RETURN and len(l_map_name) > 0:
                        letter_font = p.font.SysFont(fonts[9], 72)
                        are_you_sure_text = letter_font.render('Are you sure ?', True, (150, 0, 70))
                        screen.blit(are_you_sure_text, (title_text_location[0], title_text_location[1] + 300))

                        galochka_location = (title_text_location[0] + are_you_sure_text.get_width() + 80, title_text_location[1] + 310)
                        ex_location = (title_text_location[0] + are_you_sure_text.get_width() + 30, title_text_location[1] + 310)

                        screen.blit(I_X, (ex_location[0], ex_location[1]))
                        screen.blit(I_galochka, (galochka_location[0], galochka_location[1]))
                        p.display.flip()

                        yes_no = True

                draw_map_name()

                if event.key == p.K_ESCAPE:
                    main_loop_running = False

            if yes_no:
                if p.mouse.get_pressed() == (1, 0, 0):
                    if p.mouse.get_pos()[0] < galochka_location[0] + 40:
                        if p.mouse.get_pos()[1] < galochka_location[1] + 40:
                            if p.mouse.get_pos()[0] > galochka_location[0]:
                                if p.mouse.get_pos()[1] > galochka_location[1]:
                                    if ''.join(l_map_name) not in l_map_names:
                                        mkdir(P_base + '\\maps\\' + ''.join(l_map_name))
                                        map_file = open(P_base + '\\maps\\' + ''.join(l_map_name) + '\\' + ''.join(l_map_name), 'w')
                                        map_file.write(str(l_open_path) + '\n' + str(l_ghosts) + '\n' + str(l_gates) + '\n' + str(hero_location) + '\n' + str((wall_color, grid_color)))
                                        for i in range(len(SP_coin.image_grid[0])):
                                            copy_screen.fill((0, 0, 0))
                                            draw_coins(copy_screen, i)
                                            p.image.save(copy_screen, P_base + '\\maps\\' + ''.join(l_map_name) + '\\' + ''.join(l_map_name) + str(i) + '.png')
                                        map_file.close()
                                    if ''.join(l_map_name) in l_map_names:
                                        overwrite_yes_no = True
                                        yes_no = False

                                        screen.fill((0, 0, 0))
                                        draw_map_name()
                                        draw_text()

                                        letter_font = p.font.SysFont(fonts[9], 72)
                                        are_you_sure_text = letter_font.render('Overwrite ?', True, (150, 0, 70))
                                        screen.blit(are_you_sure_text, (title_text_location[0], title_text_location[1] + 300))

                                        galochka_location = (title_text_location[0] + are_you_sure_text.get_width() + 80, title_text_location[1] + 310)
                                        ex_location = (title_text_location[0] + are_you_sure_text.get_width() + 30, title_text_location[1] + 310)

                                        screen.blit(I_X, (ex_location[0], ex_location[1]))
                                        screen.blit(I_galochka, (galochka_location[0], galochka_location[1]))

                                        p.display.flip()
                                        continue

                                    continue_draw_map = False
                                    main_loop_running = False

                    p.display.flip()

            if overwrite_yes_no:
                if p.mouse.get_pressed() == (1, 0, 0):
                    if p.mouse.get_pos()[0] < galochka_location[0] + 40:
                        if p.mouse.get_pos()[1] < galochka_location[1] + 40:
                            if p.mouse.get_pos()[0] > galochka_location[0]:
                                if p.mouse.get_pos()[1] > galochka_location[1]:
                                    rmtree(P_base + '\\maps\\' + ''.join(l_map_name), ignore_errors=True)
                                    mkdir(P_base + '\\maps\\' + ''.join(l_map_name))
                                    map_file = open(P_base + '\\maps\\' + ''.join(l_map_name) + '\\' + ''.join(l_map_name), 'w')
                                    map_file.write(str(l_open_path) + '\n' + str(l_ghosts) + '\n' + str(l_gates) + '\n' + str(hero_location) + '\n' + str((wall_color, grid_color)))
                                    for i in range(10):
                                        copy_screen.fill((0, 0, 0))
                                        draw_coins(copy_screen, i)
                                        p.image.save(copy_screen, P_base + '\\maps\\' + ''.join(l_map_name) + '\\' + ''.join(l_map_name) + str(i) + '.png')
                                    map_file.close()
                                    continue_draw_map = False
                                    main_loop_running = False

                    if p.mouse.get_pos()[0] < ex_location[0] + 40:
                        if p.mouse.get_pos()[1] < ex_location[1] + 40:
                            if p.mouse.get_pos()[0] > ex_location[0]:
                                if p.mouse.get_pos()[1] > ex_location[1]:
                                    yes_no = False
                                    screen.fill((0, 0, 0))
                                    draw_text()
                                    draw_map_name()
                                    p.display.flip()

            if event.type == p.QUIT:
                main_loop_running = False
            if event.type == p.QUIT:
                main_loop_running = False

    return ''.join(l_map_name), continue_draw_map
