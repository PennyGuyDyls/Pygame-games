import pygame
from Scripts.pieces import Piece
from Scripts.config import screen,grey,red,Cell_width
from Scripts.button import button
def overlay():
    surf = pygame.Surface((8*Cell_width,8*Cell_width), pygame.SRCALPHA)
    pygame.draw.rect(surf, (0,0,0,200), (0,0,8*Cell_width,8*Cell_width))
    screen.blit(surf, (0,0))


def menu(start,chess):
    font=pygame.font.SysFont(None, 130)
    if start:
        text=font.render('CHESS',True,(255,255,255))
    else:
        overlay()
        if chess.checkmate:
            text=font.render(chess.checkmate+' WINS',True,(255,255,255))
        if chess.draw:
            text=font.render('DRAW',True,(255,255,255))
    screen.blit(text,(screen.get_width()//2-text.get_width()//2,Cell_width*1.5))
    pygame.display.flip()
    pygame.time.wait(1000)

    font=pygame.font.SysFont(None, 85)
    if start:
        sttext='START'
    else:
        sttext='REMATCH'
    extext='LEAVE'

    startbutton=button(Cell_width, 50, 450, 300, 200, sttext, (0,200,0), (0,255,0))
    exitbutton=button(Cell_width, 450,450, 300, 200, extext, (200,0,0), (255,0,0))

    while True:

        startbutton.draw(screen)
        exitbutton.draw(screen)
            
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if startbutton.clicked(mx,my):
                    return True
                if exitbutton.clicked(mx,my):
                    return False
            elif event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                startbutton.update(mx,my)
                exitbutton.update(mx,my)

def show(chess):
    def draw_dot(x,y):
        surf = pygame.Surface((Cell_width, Cell_width), pygame.SRCALPHA)
        pygame.draw.circle(surf, (grey), (Cell_width/2,Cell_width/2), Cell_width/5)
        screen.blit(surf, (x*Cell_width,y*Cell_width))

    for i in range(8):
        for j in range(8):
            pygame.draw.rect(screen,chess.backboard[i][j],(j*Cell_width,i*Cell_width , Cell_width, Cell_width))
    if chess.red_square!=None:
        pygame.draw.circle(screen,red,(chess.red_square[0]*Cell_width+Cell_width/2,chess.red_square[1]*Cell_width+Cell_width/2), Cell_width/2-2)
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

    overlay()

    resumebutton=button(Cell_width, 150,200,500,150, 'RESUME', (100,100,100), (170,170,170))
    settingsbutton=button(Cell_width, 150,450,500,150, 'SETTINGS', (100,100,100), (170,170,170))

    waiting=True
    while waiting:
        resumebutton.draw(screen)
        settingsbutton.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, False
            if event.type == pygame.MOUSEMOTION:
                x,y=pygame.mouse.get_pos()
                resumebutton.update(x,y)
                settingsbutton.update(x,y)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                if resumebutton.clicked(x,y):
                    return True,False
                if settingsbutton.clicked(x,y):
                    settings()
        pygame.display.flip()

def settings():
   pass


