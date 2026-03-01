import pygame
from Scripts.pieces import Piece
from Scripts.config import screen,grey,red



def menu(start,chess):
    font=pygame.font.SysFont(None, 130)
    if start:
        text=font.render('CHESS',True,(255,255,255))
    else:
        surf = pygame.Surface((800,800), pygame.SRCALPHA)
        pygame.draw.rect(surf, (0,0,0,200), (0,0,800,800))
        screen.blit(surf, (0,0))
        text=font.render(chess.checkmate+' WINS',True,(255,255,255))
    screen.blit(text,(screen.get_width()//2-text.get_width()//2,150))
    pygame.display.flip()
    pygame.time.wait(1000)


    stcolour=(0,200,0)
    excolour=(200,0,0)
    font=pygame.font.SysFont(None, 85)
    if start:
        sttext=font.render('START',True,(255,255,255))
    else:
        sttext=font.render('REMATCH',True,(255,255,255))
    extext=font.render('LEAVE',True,(255,255,255))
    while True:

        pygame.draw.rect(screen, stcolour, (50,450, 300,200))
        screen.blit(sttext,(screen.get_width()//2-sttext.get_width()//2-200,550-sttext.get_height()//2))

        pygame.draw.rect(screen, excolour, (450,450, 300,200))
        screen.blit(extext,(screen.get_width()//2-extext.get_width()//2+200,550-extext.get_height()//2))
            
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if 450<=my<=650:
                    if 50<=mx<=350:
                        return True
                    elif 450<=mx<=750:
                        return False
            elif event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                if 450<=my<=650:
                    if 50<=mx<=350:
                        stcolour=(0,255,0)
                    else:
                        stcolour=(0,200,0)
                    if 450<=mx<=750:
                        excolour=(255,0,0)
                    else:
                        excolour=(200,0,0)
                else:
                    stcolour=(0,200,0)
                    excolour=(200,0,0)

def show(chess):
    def draw_dot(x,y):
        surf = pygame.Surface((100, 100), pygame.SRCALPHA)
        pygame.draw.circle(surf, (grey), (50,50), 20)
        screen.blit(surf, (x*100,y*100))

    for i in range(8):
        for j in range(8):
            pygame.draw.rect(screen,chess.backboard[i][j],(j*100,i*100 , 100, 100))
    if chess.red_square!=None:
        pygame.draw.circle(screen,red,(chess.red_square[0]*100+50,chess.red_square[1]*100+50), 48)
    for i in range(8):
        for j in range(8):
            if chess.board[i][j]==0:
                pass
            elif chess.board[i][j]!=chess.action_piece:
                screen.blit(chess.board[i][j].image,chess.board[i][j].rect)

    for i in chess.dots:
        draw_dot(i[0],i[1])    

    if isinstance(chess.action_piece,Piece):
        screen.blit(chess.action_piece.image,chess.action_piece.rect)

def pause_menu():
    def draw_button(y,height,label,colour):
        pygame.draw.rect(screen, colour, (150,y, 500,height))
        text=font.render(label,True,(255,255,255))
        screen.blit(text,(400-text.get_width()//2,y+height//2-text.get_height()//2))

    surf = pygame.Surface((800,800), pygame.SRCALPHA)
    pygame.draw.rect(surf, (0,0,0,200), (0,0,800,800))
    screen.blit(surf, (0,0))

    font = pygame.font.SysFont(None,100)
    basecolour=(100,100,100)
    hovercolour=(170,170,170)
    res=basecolour
    set=basecolour

    waiting=True
    while waiting:
        draw_button(200,150, 'RESUME',res)
        draw_button(450,150, 'SETTINGS',set)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting=False
            if event.type == pygame.MOUSEMOTION:
                x,y=pygame.mouse.get_pos()
                if 150<=x<=650:
                    if 200<=y<=350:
                        res=hovercolour
                        set=basecolour
                    elif 450<=y<=600:
                        set=hovercolour
                        res=basecolour
                    else:
                        res=basecolour
                        set=basecolour
                else:
                    res=basecolour
                    set=basecolour
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                if 150<=x<=650:
                    if 200<=y<=350:
                        return True, True
                    if 450<=y<=350:
                        settings()
        pygame.display.flip()

def settings():
    pass



