from data.shared import P_base, p, f_draw_brick, f_draw_all_path, f_draw_wall, f_draw_path, f_fix_image, SP_hero, SP_ghost, I_quit, I_reset, I_save, I_color_palate, walk, screen_size, screen
from game_play.menus.draw_map_menu import draw_map_menu_loop
from sprites.general import SpriteSheet
from ast import literal_eval

# f_ stands for shared functions
# lf_ stands for left click function
# rf_ stands for right click function


def f_draw_map_loop(map_file_name):

    SP_gate = SpriteSheet(p.image.load(P_base + '\\sprites\\sprite_sheets\\gate_sprite_sheet.png'), (7, 2))

    l_menu = [
        (I_quit, (screen_size[0] - I_quit.get_width() - 4, screen_size[1] - I_quit.get_height() - 4 - 0 * (walk + 16)), I_quit.get_size()),
        (I_save, (screen_size[0] - I_save.get_width() - 4, screen_size[1] - I_save.get_height() - 4 - 1 * (walk + 16)), I_save.get_size()),
        (I_reset, (screen_size[0] - I_reset.get_width() - 4, screen_size[1] - I_reset.get_height() - 4 - 2 * (walk + 16)), I_reset.get_size()),
        (I_color_palate, (screen_size[0] - I_color_palate.get_width(), 0), I_color_palate.get_size()),
        (f_fix_image(SP_ghost.image_grid[0][0], (70, 70), (1, 1)), (screen_size[0] - 90, 280), f_fix_image(SP_ghost.image_grid[0][0], (70, 70), (1, 1)).get_size()),
        (f_fix_image(SP_hero.image_grid[0][0], (100, 100), (1, 1)), (screen_size[0] - 105, 380), f_fix_image(SP_hero.image_grid[0][0], (100, 100), (1, 1)). get_size()),
        (f_fix_image(SP_gate.image_grid[0][0], (40, 40), False), (screen_size[0] - 110, 500), (100, 100))
    ]

    x_grid = [i for i in range(0, screen_size[0] - 120, walk)]
    y_grid = [i for i in range(0, screen_size[1], walk)]
    current_function = 'draw_path'

    l_open_path = []
    l_ghost_location = []
    l_gates_location = []
    hero_location = []
    m_pos = [0, 0]

    wall_color = (170, 150, 0)
    grid_color = (200, 200, 0)

    if map_file_name:
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

    def f_draw_characters(surface):
        if hero_location:
            surface.blit(SP_hero.image_grid[0][0], hero_location)
        if l_ghost_location:
            for i in l_ghost_location:
                surface.blit(SP_ghost.image_grid[0][0], (i[0], i[1]))

    def f_draw_menu(surface):
        p.draw.polygon(screen, (0, 0, 0), (
            (screen_size[0] - 116, 0),
            (screen_size[0], 0),
            (screen_size[0], screen_size[1]),
            (screen_size[0] - 116, screen_size[1])
        ))
        for ii in l_menu:
            if ii != l_menu[-1]:
                surface.blit(ii[0], (ii[1][0], ii[1][1]))
            if ii == l_menu[-1]:
                surface.blit(ii[0], (ii[1][0] + 30, ii[1][1] + 30))

    def lf_save():
        nonlocal running
        if l_open_path:
            running = draw_map_menu_loop(l_open_path, [], l_ghost_location, hero_location, grid_color, wall_color, map_file_name)[1]
            f_draw_wall(screen, wall_color, grid_color)
            f_draw_all_path(screen, l_open_path)
            f_draw_menu(screen)
            f_draw_characters(screen)
            p.display.flip()
            return running
        if not l_open_path:
            return True

    def lf_reset():
        nonlocal l_open_path
        nonlocal hero_location
        nonlocal l_ghost_location
        nonlocal wall_color
        nonlocal grid_color
        l_open_path = []
        l_ghost_location = []
        hero_location = []
        wall_color = (170, 150, 0)
        grid_color = (200, 200, 0)
        f_draw_wall(screen, wall_color, grid_color)
        p.display.flip()

    def lf_color_palate_wall():
        nonlocal wall_color
        nonlocal grid_color
        wall_color = screen.get_at((p.mouse.get_pos()))
        f_draw_wall(screen, wall_color, grid_color)
        f_draw_all_path(screen, l_open_path)
        if hero_location:
            screen.blit(SP_hero.image_grid[0][0], (hero_location[0], hero_location[1]))
        if l_ghost_location:
            for i in l_ghost_location:
                screen.blit(SP_ghost.image_grid[0][0], (i[0], i[1]))
        p.display.flip()

    def lf_hero():
        nonlocal current_function
        if current_function != 'draw_hero':
            f_draw_menu(screen)
            p.draw.circle(screen, (150, 150, 0), (int(l_menu[-2][1][0] + l_menu[-2][2][0] / 2), int(l_menu[-2][1][1] + l_menu[-2][2][1] / 2)), int(l_menu[-2][2][0] / 2 + 4), 4)
            current_function = 'draw_hero'
            p.display.flip()

    def lf_ghost():
        nonlocal current_function
        if current_function != 'draw_ghost':
            f_draw_menu(screen)
            p.draw.circle(screen, (150, 150, 0), (int(l_menu[-3][1][0] + l_menu[-3][2][0] / 2), int(l_menu[-3][1][1] + l_menu[-3][2][1] / 2)), int(l_menu[-2][2][0] / 2 + 4), 4)
            current_function = 'draw_ghost'
            p.display.flip()

    def lf_gate():
        nonlocal current_function
        if current_function != 'draw_gate':
            f_draw_menu(screen)
            p.draw.circle(screen, (150, 150, 0), (int(l_menu[-1][1][0] + l_menu[-1][2][0] / 2), int(l_menu[-1][1][1] + l_menu[-1][2][1] / 2)), int(l_menu[-1][2][0] / 2 + 4), 4)
            current_function = 'draw_gate'
            p.display.flip()

    def lf_quit():
        nonlocal running
        running = False

    #

    def rf_color_palate_wall():
        nonlocal grid_color
        nonlocal wall_color
        grid_color = screen.get_at((p.mouse.get_pos()))
        f_draw_wall(screen, wall_color, grid_color)
        f_draw_all_path(screen, l_open_path)
        if hero_location:
            screen.blit(SP_hero.image_grid[0][0], (hero_location[0], hero_location[1]))
        if l_ghost_location:
            for i in l_ghost_location:
                screen.blit(SP_ghost.image_grid[0][0], (i[0], i[1]))
        p.display.flip()

    def rf_hero():
        nonlocal current_function
        if current_function == 'draw_hero':
            p.draw.circle(screen, (0, 0, 0), (int(l_menu[-2][1][0] + l_menu[-2][2][0] / 2), int(l_menu[-2][1][1] + l_menu[-2][2][1] / 2)), int(l_menu[-2][2][0] / 2 + 4), 4)
            current_function = 'draw_path'
            p.display.flip()

    def rf_ghost():
        nonlocal current_function
        if current_function == 'draw_ghost':
            current_function = 'draw_path'
            f_draw_menu(screen)
            p.display.flip()

    def rf_gate():
        nonlocal current_function
        if current_function == 'draw_gate':
            p.draw.circle(screen, (0, 0, 0), (int(l_menu[-1][1][0] + l_menu[-1][2][0] / 2), int(l_menu[-1][1][1] + l_menu[-1][2][1] / 2)), int(l_menu[-1][2][0] / 2 + 4), 4)
            current_function = 'draw_path'
            p.display.flip()

    f_draw_wall(screen, wall_color, grid_color)
    f_draw_menu(screen)
    if map_file_name:
        f_draw_all_path(screen, l_open_path)
        f_draw_characters(screen)
    p.display.flip()

    # main_loop ________________________________________________________________________
    m_left = False
    m_right = False
    running = True

    while running:

        if m_left:
            if p.mouse.get_pos()[0] < screen_size[0] - 120:
                for x in x_grid:
                    if x < p.mouse.get_pos()[0] < x + walk:
                        m_pos[0] = x
                for y in y_grid:
                    if y < p.mouse.get_pos()[1] < y + walk:
                        m_pos[1] = y

                if current_function == 'draw_path':
                    if [m_pos[0], m_pos[1]] not in l_open_path:
                        l_open_path.append([m_pos[0], m_pos[1]])
                        f_draw_path(screen, m_pos[0], m_pos[1])
                        if hero_location:
                            screen.blit(SP_hero.image_grid[0][0], hero_location)
                        if l_ghost_location:
                            for i in l_ghost_location:
                                screen.blit(SP_ghost.image_grid[0][0], i)
                        p.display.flip()

                if current_function == 'draw_hero':
                    if [m_pos[0], m_pos[1]] in l_open_path:
                        if [m_pos[0], m_pos[1]] != hero_location:
                            if hero_location:
                                f_draw_path(screen, hero_location[0], hero_location[1])
                            if [m_pos[0], m_pos[1]] in l_ghost_location:
                                f_draw_path(screen, m_pos[0], m_pos[1])
                                l_ghost_location.remove(m_pos)
                            hero_location = [m_pos[0], m_pos[1]]
                            screen.blit(SP_hero.image_grid[0][0], m_pos)
                            p.display.flip()

                if current_function == 'draw_ghost':
                    if [m_pos[0], m_pos[1]] in l_open_path:
                        if [m_pos[0], m_pos[1]] not in l_ghost_location:
                            if [m_pos[0], m_pos[1]] == hero_location:
                                f_draw_path(screen, hero_location[0], hero_location[1])
                                hero_location = []
                            l_ghost_location.append([m_pos[0], m_pos[1]])
                            screen.blit(SP_ghost.image_grid[0][0], m_pos)
                            p.display.flip()

            # menu ___________________________________________________________________
            if p.mouse.get_pos()[0] > screen_size[0] - 120:
                for i in l_menu:
                    if p.mouse.get_pos()[0] > i[1][0]:
                        if p.mouse.get_pos()[0] < i[1][0] + i[2][0]:
                            if p.mouse.get_pos()[1] > i[1][1]:
                                if p.mouse.get_pos()[1] < i[1][1] + i[2][1]:

                                    if i[0] == I_reset:
                                        lf_reset()
                                    if i[0] == I_color_palate:
                                        lf_color_palate_wall()

                                    if i[0] == I_save:
                                        if hero_location:
                                            if l_ghost_location:
                                                running = lf_save()

                                    if i[0] == I_quit:
                                        lf_quit()
                                    if i[0] == l_menu[-2][0]:
                                        lf_hero()
                                    if i[0] == l_menu[-3][0]:
                                        lf_ghost()
                                    if i[0] == l_menu[-1][0]:
                                        lf_gate()

        if m_right:
            for x in x_grid:
                if x < p.mouse.get_pos()[0] < x + walk:
                    m_pos[0] = x
            for y in y_grid:
                if y < p.mouse.get_pos()[1] < y + walk:
                    m_pos[1] = y

            if current_function == 'draw_path':
                if p.mouse.get_pos()[0] < screen_size[0] - 120:
                    if [m_pos[0], m_pos[1]] in l_open_path:
                        if [m_pos[0], m_pos[1]] == hero_location:
                            hero_location = []
                        if [m_pos[0], m_pos[1]] in l_ghost_location:
                            l_ghost_location.remove(m_pos)
                        l_open_path.remove([m_pos[0], m_pos[1]])
                        f_draw_brick(wall_color, grid_color, screen, m_pos[0], m_pos[1])
                        f_draw_all_path(screen, l_open_path)
                        if hero_location:
                            screen.blit(SP_hero.image_grid[0][0], hero_location)
                        if l_ghost_location:
                            for i in l_ghost_location:
                                screen.blit(SP_ghost.image_grid[0][0], i)
                        p.display.flip()

            if current_function == 'draw_hero':
                if [m_pos[0], m_pos[1]] == hero_location:
                    hero_location = []
                    f_draw_path(screen, m_pos[0], m_pos[1])
                    p.display.flip()
                if [m_pos[0], m_pos[1]] in l_ghost_location:
                    l_ghost_location.remove(m_pos)
                    f_draw_path(screen, m_pos[0], m_pos[1])
                    p.display.flip()

            if current_function == 'draw_ghost':
                if [m_pos[0], m_pos[1]] in l_ghost_location:
                    l_ghost_location.remove(m_pos)
                    f_draw_path(screen, m_pos[0], m_pos[1])
                    p.display.flip()
                if [m_pos[0], m_pos[1]] == hero_location:
                    hero_location = []
                    f_draw_path(screen, m_pos[0], m_pos[1])
                    p.display.flip()

            # menus __________________________________________________________
            if p.mouse.get_pos()[0] > screen_size[0] - 120:
                for i in l_menu:
                    if p.mouse.get_pos()[0] > i[1][0]:
                        if p.mouse.get_pos()[0] < i[1][0] + i[2][0]:
                            if p.mouse.get_pos()[1] > i[1][1]:
                                if p.mouse.get_pos()[1] < i[1][1] + i[2][1]:
                                    if i[0] == I_color_palate:
                                        rf_color_palate_wall()
                                    if i[0] == l_menu[-2][0]:
                                        rf_hero()
                                    if i[0] == l_menu[-3][0]:
                                        rf_ghost()
                                    if i[0] == l_menu[-1][0]:
                                        rf_gate()

        m_left = False
        m_right = False

        for event in p.event.get():

            if p.mouse.get_pressed() == (1, 0, 0):
                m_left = True
            if p.mouse.get_pressed() == (0, 0, 1):
                m_right = True

            if event.type == p.KEYUP:
                if event.key == p.K_ESCAPE:
                    running = False
            if event.type == p.QUIT:
                running = False

    return True
