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

def pause_menu(chess):

    overlay()

    resumebutton=button(Cell_width, 150,200,500,150, 'RESUME', (100,100,100), (170,170,170))
    settingsbutton=button(Cell_width, 150,450,500,150, 'SETTINGS', (100,100,100), (170,170,170))

    waiting=True
    while waiting:
        resumebutton.draw(screen)
        settingsbutton.draw(screen)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False,None
            if event.type == pygame.MOUSEMOTION:
                x,y=pygame.mouse.get_pos()
                resumebutton.update(x,y)
                settingsbutton.update(x,y)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                if resumebutton.clicked(x,y):
                    return True,chess
                if settingsbutton.clicked(x,y):
                    return True,settings(chess)
        pygame.display.flip()

def settings(chess):

    piecebutton=button(Cell_width, 150,200,500,150, 'PIECE THEMES', (100,100,100), (170,170,170))
    boardbutton=button(Cell_width, 150,450,500,150, 'BOARD THEMES', (100,100,100), (170,170,170))

    waiting=True
    while waiting:
        piecebutton.draw(screen)
        boardbutton.draw(screen)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False,None
            if event.type == pygame.MOUSEMOTION:
                x,y=pygame.mouse.get_pos()
                piecebutton.update(x,y)
                boardbutton.update(x,y)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                if piecebutton.clicked(x,y):
                    piecesettings()
                    for i in range(8):
                        for j in range(8):
                            square=chess.board[i][j]
                            if isinstance(square,Piece):
                                chess.board[i][j]=type(square)(square.colour,square.posx,square.posy)
                    return chess
                if boardbutton.clicked(x,y):
                    return boardsettings(chess)
        pygame.display.flip()

def boardsettings(chess):
    import Scripts.config as config

    def draw_preview(light, dark, x, y, size):
        for i in range(2):
            for j in range(2):
                colour = light if (i+j) % 2 == 0 else dark
                pygame.draw.rect(screen, colour, (x + j*size, y + i*size, size, size))

    screen.fill((0,0,0)) 

    buttons = []
    for i in range(len(config.themes)):
        buttons.append(button(Cell_width, (i%3)*250+50, (i//3)*250+50, 200, 200, None, None, None))
        light,dark=config.themes[i]
        draw_preview(light,dark, (i%3)*2.5*Cell_width+Cell_width/2, (i//3)*2.5*Cell_width+Cell_width/2, Cell_width)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                for i in range(len(config.themes)):
                    if buttons[i].clicked(x,y):
                        config.current_theme = i
                        light,dark=config.themes[config.current_theme]
                        chess.backboard = [[dark if (row + col) % 2 == 1 else light for col in range(8)] for row in range(8)]
                        return chess
                    
def piecesettings():
    import Scripts.config as config
    def drawbuttons(btn1,btn2):
        btn1.draw(screen)
        btn2.draw(screen)
        for i,img in enumerate(config.pieces_scaled[0]):
            screen.blit(img,((i+1)*Cell_width+Cell_width/2-img.get_width()/2,Cell_width*2-img.get_height()))

        for i,img in enumerate(config.pieces_scaled[2]):
            screen.blit(img,((i+1)*Cell_width+Cell_width/2-img.get_width()/2,Cell_width*4-img.get_height()))

    set1btn=button(Cell_width, 100,100,600,100, None, (100,100,100), (170,170,170))
    set2btn=button(Cell_width, 100,300,600,100, None, (100,100,100), (170,170,170))

    screen.fill((0,0,0))

    waiting=True
    while waiting:
        drawbuttons(set1btn,set2btn)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEMOTION:
                x,y=pygame.mouse.get_pos()
                set1btn.update(x,y)
                set2btn.update(x,y)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                if set1btn.clicked(x,y):
                    config.pieces=config.pieces_scaled[0:2]
                    return None
                if set2btn.clicked(x,y):
                    config.pieces=config.pieces_scaled[2:4]
                    return None
        pygame.display.flip()
    
    pygame.display.flip()

    






