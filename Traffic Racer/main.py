import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
BG = pygame.transform.scale(pygame.image.load('images/bg.jpeg'), (WIDTH, HEIGHT)).convert()
clock = pygame.time.Clock()

icon = pygame.image.load('images\icon.ico').convert_alpha()
pygame.display.set_icon(icon)
pygame.display.set_caption('Смешарики от Кеби')

AIM = pygame.transform.scale(pygame.image.load('images/aim.png'), (75, 75)).convert_alpha()
PINKY = pygame.image.load('images/pink.png').convert_alpha()
RED = pygame.image.load('images/red.png').convert_alpha()
YELLOW = pygame.image.load('images/yellow.png').convert_alpha()
GREEN = pygame.image.load('images/green.png').convert_alpha()
BLUE = pygame.image.load('images/blue.png').convert_alpha()

class Baloons:
    Colors = {
        'pinky' : PINKY,
        'red' : RED,
        'blue' : BLUE,
        'green' : GREEN,
        'yellow' : YELLOW,
    }

    def __init__(self, x, y,color):
        self.x = x
        self.y = y
        self.img = self.Colors[color]
        self.rects = self.img.get_rect()

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, speed):
        self.y -= speed


def main():
    run = True
    FPS = 60
    speed = 2
    baloons = []
    scores = 0
    lost = 0
    wave = 5
    stroka = ' :) '

    def redraw():
        SCREEN.blit(BG, (0, 0))

        # Рендерим тут, так как scores не обновится
        scores_font = pygame.font.SysFont('Roboto Mono', 40)
        scores_render = scores_font.render(f'Scores: {scores}', True, 'black')

        lost_font = pygame.font.SysFont('Robot Mono', 40)
        losts_render = lost_font.render(f'Lost {lost}/10 baloons', True, 'black')

        SCREEN.blit(scores_render, (10, 10))
        SCREEN.blit(losts_render, (WIDTH - losts_render.get_width() - 10, 20))

        record_open = open('record.txt')
        record_show = record_open.read().strip()

        if scores > int(record_show):
            record_write = open('record.txt', 'w')
            record_write.write(str(scores))

        record_render = scores_font.render(f'Record: {record_show}', True, 'Black')
        SCREEN.blit(record_render, (10, scores_render.get_height() + 10))

        for baloon in baloons:
            baloon.draw(SCREEN)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        SCREEN.blit(AIM,(mouse_x - 37, mouse_y - 35))
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == stroka.find('XD') + 2:  # Left mouse button is 1
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for baloon in baloons:
                        if baloon.rects.collidepoint(mouse_x - baloon.x, mouse_y - baloon.y):
                            baloons.remove(baloon)
                            scores += 10

        if len(baloons) < wave:
            baloon = Baloons(random.randint(0, WIDTH - 60), HEIGHT + 100, random.choice(
                                             ['pinky', 'red', 'yellow','green','blue']))
            baloons.append(baloon)

        for baloon in baloons:
            baloon.move(speed)
            if baloon.y < -120:
                baloons.remove(baloon)
                lost += 1

        if lost >= 10:
            run = False


def main_menu():
    run = True
    while run:
        SCREEN.blit(BG,(0,0))

        start_font = pygame.font.SysFont('Raleway', 100)
        start_render = start_font.render('Играть', True, 'Yellow')
        start_rect = start_render.get_rect(topleft= (WIDTH/2 - start_render.get_width()
                                             + 100, HEIGHT/2- start_render.get_height()))

        SCREEN.blit(start_render,(start_rect))

        record_open = open('record.txt')
        record_show = record_open.read().strip()
        record_font = pygame.font.SysFont('RaleWay', 55)
        record_render = record_font.render(f'Ваш рекорд: {record_show}', True,
                                                                                 'Black')
        SCREEN.blit(record_render, ((WIDTH-record_render.get_width()) / 2, (HEIGHT-
                                           record_render.get_height() + 100) / 2))

        author_font = pygame.font.SysFont('Roboto Slab', 45)
        author_render = author_font.render('Directed by Kebi', True, 'Magenta')

        SCREEN.blit(author_render, (WIDTH-author_render.get_width() - 10, HEIGHT
                                               -author_render.get_height() - 10))

        mouse = pygame.mouse.get_pos()
        if start_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            main()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.flip()

if __name__ == '__main__':
    main_menu()
