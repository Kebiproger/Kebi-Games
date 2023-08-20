import pygame
import random
import time

pygame.init()
pygame.display.set_caption('Пин-понг')

WIDTH, HEIGHT = 720, 480
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))

class Player():
    font = pygame.font.SysFont('MONOSPACE', 50)
    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.height = 100
        self.weight = 10
        self.show = self.font.render(f'{score}', True, 'White')

    def draw(self, window, x, y):
        self.rect = pygame.Rect(self.x, self.y, self.weight, self.height)
        pygame.draw.rect(window,'White', self.rect)
        window.blit(self.show, (x, y))

pl1_sc = 0
pl2_sc = 0

one_player = False
two_player = False
hack = False
def main():
    global pl1_sc
    global pl2_sc
    global one_player
    global two_player
    global hack

    running = True
    FPS = 60
    clock = pygame.time.Clock()
    timer = 0
    seconds_font = pygame.font.SysFont('Monospace', 70)

    rect_size = 12
    rect_x = WIDTH // 2 - 10
    rect_y = HEIGHT // 2 - rect_size // 2
    rect_speed = 7

    player1 = Player(5, HEIGHT // 2 - 50, pl1_sc)
    player2 = Player(WIDTH - 15, HEIGHT // 2 - 50, pl2_sc)
    player_speed = 3.5
    enemy_speed = 2.5

    move = random.choice(['right','left'])
    up = random.choice(['forward'])
    luck = random.choice(['lose','win'])
    def redraw():
        global ball

        SCREEN.fill((0,0,0)) # Без заливки(фона) будут глюки
        ball = pygame.Rect(rect_x, rect_y, rect_size, rect_size)
        pygame.draw.rect(SCREEN,'White', ball)

        pygame.draw.rect(SCREEN, 'white', pygame.Rect(WIDTH // 2 - 5, 0 , 2, 480))

        player1.draw(SCREEN,100, 50)
        player2.draw(SCREEN, WIDTH - 100 - player2.show.get_width(), 50)

        if timer < FPS * 4:
            SCREEN.blit(seconds_label, (WIDTH // 2 - seconds_label.get_width(), HEIGHT // 2 - \
                        seconds_label.get_height()))
        pygame.display.flip()

    while running:
        clock.tick(FPS)
        seconds_label = seconds_font.render(f'{timer // 60}', True, 'White')
        redraw()
        timer += 1

        if timer > FPS * 4:
            if move == 'left':
                rect_x -= rect_speed
            elif move == 'right':
                rect_x += rect_speed

            if ball.colliderect(player1):
                move = 'right'
                if up == 'forward':
                    up = random.choice(['up', 'down',])
            elif ball.colliderect(player2):
                move = 'left'
                if up == 'forward':
                    up = random.choice(['up', 'down'])

            if up == 'up':
                rect_y -= 2
            elif up == 'down':
                rect_y += 2

            if rect_y < 0:
                up = 'down'
            elif rect_y > HEIGHT - rect_size:
                up = 'up'

        # Моя нейронка XD
            if one_player or hack:
                if luck == 'win':
                    enemy_speed = 2
                elif luck == 'lose':
                    enemy_speed = 3.5
                    player_speed = 2.5

            if one_player or hack:
                if move == 'right' and player2.y > 0 and player2.rect.centery > ball.y:
                    player2.y -= player_speed
                elif move == 'right' and player2.y < HEIGHT - player2.height and player2.rect.centery < ball.y:
                    player2.y += player_speed

            if hack:
                if move == 'left' and  player1.y > 0 and player1.rect.centery > ball.y:
                    player1.y -= enemy_speed
                elif move == 'left' and player1.y < HEIGHT - player1.height and player1.rect.centery < ball.y:
                    player1.y += enemy_speed

            if rect_x > WIDTH:
                pl1_sc += 1
                main()
            elif rect_x < 0:
                pl2_sc += 1
                main()

            key = pygame.key.get_pressed()
            if one_player or two_player:
                if key[pygame.K_w] and player1.y > 0:
                    player1.y -= player_speed
                if key[pygame.K_s] and player1.y + 100 < HEIGHT:
                    player1.y += player_speed

            if two_player:
                if key[pygame.K_UP] and player2.y > 0:
                    player2.y -= player_speed
                if key[pygame.K_DOWN] and player2.y + 100 < HEIGHT:
                    player2.y += player_speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pl1_sc, pl2_sc = 0, 0
                one_player = two_player = hack = False
                main_menu()

def main_menu():
    global one_player
    global two_player
    global hack

    run = True
    while run:
        SCREEN.fill((0,0,0))
        mm_font = pygame.font.SysFont('Monospace', 30)

        one_p = mm_font.render('1 игрок', True, 'white')
        red = pygame.Rect(100, 300, 150, 70)
        pygame.draw.rect(SCREEN,'Red', red)
        SCREEN.blit(one_p, (red.x + 10, red.y + 20))

        two_p = mm_font.render('2 игрока', True, 'black')
        green = pygame.Rect(red.x + 170, 300, 150, 70)
        pygame.draw.rect(SCREEN, 'green', green)
        SCREEN.blit(two_p, (green.x + 5, green.y + 20))

        bots_mode = mm_font.render('admin', True, 'black')
        purple = pygame.Rect(green.x + 170, 300, 150, 70)
        pygame.draw.rect(SCREEN, 'orange', purple)
        SCREEN.blit(bots_mode, (purple.x + 30, purple.y + 20))

        mouse = pygame.mouse.get_pos()
        if red.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            one_player = True
            main()
        elif green.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            two_player = True
            main()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        secret = pygame.Rect(mouse_x - 75, mouse_y - 35, 150, 70)
        if pygame.mouse.get_pressed()[2]:
            pygame.draw.rect(SCREEN, 'purple', secret)
            author = mm_font.render('Kebi', True, 'black')
            SCREEN.blit(author, (secret.x + 30, secret.y + 20))
        if purple.centerx == secret.centerx and purple.centery == secret.centery:
            time.sleep(1)
            hack = True
            main()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        pygame.display.update()
main_menu()
