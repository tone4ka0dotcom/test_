import sys
from time import time
from objects import *
from db_table import *

current_player = ''
start_time = 0
total_time = 0


def show_bd():
    connection = sqlite3.connect('game_database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM players ORDER BY points DESC LIMIT 5')
    results = cursor.fetchall()
    y = 200
    title = Table(100, y, 'Имя', 'Очки')
    players_list = list()
    players_list.append(title)
    for data in results:
        y += 30
        player = Table(100, y, data[0], str(data[1]))
        players_list.append(player)
    connection.close()
    return players_list


def look_rules():
    while True:
        screen.fill(beige)
        btn_back.draw_btn()
        txt1.write()
        txt2.write()
        txt3.write()
        txt4.write()
        is_game()
        clock.tick(30)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_back.rect.collidepoint(event.pos):
                    main()


def main():
    global current_player
    is_input = False
    txt_color = grey
    name = 'Нажмите здесь'
    help_txt = Text(120, 210, 'Введите имя ниже и нажмите enter:')
    while True:
        screen.blit(background, (0, 0))
        help_area.draw()
        input_area.draw()
        help_txt.write()
        btn_start.draw_btn()
        btn_rules.draw_btn()
        txt_input = Text(210, 260, name, txt_color)
        txt_input.write()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if input_area.rect.collidepoint(event.pos):
                    if name == 'Нажмите здесь':
                        is_input = True
                        name = ''
                        txt_color = green
                elif btn_start.rect.collidepoint(event.pos) and name == 'Имя сохранено':
                    my_game()
                elif btn_rules.rect.collidepoint(event.pos):
                    look_rules()
            if is_input and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    connection = sqlite3.connect('game_database.db')
                    cursor = connection.cursor()
                    cursor.execute('SELECT username FROM players')
                    results = cursor.fetchall()
                    connection.close()
                    results = [x[0] for x in results]
                    if name not in results:
                        add_el(name, 0)
                        current_player = name
                        name = 'Имя сохранено'
                        help_txt = Text(150, 210, 'Теперь вы можете начать игру!')
                        txt_color = grey
                        is_input = False
                    else:
                        help_txt = Text(120, 210, 'Такое имя уже есть, введите новое')
                        name = ''
                        is_input = True
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 10:
                        name += event.unicode
        pygame.display.update()


def is_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def my_game():
    global total_time, start_time
    start_time = time()
    stop_game = False
    a = 0
    plate.speed = 9
    plate.points = 0
    plate.x = 250
    f_group = pygame.sprite.Group()
    for i in names_food:
        f = Food(randint(15, 585), randint(-1000, 0), 40, 40, 'FreePixelFood/' + i, randint(10, 20) * 0.2)
        f_group.add(f)
    while f_group and not stop_game:
        screen.blit(background, (0, 0))
        plate.reset()
        plate.move()
        f_group.draw(screen)
        f_group.update()
        clsn = plate.collision(f_group)
        if clsn != 'bomb' and a == 0:
            plate.points = clsn
        else:
            plate.speed = 0
            if a != len(names_bomb):
                exp_group[a].reset()
                a += 1
            if a == len(names_bomb):
                stop_game = True
                plate.points = -100
        back_rect.draw()
        points_txt = Text(50, 15, 'Очки: ' + str(plate.points))
        seconds_txt = Text(450, 15, 'Время: ' + str(20-total_time))
        seconds_txt.write()
        points_txt.write()
        is_game()
        end_time = time()
        total_time = int(end_time - start_time)
        if total_time == 20 or stop_game:
            finish()
        clock.tick(30)
        pygame.display.update()


def finish():
    update_db(current_player, plate.points)
    if total_time >= 20 and plate.points >= 30:
        finish_txt = Text(150, 50, 'Вы выиграли! Ваш счет: ' + str(plate.points))
    else:
        finish_txt = Text(150, 50, 'Вы проиграли... Ваш счет: ' + str(plate.points))
    players_list = show_bd()
    while True:
        screen.fill(beige)
        btn_back.draw_btn()
        for i in players_list:
            i.draw_line()
        finish_txt.write()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_back.rect.collidepoint(event.pos):
                    main()
        clock.tick(30)
        pygame.display.update()


main()
