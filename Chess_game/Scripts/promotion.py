import pygame
from Scripts.config import themes,current_theme, pieces, screen, Cell_width


def pawn_promotion(colour,x,y):
    from Scripts.config import themes,current_theme
    light,dark=themes[current_theme]
    def show_option(piece,x,y):
        if piece == 'QUEEN':
            img=pieces[colour][4]
        elif piece == 'KNIGHT':
            img=pieces[colour][1]
        elif piece == 'ROOK':
            img=pieces[colour][3]
        elif piece == 'BISHOP':
            img=pieces[colour][2]

        pygame.draw.rect(screen,(light if (x + y) % 2 == 0 else dark),(x*Cell_width,y*Cell_width,Cell_width,Cell_width))
        screen.blit(img,(x*Cell_width+Cell_width/2-img.get_width()//2,y*Cell_width+Cell_width/2-img.get_height()//2))

    origy=y

    surf = pygame.Surface((8*Cell_width,8*Cell_width), pygame.SRCALPHA)
    pygame.draw.rect(surf, (0,0,0,200), (0,0,8*Cell_width,8*Cell_width))
    screen.blit(surf, (0,0))

    options=['QUEEN','KNIGHT','ROOK','BISHOP']
    for i in range(4):
        show_option(options[i],x,y)
        if y>=4:
            y-=1
        else:
            y+=1
    pygame.display.flip()
    waiting=True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx,my=pygame.mouse.get_pos()
                if x*Cell_width<mx<(x+1)*Cell_width:
                    if origy==0:
                        for i in range(4):
                            if i*Cell_width<my<(i+1)*Cell_width:
                                return options[i]
                    elif origy==7:
                        for i in range(7,3,-1):
                            if i*Cell_width<my<(i+1)*Cell_width:
                                return options[7-i]
                            