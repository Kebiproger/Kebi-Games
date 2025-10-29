import pygame

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((1920, 1080))

walk_right = [
    pygame.image.load('images/right1.png').convert_alpha(),
    pygame.image.load('images/right2.png').convert_alpha(),
    pygame.image.load('images/right3.png').convert_alpha(),
    pygame.image.load('images/right4.png').convert_alpha(),
    pygame.image.load('images/right5.png').convert_alpha(),
    pygame.image.load('images/right6.png').convert_alpha(),
    pygame.image.load('images/right7.png').convert_alpha(),
    pygame.image.load('images/right8.png').convert_alpha(),
    pygame.image.load('images/right9.png').convert_alpha(),
    pygame.image.load('images/right11.png').convert_alpha(),
    pygame.image.load('images/right12.png').convert_alpha(),
    pygame.image.load('images/right13.png').convert_alpha(),
    pygame.image.load('images/right14.png').convert_alpha(),
    pygame.image.load('images/right15.png').convert_alpha(),
    pygame.image.load('images/right16.png').convert_alpha(),
    pygame.image.load('images/right17.png').convert_alpha(),
    pygame.image.load('images/right18.png').convert_alpha(),
    pygame.image.load('images/right19.png').convert_alpha(),
    pygame.image.load('images/right20.png').convert_alpha(),
    pygame.image.load('images/right21.png').convert_alpha(),
    pygame.image.load('images/right22.png').convert_alpha(),
    pygame.image.load('images/right23.png').convert_alpha(),
    pygame.image.load('images/right24.png').convert_alpha(),
    pygame.image.load('images/right25.png').convert_alpha(),
    pygame.image.load('images/right26.png').convert_alpha(),
]
walk_left = [
    pygame.image.load('images/left1.png').convert_alpha(),
    pygame.image.load('images/left2.png').convert_alpha(),
    pygame.image.load('images/left3.png').convert_alpha(),
    pygame.image.load('images/left4.png').convert_alpha(),
    pygame.image.load('images/left5.png').convert_alpha(),
    pygame.image.load('images/left6.png').convert_alpha(),
    pygame.image.load('images/left7.png').convert_alpha(),
    pygame.image.load('images/left8.png').convert_alpha(),
    pygame.image.load('images/left9.png').convert_alpha(),
    pygame.image.load('images/left10.png').convert_alpha(),
    pygame.image.load('images/left11.png').convert_alpha(),
    pygame.image.load('images/left12.png').convert_alpha(),
    pygame.image.load('images/left13.png').convert_alpha(),
    pygame.image.load('images/left14.png').convert_alpha(),
    pygame.image.load('images/left15.png').convert_alpha(),
    pygame.image.load('images/left16.png').convert_alpha(),
    pygame.image.load('images/left17.png').convert_alpha(),
    pygame.image.load('images/left18.png').convert_alpha(),
    pygame.image.load('images/left19.png').convert_alpha(),
    pygame.image.load('images/left20.png').convert_alpha(),
    pygame.image.load('images/left21.png').convert_alpha(),
    pygame.image.load('images/left22.png').convert_alpha(),
    pygame.image.load('images/left23.png').convert_alpha(),
    pygame.image.load('images/left24.png').convert_alpha(),
    pygame.image.load('images/left25.png').convert_alpha(),
    pygame.image.load('images/left26.png').convert_alpha(),
]

bg = pygame.image.load('images/background2.png').convert()
screen.blit(bg,(0,0))

ghost = pygame.image.load('images/spider.png').convert_alpha()
ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 1700)
spider_timer = pygame.USEREVENT + 2
pygame.time.set_timer(spider_timer, 2000)

spider = [
    pygame.image.load('images/spider1.png'),
    pygame.image.load('images/spider2.png'),
    pygame.image.load('images/spider3.png'),
    pygame.image.load('images/spider4.png'),
    pygame.image.load('images/spider5.png'),
    pygame.image.load('images/spider6.png'),
    pygame.image.load('images/spider7.png'),
    pygame.image.load('images/spider8.png'),
    pygame.image.load('images/spider9.png'),
]
spider_anim_count = 0

ghost_list = []
spider_list = []

player_anim_count = 0

bg_x = 0

player_speed = 15
player_x = 250
player_y = 650
rect_player = pygame.image.load('images/rect_player.png').convert_alpha()

jump = False
jump_count = 11

background_music = pygame.mixer.Sound('music/background_song.mp3')
background_music.set_volume(0.05)
background_music.play()
loosing_song = pygame.mixer.Sound('music/losing_song.wav')
knife_sound = pygame.mixer.Sound('music/knife.mp3')
jump_sound = pygame.mixer.Sound('music/jump.mp3')

label = pygame.font.Font('fonts/font.ttf', 140)
lebel2 = pygame.font.Font('fonts/font.ttf', 90)
exit = pygame.font.Font('fonts/font.ttf', 90)
time_show = pygame.font.Font('fonts/font.ttf', 40)
knife_count = pygame.font.Font(None, 60)
record = pygame.font.Font('fonts/font.ttf', 40)

lose_label = label.render('Вы проиграли', True,('Red'))
restart_label = lebel2.render('Играть снова', True,('White'))
exit_label = exit.render('Выйти', True, ('White'))

times = 0

restart_rect = restart_label.get_rect(topleft = (680, 480))
exit_rect = exit_label.get_rect(topleft = (800, 640))

knife = pygame.image.load('images/knife.png').convert_alpha()
knifes = []
knifes_left = 1

gameplay = True
running = True
while running:
    clock.tick(30)
    times += 1
    time_lebel = time_show.render(f'Your Score:{times}', True, 'White')
    screen.blit(bg,(bg_x,0))
    screen.blit(bg,(bg_x + 1900,0))
    knife_label = knife_count.render(f'{knifes_left}x', True, ('White'))
    screen.blit(knife_label,(250,157))
    screen.blit(knife,(307,167))
    screen.blit(time_lebel,(420,147))

    record_score = open('record.txt', 'r')
    record_show = record_score.readline()
    record_render = record.render(f'Record:{record_show}', True, 'White')
    if times > int(record_show):
        record_score = open('record.txt', 'w')
        record_score.write(str(times))

    screen.blit(record_render,(1000,147))

    if gameplay:
        player_rect = rect_player.get_rect(topleft = (player_x, player_y))

        if spider_list:
            for index1, el1 in enumerate(spider_list):
               screen.blit(spider[spider_anim_count], el1)
               spider_anim_count += 1
               if spider_anim_count > 6:
                   spider_anim_count = 0
               if times >= 500 and times <= 1000:
                   el1.x -= 20
               if times >= 1000:
                   el1.x -= 25
               if times < 500:
                   el1.x -=15
               if el1.x < -10 and len(spider_list) > -0:
                    spider_list.pop(index1)
               if player_rect.colliderect(el1):
                    gameplay = False
                    loosing_song.set_volume(0.1)
                    loosing_song.play()

        if ghost_list:
            for i, el in enumerate(ghost_list):
                screen.blit(ghost, el)
                if times > 500 and times < 1000:
                   el.x -= 20
                if times > 1000:
                   el.x -= 25
                if times < 500:
                   el.x -=15
                if el.x < -10:
                    ghost_list.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False
                    loosing_song.set_volume(0.1)
                    loosing_song.play()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and player_x < 1580:
            player_x += player_speed
        elif keys[pygame.K_a] and player_x > 180:
            player_x -= player_speed
        if not jump:
            if keys[pygame.K_SPACE]:
                jump = True
                jump_sound.set_volume(0.04)
                jump_sound.play()
        else:
            if jump_count >= -11:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                jump = False
                jump_count = 11

        player_anim_count += 1
        if player_anim_count > 24:
            player_anim_count = 0

        bg_x -= 5
        if bg_x <= -1900:
            bg_x = 0

        if knifes:
            for (i, el) in enumerate(knifes):
                screen.blit(knife, (el.x, el.y))
                el.x += 30
                if el.x > 1690 and len(knifes) > -0:
                    knifes_left += 1
                    knifes.pop(i)


                if ghost_list:
                    for (index, ghost_element) in enumerate(ghost_list):
                        if el.colliderect(ghost_element):
                            ghost_list.pop(index)
                            knifes_left += 1
                            knifes.pop(i)


    else:
        background_music.stop()
        screen.fill((101, 67, 33))
        screen.blit(lose_label,(500, 240))
        screen.blit(restart_label, restart_rect)
        screen.blit(exit_label ,exit_rect)
        times = 0

        mouse = pygame.mouse.get_pos()
        if restart_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 250
            ghost_list.clear()
            knifes.clear()
            knifes_left = 1
            spider_list.clear()
            background_music.stop()
            background_music.play()

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.display.iconify()
            if event.key == pygame.K_q and knifes_left > 0:
                knifes.append(knife.get_rect(topleft =(player_x + 40, player_y + 170)))
                knife_sound.set_volume(0.1)
                knife_sound.play()
                knifes_left -= 1

        if event.type == ghost_timer:
            ghost_list.append(ghost.get_rect(topleft = (1930,545)))
        if event.type == spider_timer:
            if spider_anim_count > 8:
                    spider_anim_count = 0
            spider_list.append(spider[spider_anim_count].get_rect(topleft = (1930,750)))

    mouse = pygame.mouse.get_pos()
    if exit_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
        running = False
