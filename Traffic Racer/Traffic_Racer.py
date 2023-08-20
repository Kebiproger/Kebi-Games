import pygame

# Обьязательно инициализируем а то не будет надписи музыки и.т.д
pygame.init()

clock = pygame.time.Clock()

WIDTH,HEIGHT = 840,648

screen = pygame.display.set_mode((WIDTH,HEIGHT))
bg = pygame.transform.scale(pygame.image.load('imgs/background-1_0.png').convert(),\
                                                                    (WIDTH,HEIGHT))
bg_y = 0
bg_music = pygame.mixer.Sound('music/bg.mp3')
bg_music.set_volume(0.05)
bg_music.play()
icon = pygame.image.load('imgs/icon.ico')
pygame.display.set_icon(icon)

pygame.display.set_caption('Traffic Racer 1.0')  # Надпись на окне

gg = pygame.image.load('imgs/car1.png').convert_alpha()
cr = pygame.image.load('imgs/car_rect.png').convert_alpha()
blue_car = pygame.image.load('imgs\enemy1.png').convert_alpha()
white_car = pygame.image.load('imgs\enemy2.png').convert_alpha()
gruzak_car = pygame.image.load('imgs\enemy3.png').convert_alpha()
red_car = pygame.image.load('imgs\enemy4.png').convert_alpha()

enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 9000)
enemy_timer2 = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_timer2,7500)
enemy_timer3 = pygame.USEREVENT + 3
pygame.time.set_timer(enemy_timer3,11000)
enemy_timer4 = pygame.USEREVENT + 4
pygame.time.set_timer(enemy_timer4,5500)

# Движущийся машины добавляются список
car1= []
car2 = []
car3 = []
car4 = []

gg_x = 380

record = pygame.font.Font('font.ttf', 30)
timer = 0

lose = pygame.font.Font('font.ttf',80)
lose_label = lose.render('Игра окончена!', True,'white')

restart = pygame.font.Font(None, 60)
restart_label = restart.render('Играть Снова', True, 'White')
restart_rect = restart_label.get_rect(topleft=(270,300))
            # Кардинаты прямоугольника(вооброжаемого) должны быть обьязательно
exit = pygame.font.Font(None,60)
exit_label = exit.render('Выйти',True, 'white')
exit_rect = exit_label.get_rect(topleft=(330,380))

start_icon = pygame.transform.scale(pygame.image.load('imgs/blur.jpeg').convert(),\
                                                                     (WIDTH,HEIGHT))
start_label = pygame.font.Font('font.ttf',100)
start_render = start_label.render('Играть', True, 'White')
start_rect = start_render.get_rect(topleft=(280,300))

author = record.render('Created by KebiProger',True,'Black')

start = True
running = False
gaming = True

while start:
    screen.blit(start_icon,(0,0))
    screen.blit(start_render,(280,300))
    screen.blit(author,(WIDTH - author.get_width()-10,HEIGHT - 40))

    mouse = pygame.mouse.get_pos()
    if start_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
        running = True
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False

    while running:
        screen.blit(bg,(0,bg_y))
        screen.blit(bg,(0,bg_y - 200))
        bg_y += 5
        if bg_y > 210:
            bg_y = 0

        screen.blit(gg,(gg_x, 500))
        clock.tick(70)

        record_read = open('record.txt')
        record_show = record_read.readline()
        record_render = record.render(f'{record_show}m', True, 'Yellow')
        if timer > int(record_show):
            record_write = open('record.txt','w')
            record_write.write(str(timer))
            record_write.close()

        total_scores = record.render(f'Текущее очко {timer}m. Налучший рекорд {record_show}m'\
                                                                            , True, 'Yellow')

        # Задний фон очков и рекорда
        record_label = record.render(f'{timer}m', True,('white'))
        pygame.draw.rect(screen, '#2b2d2f', (20, 10, record_render.get_width()+ 20, 80))
        screen.blit(record_label,(30,10))
        screen.blit(record_render,(30,50))

        if gaming:
            car_rect = cr.get_rect(topleft=(gg_x,500))
            timer+= 1  # Сделал таймер именно тут, потому что оно не было бы статичным
            if car1:
                for index,el in enumerate(car1):
                    screen.blit(blue_car,el)
                    el.y += 3
                    if el.y > 700 and len(car1) > 0:
                        car1.pop(index)
                    if car_rect.colliderect(el):
                        gaming = False
                        car1.pop(index)
            if car2:
                for i,elem in enumerate(car2):
                    screen.blit(white_car,elem)
                    elem.y += 2
                    if elem.y > 700 and len(car2) > -0:
                        car2.pop(i)
                    if car_rect.colliderect(elem):
                        gaming = False
                        car2.pop(i)

            if car3:
                for index1,elem1 in enumerate(car3):
                    screen.blit(gruzak_car,elem1)
                    elem1.y += 1.5
                    if elem1.y > 700 and len(car3) > -0:
                        car3.pop(index1)
                    if car_rect.colliderect(elem1):
                        gaming = False
                        car3.pop(index1)
            if car4:
                for index4,elem4 in enumerate(car4):
                    screen.blit(red_car,elem4)
                    elem4.y += 3
                    if elem4.y > 700 and len(car4) > -0:
                        car4.pop(index4)
                    if car_rect.colliderect(elem4):
                        gaming = False
                        car4.pop(index4)


            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and gg_x > 140 or keys[pygame.K_LEFT] and gg_x > 140:
                gg_x -= 6
            if keys[pygame.K_d] and gg_x < 635 or keys[pygame.K_RIGHT] and gg_x < 635:
                gg_x += 6
        else:
            bg_music.set_volume(0.01)
            screen.fill("#2b2d2f")
            screen.blit(lose_label,(160,70))
            screen.blit(total_scores,(150,200))

            # Координатам должен являться имеено rect
            screen.blit(exit_label,exit_rect)
            screen.blit(restart_label, restart_rect)

            mouse = pygame.mouse.get_pos()
            if restart_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                timer = 0
                bg_music.stop()
                gaming = True
                gg_x = 380
                car1.clear()
                car2.clear()
                car3.clear()
                car4.clear()
                bg_music.set_volume(0.03)
                # bg_music.play()
            elif exit_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                running = False
                start = False

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                running = False
            if event.type == enemy_timer:
                car1.append(blue_car.get_rect(topleft=(180,-200)))
            if event.type == enemy_timer2:
                car2.append(white_car.get_rect(topleft=(330,-200)))
            if event.type == enemy_timer3:
                car3.append(gruzak_car.get_rect(topleft=(450,-200)))
            if event.type == enemy_timer4:
                car4.append(red_car.get_rect(topleft=(580,-200)))
