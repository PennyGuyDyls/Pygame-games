import pygame

def menu():
    display = pygame.display.set_mode((1050,1000))

    IMG_DIR='Arcade/display_Images/'
    connect4_orig = pygame.image.load(IMG_DIR+"connect_4.png")
    connect4_img = pygame.transform.scale(connect4_orig, (150,150))
    minesweeper_orig = pygame.image.load(IMG_DIR+"Mine_sweeper.png")
    minesweeper_img = pygame.transform.scale(minesweeper_orig, (150,150))
    snake_orig = pygame.image.load(IMG_DIR+"Snake.png")
    snake_img = pygame.transform.scale(snake_orig, (150,150))
    pong_orig = pygame.image.load(IMG_DIR+"Pong.png")
    pong_img = pygame.transform.scale(pong_orig, (150,150))
    spaceinvaders_orig=pygame.image.load(IMG_DIR+"Space_Invaders.png")
    spaceinvaders_img = pygame.transform.scale(spaceinvaders_orig, (150,150))
    games_orig = [connect4_orig,minesweeper_orig,snake_orig,pong_orig,spaceinvaders_orig]
    games = [connect4_img, minesweeper_img, snake_img, pong_img, spaceinvaders_img]
    base_locations=[[i*games[i].get_width()*4/3+games[i].get_width()*1/3, 50] for i in range(len(games))]
    locations=base_locations.copy()
    
    pygame.display.flip()
    while True:
        display.fill((0,0,0))
        for i in range(len(games)):
            display.blit(games[i], locations[i])
        pygame.display.flip()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return 'exit'

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx,my=pygame.mouse.get_pos()
                for i in range(len(games)):
                    if locations[i][0]<=mx<=locations[i][0]+games[i].get_width() and locations[i][1]<=my<=locations[i][1]+games[i].get_height():
                        return i
                
            elif event.type == pygame.MOUSEMOTION:
                mx,my=pygame.mouse.get_pos()
                click=None
                for i in range(len(games)):
                    if locations[i][0]<=mx<=locations[i][0]+games[i].get_width() and locations[i][1]<=my<=locations[i][1]+games[i].get_height():
                        click=i
                        break

                for i in range(len(games)):
                    if i == click:
                        games[i]=pygame.transform.scale(games_orig[i], (180,180))
                        display.blit(games[i], (500,500))
                        locations[i]=(base_locations[i][0]-15, 35)
                    else:
                        games[i]=pygame.transform.scale(games_orig[i], (150,150))
                        locations[i]=(base_locations[i])

            


pygame.init()

play=True
while play:
    game=menu()

    if game==0:
        from Connect_4.Connect_4_pygame import run
        run()
    elif game==1:
        from Mine_sweeper.Minesweeper_pygame import run
        run()
    elif game==2:
        from Snake.Snake_Pygame import run
        run()
    elif game==3:
        from Pong.Pong_pygame import run
        run()
    elif game==4:
        from Space_Invaders.Space_invaders_Pygame import run
        run()
    elif game=='exit':
        play=False