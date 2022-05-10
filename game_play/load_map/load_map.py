from game_play.menus.main_menu import p, screen, screen_size
from game_play.draw_map.draw_map import f_draw_map_loop
from game_play.game_main_loop.game_main_loop import f_game_main_loop
from data.shared import I_galochka, P_base, I_galochka_gray, I_lowlight_down_arrow, I_lowlight_up_arrow, I_X, f_fix_image, I_up_arrow, I_down_arrow
from os import listdir


def f_load_map():

    main_menu_running = True
    l_map_names = listdir(P_base + '\\maps')
    l_map_name_locations = []
    fonts = p.font.get_fonts()
    decision = 'play'
    menu_decision = [l_map_names[0], 0]
    erase_menu_decision = -1
    scrolling = 0
    shown_menu = None

    erase_chosen_map = [p.Surface((650, 70)), [620, 45]]

    chosen_map = ''

    d_boxes = {
        'biggest': [p.Surface(screen_size), (0, 0), (50, 50, 50)],
        'main': [p.Surface((screen_size[0] - 80, screen_size[1] - 80)), (40, 40), (0, 0, 0)],
        'upper': [p.Surface((screen_size[0] - 80, screen_size[1] - 160)), (40, 120), (20, 20, 20)],
        'scroll': [p.Surface((40, screen_size[1] - 160)), (screen_size[0] - 80, 120), (50, 20, 20)],

        'play_brown': [p.Surface((240, 80)), (40, 40), (50, 20, 20)],
        'play_green': [p.Surface((240, 80)), (40, 40), (20, 100, 20)],
        'edit_green': [p.Surface((240, 80)), (280, 40), (20, 100, 20)],
        'edit_brown': [p.Surface((240, 80)), (280, 40), (50, 20, 20)],
        'exit': [p.Surface((40, 40)), (screen_size[0] - 80, 40), (50, 20, 20)],
        'up': [p.Surface((40, 40)), (screen_size[0] - 80, 120), (0, 0, 0)],
        'down': [p.Surface((40, 40)), (screen_size[0] - 80, 160), (0, 0, 0)],
        'galochka_green': [p.Surface((60, 60)), (540, 50), (20, 20, 50)],
        'galochka_grey': [p.Surface((60, 60)), (540, 50), (20, 20, 50)],

        'menu': [p.Surface((screen_size[0] - 125, 42 * len(l_map_names) + 1)), [45, 125], (0, 0, 0)]
    }
    d_lowlight = {
        'play_brown': [p.Surface((240, 80)), (40, 40), (30, 0, 0)],
        'play_green': [p.Surface((240, 80)), (40, 40), (0, 80, 0)],
        'edit_green': [p.Surface((240, 80)), (280, 40), (0, 80, 0)],
        'edit_brown': [p.Surface((240, 80)), (280, 40), (30, 0, 0)],
        'exit': [p.Surface((40, 40)), (screen_size[0] - 80, 40), (30, 0, 0)],
        'up': [p.Surface((40, 40)), (screen_size[0] - 80, 120), (0, 0, 0)],
        'down': [p.Surface((40, 40)), (screen_size[0] - 80, 160), (0, 0, 0)]
    }
    d_buttons = {}

    m_pressed = False

    # functions ________________________________________________

    def f_draw_box(surface, location, end_location, color):

        color_0 = I_down_arrow.get_at((0, 10))
        color_1 = I_down_arrow.get_at((1, 10))
        color_2 = I_down_arrow.get_at((2, 10))
        color_3 = I_down_arrow.get_at((3, 10))
        color_4 = I_down_arrow.get_at((4, 10))

        p.draw.polygon(surface, color_0, (
            (location[0], location[1]),
            (end_location[0], location[1]),
            (end_location[0], end_location[1]),
            (location[0], end_location[1])
        ), 1)

        p.draw.polygon(surface, color_1, (
            (location[0] + 1, location[1] + 1),
            (end_location[0] - 1, location[1] + 1),
            (end_location[0] - 1, end_location[1] - 1),
            (location[0] + 1, end_location[1] - 1)
        ), 1)

        p.draw.polygon(surface, color_2, (
            (location[0] + 2, location[1] + 2),
            (end_location[0] - 2, location[1] + 2),
            (end_location[0] - 2, end_location[1] - 2),
            (location[0] + 2, end_location[1] - 2)
        ), 1)

        p.draw.polygon(surface, color_3, (
            (location[0] + 3, location[1] + 3),
            (end_location[0] - 3, location[1] + 3),
            (end_location[0] - 3, end_location[1] - 3),
            (location[0] + 3, end_location[1] - 3)
        ), 1)

        p.draw.polygon(surface, color_4, (
            (location[0] + 4, location[1] + 4),
            (end_location[0] - 4, location[1] + 4),
            (end_location[0] - 4, end_location[1] - 4),
            (location[0] + 4, end_location[1] - 4)
        ), 1)

        p.draw.polygon(surface, color, (
            (location[0] + 5, location[1] + 5),
            (end_location[0] - 5, location[1] + 5),
            (end_location[0] - 5, end_location[1] - 5),
            (location[0] + 5, end_location[1] - 5)
        ))

    def f_draw_chosen_map_name():
        erase_chosen_map[0].fill((0, 0, 0))
        screen.blit(erase_chosen_map[0], erase_chosen_map[1])
        font = p.font.SysFont(fonts[48], 50)
        text = font.render(chosen_map, True, (30, 130, 50))
        erase_chosen_map[0].blit(text, (0, 0))
        screen.blit(erase_chosen_map[0], erase_chosen_map[1])

    def f_draw_chosen_map_box():
        if erase_menu_decision != -1:
            p.draw.line(d_boxes['menu'][0], (50, 50, 50), (0, erase_menu_decision), (d_boxes['menu'][0].get_width(), erase_menu_decision))
            p.draw.line(d_boxes['menu'][0], (50, 50, 50), (0, erase_menu_decision + 42), (d_boxes['menu'][0].get_width(), erase_menu_decision + 42))
        p.draw.line(d_boxes['menu'][0], (100, 0, 100), (0, menu_decision[1]), (d_boxes['menu'][0].get_width(), menu_decision[1]))
        p.draw.line(d_boxes['menu'][0], (100, 0, 100), (0, menu_decision[1] + 42), (d_boxes['menu'][0].get_width(), menu_decision[1] + 42))
        shown_menu.blit(d_boxes['menu'][0], (0, scrolling))
        screen.blit(shown_menu, d_boxes['menu'][1])

    def f_draw_show_map():
        nonlocal shown_menu
        shown_menu = p.Surface((d_boxes['menu'][0].get_width(), screen_size[1] - 180))
        shown_menu.blit(d_boxes['menu'][0], (0, scrolling))
        screen.blit(shown_menu, d_boxes['menu'][1])

    def f_start_game():

        nonlocal l_map_name_locations, shown_menu, fonts, l_map_name_locations, fonts, d_buttons

        i_x = f_fix_image(I_X, (30, 30), (0, 0))
        i_galochka_gray = f_fix_image(I_galochka_gray, (45, 45), (0, 0))
        i_galochka_green = f_fix_image(I_galochka, (45, 45), (0, 0))

        i_up_arrow = f_fix_image(I_up_arrow, (40, 40), False)
        i_down_arrow = f_fix_image(I_down_arrow, (40, 40), False)
        i_lowlight_up_arrow = f_fix_image(I_lowlight_up_arrow, (40, 40), False)
        i_lowlight_down_arrow = f_fix_image(I_lowlight_down_arrow, (40, 40), False)

        for i in d_boxes:

            if i != 'menu':
                f_draw_box(d_boxes[i][0], (0, 0), d_boxes[i][0].get_size(), d_boxes[i][2])

            if i == 'exit':
                d_boxes[i][0].blit(i_x, (5, 5))
            if i == 'up':
                d_boxes[i][0].blit(i_up_arrow, (0, 0))
            if i == 'down':
                d_boxes[i][0].blit(i_down_arrow, (0, 0))
            if i == 'galochka_green':
                d_boxes[i][0].blit(i_galochka_green, (30 - 22.5, 30 - 22.5))
            if i == 'galochka_grey':
                d_boxes[i][0].blit(i_galochka_gray, (30 - 22.5, 30 - 22.5))
            if i == 'play_brown':
                font = p.font.SysFont(fonts[48], 72)
                text = font.render('PLAY', True, (30, 130, 50))
                b_size = d_boxes[i][0].get_size()
                t_size = text.get_size()
                d_boxes[i][0].blit(text, (b_size[0] / 2 - t_size[0] / 2, b_size[1] / 2 - t_size[1] / 2))
            if i == 'play_green':
                font = p.font.SysFont(fonts[48], 72)
                text = font.render('PLAY', True, (50, 20, 20))
                b_size = d_boxes[i][0].get_size()
                t_size = text.get_size()
                d_boxes[i][0].blit(text, (b_size[0] / 2 - t_size[0] / 2, b_size[1] / 2 - t_size[1] / 2))
            if i == 'edit_green':
                font = p.font.SysFont(fonts[48], 72)
                text = font.render('EDIT', True, (50, 20, 20))
                b_size = d_boxes[i][0].get_size()
                t_size = text.get_size()
                d_boxes[i][0].blit(text, (b_size[0] / 2 - t_size[0] / 2, b_size[1] / 2 - t_size[1] / 2))
            if i == 'edit_brown':
                font = p.font.SysFont(fonts[48], 72)
                text = font.render('EDIT', True, (30, 130, 50))
                b_size = d_boxes[i][0].get_size()
                t_size = text.get_size()
                d_boxes[i][0].blit(text, (b_size[0] / 2 - t_size[0] / 2, b_size[1] / 2 - t_size[1] / 2))
            if i == 'menu':
                for name, y in zip(l_map_names, range(0, d_boxes['menu'][0].get_height(), 42)):
                    p.draw.line(d_boxes[i][0], (50, 50, 50), (0, y), (d_boxes[i][0].get_width(), y))
                    font = p.font.SysFont(fonts[48], 30)
                    text = font.render(name, True, (30, 130, 50))
                    d_boxes[i][0].blit(text, (20, y))
                    l_map_name_locations.append(y)
                f_draw_show_map()
            d_boxes[i][2] = d_boxes[i][0].get_size()

            if i != 'menu':
                screen.blit(d_boxes[i][0], d_boxes[i][1])

        for i in d_lowlight:
            f_draw_box(d_lowlight[i][0], (0, 0), d_lowlight[i][0].get_size(), d_lowlight[i][2])
            if i == 'exit':
                d_lowlight[i][0].blit(i_x, (5, 5))
            if i == 'up':
                d_lowlight[i][0].blit(i_lowlight_up_arrow, (0, 0))
            if i == 'down':
                d_lowlight[i][0].blit(i_lowlight_down_arrow, (0, 0))
            if i == 'play_brown':
                font = p.font.SysFont(fonts[48], 72)
                text = font.render('PLAY', True, (30, 130, 50))
                b_size = d_lowlight[i][0].get_size()
                t_size = text.get_size()
                d_lowlight[i][0].blit(text, (b_size[0] / 2 - t_size[0] / 2, b_size[1] / 2 - t_size[1] / 2))
            if i == 'play_green':
                font = p.font.SysFont(fonts[48], 72)
                text = font.render('PLAY', True, (50, 20, 20))
                b_size = d_lowlight[i][0].get_size()
                t_size = text.get_size()
                d_lowlight[i][0].blit(text, (b_size[0] / 2 - t_size[0] / 2, b_size[1] / 2 - t_size[1] / 2))
            if i == 'edit_green':
                font = p.font.SysFont(fonts[48], 72)
                text = font.render('EDIT', True, (50, 20, 20))
                b_size = d_lowlight[i][0].get_size()
                t_size = text.get_size()
                d_lowlight[i][0].blit(text, (b_size[0] / 2 - t_size[0] / 2, b_size[1] / 2 - t_size[1] / 2))
            if i == 'edit_brown':
                font = p.font.SysFont(fonts[48], 72)
                text = font.render('EDIT', True, (30, 130, 50))
                b_size = d_lowlight[i][0].get_size()
                t_size = text.get_size()
                d_lowlight[i][0].blit(text, (b_size[0] / 2 - t_size[0] / 2, b_size[1] / 2 - t_size[1] / 2))

            d_lowlight[i][2] = d_lowlight[i][0].get_size()

        d_buttons['play'] = d_boxes['play_green']
        d_buttons['edit'] = d_boxes['edit_brown']
        d_buttons['exit'] = d_boxes['exit']
        d_buttons['up'] = d_boxes['up']
        d_buttons['down'] = d_boxes['down']
        d_buttons['galochka'] = d_boxes['galochka_grey']

        p.display.flip()

    def f_input():
        nonlocal chosen_map, scrolling, erase_menu_decision, m_pressed, l_map_name_locations, l_map_names, fonts, running, main_menu_running, decision

        for event in p.event.get():

            m_pos = p.mouse.get_pos()
            if p.mouse.get_pressed() == (1, 0, 0):
                m_pressed = 'm_left'

            if event.type == p.MOUSEBUTTONDOWN:
                if m_pressed == 'm_left':

                    for i in l_map_name_locations:

                        if m_pos[0] > 40:
                            if m_pos[0] < screen_size[0] - 80:
                                if m_pos[1] > i + 120:
                                    if m_pos[1] < i + 42 + 120:

                                        if chosen_map == '':
                                            d_buttons['galochka'] = d_boxes['galochka_green']

                                        menu_decision[1] = i - scrolling
                                        f_draw_chosen_map_box()
                                        erase_menu_decision = i - scrolling
                                        chosen_map = (l_map_names[int(i / 42) - int(scrolling / 42)])

                for i in d_buttons:
                    if p.mouse.get_pos()[0] > d_buttons[i][1][0]:
                        if p.mouse.get_pos()[0] < d_buttons[i][1][0] + d_buttons[i][2][0]:
                            if p.mouse.get_pos()[1] > d_buttons[i][1][1]:
                                if p.mouse.get_pos()[1] < d_buttons[i][1][1] + d_buttons[i][2][1]:
                                    if i == 'play':
                                        decision = 'play'
                                        screen.blit(d_boxes['play_green'][0], d_boxes['play_green'][1])
                                        screen.blit(d_boxes['edit_brown'][0], d_boxes['edit_brown'][1])
                                        p.display.flip()
                                    if i == 'edit':
                                        decision = 'edit'
                                        screen.blit(d_boxes['play_brown'][0], d_boxes['play_brown'][1])
                                        screen.blit(d_boxes['edit_green'][0], d_boxes['edit_green'][1])
                                        p.display.flip()
                                    if i == 'up':
                                        screen.blit(d_lowlight[i][0], d_lowlight[i][1])
                                        p.display.flip()
                                    if i == 'down':
                                        screen.blit(d_lowlight[i][0], d_lowlight[i][1])
                                        p.display.flip()
                                    if i == 'galochka':
                                        screen.blit(d_boxes['galochka_grey'][0], d_boxes['galochka_grey'][1])
                                        p.display.flip()

            if event.type == p.MOUSEBUTTONUP:

                    f_draw_chosen_map_name()

                    for i in d_buttons:
                        if p.mouse.get_pos()[0] > d_buttons[i][1][0]:
                            if p.mouse.get_pos()[0] < d_buttons[i][1][0] + d_buttons[i][2][0]:
                                if p.mouse.get_pos()[1] > d_buttons[i][1][1]:
                                    if p.mouse.get_pos()[1] < d_buttons[i][1][1] + d_buttons[i][2][1]:

                                        if i == 'exit':
                                            running = False

                                        if i == 'down':
                                            if len(l_map_names) > 15:
                                                if abs(int(scrolling / 42)) != len(l_map_names) - 15:
                                                    scrolling -= 42
                                                    f_draw_show_map()
                                                    p.display.flip()

                                        if i == 'up':
                                            if len(l_map_names) > 14:
                                                if scrolling < 0:
                                                    scrolling += 42
                                                    f_draw_show_map()
                                                    p.display.flip()

                                        if i == 'galochka':
                                            if chosen_map != '':
                                                running = False
                                                if decision == 'edit':
                                                    f_draw_map_loop(chosen_map)
                                                if decision == 'play':
                                                    f_game_main_loop(chosen_map)
                        if decision == 'play':
                            screen.blit(d_boxes['play_green'][0], d_boxes['play_green'][1])
                            screen.blit(d_boxes['edit_brown'][0], d_boxes['edit_brown'][1])
                        if decision == 'edit':
                            screen.blit(d_boxes['play_brown'][0], d_boxes['play_brown'][1])
                            screen.blit(d_boxes['edit_green'][0], d_boxes['edit_green'][1])
                        if i != 'play' and i != 'edit':
                            screen.blit(d_buttons[i][0], d_buttons[i][1])

                    m_pressed = False
                    p.display.flip()

            if event.type == p.KEYUP:
                if event.key == p.K_ESCAPE:
                    running = False
                    main_menu_running = True
            if event.type == p.QUIT:
                running = False
                main_menu_running = False

    # main_loop ____________________________________________________

    f_start_game()

    running = True
    while running:
        f_input()

    return main_menu_running
