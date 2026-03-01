import pygame
from Scripts.config import light, dark, pieces,screen


def pawn_promotion(colour,x,y):
    def show_option(piece,x,y):
        if piece == 'QUEEN':
            img=pieces[colour][4]
        elif piece == 'KNIGHT':
            img=pieces[colour][1]
        elif piece == 'ROOK':
            img=pieces[colour][3]
        elif piece == 'BISHOP':
            img=pieces[colour][2]

        pygame.draw.rect(screen,(dark if (x + y) % 2 == 0 else light),(x*100,y*100,100,100))
        screen.blit(img,(x*100+50-img.get_width()//2,y*100+50-img.get_height()//2))

    origy=y

    surf = pygame.Surface((800,800), pygame.SRCALPHA)
    pygame.draw.rect(surf, (0,0,0,200), (0,0,800,800))
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
                if x*100<mx<(x+1)*100:
                    if origy==0:
                        for i in range(4):
                            if i*100<my<(i+1)*100:
                                return options[i]
                    elif origy==7:
                        for i in range(7,3,-1):
                            if i*100<my<(i+1)*100:
                                return options[7-i]
                            