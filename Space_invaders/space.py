import pygame
import os
import random

pygame.init() #  Иницализация обьязательна

WIDTH,HEIGHT = 1080,720
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Space Invaders 2.0')
icon = pygame.image.load(os.path.join('images', 'icon.ico'))
pygame.display.set_icon(icon)

# Враги
PURPLE_SHIP = pygame.image.load(os.path.join('images', 'purple.png'))
MAGENTA_SHIP = pygame.image.load(os.path.join('images', 'magenta.png'))
BLUE_SHIP = pygame.image.load(os.path.join('images', 'blue.png'))
CYAN_SHIP = pygame.image.load(os.path.join('images', 'cyan.png'))
PINK_SHIP = pygame.image.load(os.path.join('images', 'pink.png'))

PLAYER_SHIP = pygame.image.load(os.path.join('images', 'player.png'))

LASER = pygame.image.load(os.path.join('images', 'laser.png'))

SHOOT_SOUND = pygame.mixer.Sound(os.path.join('sound', 'shoot.wav'))
SHOOT_SOUND.set_volume(0.1)

COLL_SOUND = pygame.mixer.Sound(os.path.join('sound', 'collision.wav'))
COLL_SOUND.set_volume(0.1)

INVADER_SOUND = pygame.mixer.Sound(os.path.join('sound', 'invader.wav'))
INVADER_SOUND.set_volume(0.1)

BG = pygame.transform.scale(pygame.image.load(os.path.join('images', 'bg.png')), (WIDTH,HEIGHT))

class Laser():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self,height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100) -> None:
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = LASER
        self.lasers = []
        self.cool_counter = 0

    def draw(self, window):
        window.blit(self.ship_img,(self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                if obj.health > 0:
                    obj.health -= 10
                    self.lasers.remove(laser)
                    INVADER_SOUND.play()

    def cooldown(self):
        if self.cool_counter >= self.COOLDOWN:
            self.cool_counter = 0
        elif self.cool_counter > 0:
            self.cool_counter += 1

    def shoot(self):
        if self.cool_counter == 0:
            laser = Laser(self.x + 50 ,self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_counter = 1
            SHOOT_SOUND.play()

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img =PLAYER_SHIP
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if len(self.lasers) > 0:
                            self.lasers.remove(laser)
                        COLL_SOUND.play()

    def draw(self, window, color):
        if self.health > 0:
            super().draw(window)
            self.healthbar(window, color)

    def healthbar(self, window, color):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 5))
        pygame.draw.rect(window, color, (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health),5))


class Enemy(Ship):
    COLOR_MAP = {
        'magenta' : (MAGENTA_SHIP),
        'purple' : (PURPLE_SHIP),
        'blue' : (BLUE_SHIP),
        'cyan' : (CYAN_SHIP),
        'pink' : (PINK_SHIP)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x , y, health)
        self.ship_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, speed):
        self.y += speed

    def shoot(self):
        if self.cool_counter == 0:
            laser = Laser(self.x + 30 ,self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_counter = 1


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    run = True
    FPS = 60
    level = 0
    lives = 0
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont('Roboto Mono', 35)
    lose_font = pygame.font.SysFont('Roboto Mono', 30)
    lost_font = pygame.font.SysFont('Roboto Mono', 55)

    enemies = []
    wave_length = 5
    enemy_vel = 1.4
    laser_vel = 4.5

    player_speed = 7
    player2 = Player((WIDTH / 2)-50,HEIGHT-110)
    player = Player((WIDTH / 2)- player2.get_width() - 100,HEIGHT-110)

    lost = False
    lost_count = 0

    def redraw_window():
        WINDOW.blit(BG,(0,0))

        lives_label = lose_font.render(f'Пропущенных кораблей: {lives}/5', True, 'White')
        level_label = main_font.render(f'Уровень: {level}', True, 'White')

        for enemy in enemies:
            enemy.draw(WINDOW)

        player.draw(WINDOW, 'Lime')
        first_p = main_font.render('1', True, 'Lime')
        WINDOW.blit(first_p, (player.x + 47, player.y - 20))

        player2.draw(WINDOW, 'PURPLE')
        second_p = main_font.render('2', True, 'PURPLE')
        WINDOW.blit(second_p, (player2.x + 47, player2.y - 20))

        if lost:
             lost_label = lost_font.render('Вы проиграли!', 1, 'White')
             WINDOW.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, HEIGHT/2))

        WINDOW.blit(lives_label,(10,15))
        WINDOW.blit(level_label,(WIDTH - level_label.get_width()-10,10))

        pygame.display.flip()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives >= 10 or player.health <= 0 and player2.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 2:
                run = False
            else:
                continue

        if len(enemies) < wave_length:
                enemy = Enemy(random.randint(50,WIDTH - 100), random.randint(-500, -100),random.choice \
                                                             (['magenta','purple','blue','pink','cyan']))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        if player.health > 0:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and player.x > 0:
                player.x -= player_speed
            if keys[pygame.K_d] and player.x < WIDTH - player.get_width():
                player.x += player_speed
            if keys[pygame.K_w] and player.y > 0:
                player.y -= player_speed
            if keys[pygame.K_s] and player.y  + player.get_height() + 20 < HEIGHT :
                player.y += player_speed
            if keys[pygame.K_SPACE]:
                player.shoot()

        # Второй игрок
        if player2.health > 0:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player2.x > 0:
                player2.x -= player_speed
            if keys[pygame.K_RIGHT] and player2.x < WIDTH - player2.get_width():
                player2.x += player_speed
            if keys[pygame.K_UP] and player2.y > 0:
                player2.y -= player_speed
            if keys[pygame.K_DOWN] and player2.y  + player2.get_height() + 20 < HEIGHT :
                player2.y += player_speed
            if keys[pygame.K_RETURN]:
                player2.shoot()

        for enemy in enemies:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            enemy.move_lasers(laser_vel, player2)

            if random.randrange(0,120) == 1:
                enemy.shoot()
            if player.health > 0:
                if collide(enemy,player):
                    player.health -= 10
                    enemies.remove(enemy)
                    INVADER_SOUND.play()

            # Второй игрок
            if player2.health > 0:
                if collide(enemy,player2):
                    player2.health -= 10
                    enemies.remove(enemy)
                    INVADER_SOUND.play()

            if enemy.y + enemy.get_height() > HEIGHT:
                lives += 1
                enemies.remove(enemy)
                INVADER_SOUND.play()

        player.move_lasers(-laser_vel, enemies)
        player2.move_lasers(-laser_vel, enemies)

def main_menu():
    title_font = pygame.font.SysFont('Roboto Mono', 60)
    run = True
    while run:
        WINDOW.blit(BG,(0,0))
        title_label = title_font.render('Нажмите ЛКМ чтобы начать...', 1, 'White')
        WINDOW.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 300))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

main_menu()
