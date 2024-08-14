import pygame
import sys
from random import *
import os
import sqlite3
from time import time


class Table:
    def __init__(self, x, y, name, point, color=(74, 151, 18)):
        self.name = Text(x, y, name, color)
        self.points = Text(x+50, y, point, color)
        self.x = x
        self.y = y

    def draw_line(self):
        screen.blit(self.name.text, (self.x, self.y))
        screen.blit(self.name.text, (self.x, self.y))
        screen.blit(self.points.text, (self.x+200, self.y))


class Button:
    def __init__(self, x, y, width, height, color1, color2, text):
        self.button_txt = Text(x+20, y+10, text, color1)
        self.btn_input1 = Area(x, y, width, height, color1)
        self.btn_input2 = Area(x+5, y+5, width+-10, height-10, color2)
        self.rect = self.btn_input1.rect

    def draw_btn(self):
        self.btn_input1.draw()
        self.btn_input2.draw()
        self.button_txt.write()


class Area:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)


class Text:
    def __init__(self, x, y, txt, color=(74, 151, 18), size=30):
        self.font = pygame.font.Font(None, size)
        self.text = self.font.render(txt, True, color)
        self.x = x
        self.y = y

    def write(self):
        screen.blit(self.text, (self.x, self.y))


class Food(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, speed):
        super().__init__()
        self.name = image
        image = pygame.image.load(image)
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def move_main(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < 520:
            self.rect.x += self.speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 550:
            self.rect.y = 0
            self.rect.x = randint(15, 585)

    def collision(self, f_group):
        food = pygame.sprite.spritecollideany(self, f_group)
        if food:
            if food.name in 'FreePixelFood/bomb1.png FreePixelFood/bomb2.png FreePixelFood/bomb3.png':
                global exp_group
                exp_group = []
                names = os.listdir('Explosion')
                for i in names:
                    f = Food(150, 270, 300, 300, 'Explosion/'+i, 0)
                    exp_group.append(f)
                food.kill()
            else:
                food.kill()
                global points
                points += 1


def create_db():
    connection = sqlite3.connect('game_database.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS players (
    username TEXT,
    points INTEGER
    )
    ''')
    connection.commit()
    connection.close()


def add_el(name, point):
    connection = sqlite3.connect('game_database.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO players (username, points) VALUES (?, ?)", (name, point))
    connection.commit()
    connection.close()


def update_db(name, point):
    connection = sqlite3.connect('game_database.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE players SET points = ? WHERE username = ?', (point, name))
    connection.commit()
    connection.close()


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
    txt1 = Text(20, 200, 'В этой игре необходимо набрать больше 30 очков за 20 секунд.', size=23)
    txt2 = Text(20, 260, 'Тарелкой можно управлять клавишами "вправо"/"влево".', size=23)
    txt3 = Text(20, 230, 'Вы выиграете, если наберете 30 очков!', size=23)
    txt4 = Text(20, 290, 'Но остерегайтесь бомб! Коснувшись бомбы, вы проиграете :(', size=23)
    btn_back = Button(200, 400, 200, 40, (74, 151, 18), (238, 223, 176), 'Назад в меню')
    while True:
        screen.fill((238, 223, 176))
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
    is_input = False
    txt_color = (177, 185, 182)
    name = 'Нажмите здесь'
    help_area = Area(100, 200, 400, 40, (238, 223, 176))
    help_txt = Text(120, 210, 'Введите имя ниже и нажмите enter:')
    input_area = Area(200, 250, 200, 40, (238, 223, 176))
    btn_start = Button(200, 300, 200, 40, (74, 151, 18), (238, 223, 176), 'Начать игру')
    btn_rules = Button(200, 350, 200, 40, (74, 151, 18), (238, 223, 176), 'Правила игры')
    while True:
        screen.blit(background, (0, 0))
        help_area.draw()
        help_txt.write()
        input_area.draw()
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
                        txt_color = (74, 151, 18)
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
                        global current_player
                        current_player = name
                        name = 'Имя сохранено'
                        help_txt = Text(150, 210, 'Теперь вы можете начать игру!')
                        txt_color = (177, 185, 182)
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
    global exp_group, points, total_time, start_time
    points = 0
    exp_group = []
    start_time = time()
    stop_game = False
    plate = Food(300, 500, 80, 80, 'plate.png', 9)
    f_group = pygame.sprite.Group()
    names = os.listdir('FreePixelFood')
    a = 0
    for i in names:
        f = Food(randint(15, 585), randint(-1000, 0), 40, 40, 'FreePixelFood/' + i, randint(10, 20) * 0.2)
        f_group.add(f)
    back_rect = Area(0, 0, 600, 50, (238, 223, 176))
    while f_group and not stop_game:
        screen.blit(background, (0, 0))
        plate.reset()
        plate.move_main()
        f_group.draw(screen)
        f_group.update()
        plate.collision(f_group)
        back_rect.draw()
        points_txt = Text(50, 15, 'Очки: ' + str(points))
        seconds_txt = Text(450, 15, 'Время: ' + str(20-total_time))
        seconds_txt.write()
        points_txt.write()
        is_game()
        end_time = time()
        total_time = int(end_time - start_time)
        if exp_group:
            exp_group[int(a)].reset()
            a += 1
            if a == 16:
                stop_game = True
                points = -100
                exp_group = []
        if total_time == 20 or stop_game:
            finish()
        clock.tick(30)
        pygame.display.update()


def finish():
    update_db(current_player, points)
    if total_time >= 20 and points >= 30:
        finish_txt1 = Text(150, 50, 'Вы победили! Ваш счет: ' + str(points))
    else:
        finish_txt1 = Text(150, 50, 'Вы проиграли... Ваш счет: ' + str(points))
    players_list = show_bd()
    btn_back = Button(200, 500, 200, 40, (74, 151, 18), (238, 223, 176), 'Назад в меню')
    while True:
        screen.fill((238, 223, 176))
        btn_back.draw_btn()
        for i in players_list:
            i.draw_line()
        finish_txt1.write()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_back.rect.collidepoint(event.pos):
                    main()
        clock.tick(30)
        pygame.display.update()


pygame.init()
window_size = (600, 600)
pygame.display.set_caption("Поймай еду")
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()
points = 0
background = pygame.image.load('kitchen.jpg')
background = pygame.transform.scale(background, (600, 600))
current_player = ''
create_db()
start_time = 0
total_time = 0
exp_group = []
main()
