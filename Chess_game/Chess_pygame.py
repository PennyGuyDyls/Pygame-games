import pygame
light=(150,255,150)
dark=(100,255,100)
black=(0,0,0)
white=(255,255,255)
grey=(0,0,0,150)
red=(255,0,0)

class game():
    def __init__(self):
        self.backboard = [[dark if (row + col) % 2 == 0 else light for col in range(8)] for row in range(8)]

        top_bottom=[[rook(i,0,(0 if i else 7)),
                     knight(i,1,(0 if i else 7)),
                     bishop(i,2,(0 if i else 7)),
                     queen(i,3,(0 if i else 7)),
                     king(i,4,(0 if i else 7)),
                     bishop(i,5,(0 if i else 7)),
                     knight(i,6,(0 if i else 7)),
                     rook(i,7,(0 if i else 7))]
                       for i in range(2)]
        self.board = [top_bottom[1],[pawn(1,i,1) for i in range(8)]]

        for row in range(4):
            self.board.append([0 for col in range(8)])

        self.board.append([pawn(0,i,6) for i in range(8)])
        self.board.append(top_bottom[0])
        
        for i in range(8):
            for j in range(8):
                if self.board[i][j]!=0:
                    self.board[i][j].rect.center=(j*100+50,i*100+50)

        self.turn=0
        self.dots=[]
        self.action_piece=None
        self.moving=None
        self.blackincheck=False
        self.whiteincheck=False
        self.red_square=None
        self.moved=False
        self.checkmate=False
        self.stalemate=False

    def select(self,row,col):

        if [col,row] in self.dots:
            self.board=self.action_piece.move(self.board,row,col)
            self.moved=True
            self.swap_turn()
            self.dots=[]
            pos = self.in_check()
            if pos != None:
                x,y = pos
            else:
                self.red_square=None
            game_end=self.check_game_end()
            if self.blackincheck or self.whiteincheck:
                self.red_square=[x,y]
                if game_end and self.blackincheck:
                    self.checkmate='BLACK'
                elif game_end and self.whiteincheck:
                    self.checkmate='WHITE'
            else:
                if game_end:
                    self.stalemate=True

                

        elif self.board[row][col] == 0:
            self.moved=False
            self.action_piece=None
            self.dots=[]

        elif isinstance(self.board[row][col],Piece) and self.board[row][col].colour==self.turn:
            self.moved=False
            self.action_piece=self.board[row][col]
            self.dots=self.action_piece.check_possible_moves(self.board)
            self.dots=self.action_piece.check_legality(self.board,self.dots)

    def swap_turn(self):
        if self.turn:
            self.turn=0
        else:
            self.turn=1

    def in_check(self):
        self.blackincheck=False
        self.whiteincheck=False
        for i in range(8):
            for j in range(8):
                if isinstance(self.board[i][j],Piece):
                    for k in self.board[i][j].check_possible_moves(self.board):
                        if isinstance(self.board[k[1]][k[0]],king) and self.board[k[1]][k[0]].colour==self.board[i][j].oppcolour:
                            if self.board[i][j].oppcolour==0:
                                self.blackincheck=True
                                return k[0],k[1]
                            else:
                                self.whiteincheck=True
                                return k[0],k[1]
        self.blackincheck=False
        self.whiteincheck=False
        return None
    
    def check_game_end(self):
        for i in range(8):
            for j in range(8):
                if isinstance(self.board[i][j],Piece) and self.board[i][j].colour == self.turn:
                    if self.board[i][j].check_legality(self.board,(self.board[i][j].check_possible_moves(self.board))) != []:
                        return False
        return True



class Piece(pygame.sprite.Sprite):

    def check_valid_location(self,board,x,y):
        if not (0<=x<8 and 0<=y<8):
            if self.type in ['BISHOP','ROOK','QUEEN']:
                return False,False
            return False
        
        if board[y][x]==0:
            if self.type=='PAWN':
                return False
            if self.type in ['BISHOP','ROOK','QUEEN']:
                return True,False
            return True
        
        if isinstance(board[y][x],Piece) and board[y][x].colour==self.oppcolour:
            if self.type in ['BISHOP','ROOK','QUEEN']:
                return True,True
            return True
        
        if self.type in ['BISHOP','ROOK','QUEEN']:
            return False,True
        return False

    def move(self,board,y,x):
        if self.type=='PAWN':
            self.move2=False


        elif self.type == 'KING':
            self.moved=True
            if x-self.posx==2:
                board[self.posy][7].move(board,self.posy,5)
            if x-self.posx==-2:
                board[self.posy][0].move(board,self.posy,3)

        elif self.type =='ROOK':
            self.moved=True

        board[self.posy][self.posx]=0
        self.posx,self.posy=x,y
        self.rect.center = (x*100+50,y*100+50)
        if isinstance(board[y][x],Piece):
            capture_sound.play()
        else:
            move_sound.play()
        board[y][x]=self
        return board
    
    def logic_move(self,board,y,x):
        if self.type=='PAWN':
            self.move2=False


        elif self.type == 'KING':
            self.moved=True
            if x-self.posx==2:
                board[self.posy][7].logic_move(board,self.posy,5)
            if x-self.posx==-2:
                board[self.posy][0].logic_move(board,self.posy,3)

        elif self.type =='ROOK':
            self.moved=True

        board[self.posy][self.posx]=0
        self.posx,self.posy=x,y
        board[y][x]=self
        return board
    
    def logic_clone(self):
        new = object.__new__(type(self))
        new.colour = self.colour
        new.oppcolour = self.oppcolour
        new.posx = self.posx
        new.posy = self.posy
        new.moved = getattr(self, "moved", False)
        new.move2 = getattr(self, "move2", False)
        new.type = self.type
        new.mod = getattr(self,'mod',False)
        return new


    def clone_board(self,board):
        new_board = [[0 for i in range(8)] for j in range(8)]
        for y in range(8):
            for x in range(8):
                if board[y][x] == 0:
                    pass
                else:
                    new_board[y][x] = board[y][x].logic_clone()
        return new_board


    def check_legality(self,board,dots):
        for i in reversed(range(len(dots))):
            fakeboard=self.clone_board(board)
            fakeboard[self.posy][self.posx].logic_move(fakeboard,dots[i][1],dots[i][0])
            check_colour=False
            check_colour=self.in_check(board,check_colour)
            checked = self.in_check(fakeboard,check_colour)
            if checked:
                if checked=='BLACK' and self.colour==0:
                    dots.pop(i)
                elif checked=='WHITE' and self.colour==1:
                    dots.pop(i)
        return dots

    def in_check(self,board,check_colour):
        for i in range(8):
            for j in range(8):
                if isinstance(board[i][j],Piece):
                    for k in board[i][j].check_possible_moves(board):
                        if isinstance(board[k[1]][k[0]],king) and board[k[1]][k[0]].colour==board[i][j].oppcolour:
                            if board[i][j].oppcolour==0 and check_colour!='WHITE':
                                return 'BLACK'
                            elif board[i][j].oppcolour==1 and check_colour!='BLACK':
                                return 'WHITE'
        return False

    
    def checks_for_lines(self, board,directions):
        dots=[]

        for i in directions:
            newx,newy=self.posx,self.posy
            while 0<=newx<8 and 0<=newy<8:
                newx+=i[0]
                newy+=i[1]
                free,piece=self.check_valid_location(board,newx,newy)
                if free:
                    dots.append([newx,newy])
                if piece:
                    break

        return dots
    
    def follow(self,x,y):
        self.rect.center = (x,y)

    def cancel_follow(self):
        self.rect.center = (self.posx*100+50,self.posy*100+50)
    

class pawn(Piece):
    def __init__(self, colour,x,y):
        super().__init__()
        self.colour=colour
        self.posx,self.posy=x,y
        self.image=pieces[colour][0]
        self.rect = self.image.get_rect()
        self.rect.center = (x*100+50,y*100+50)
        self.type='PAWN'
        self.move2=True

        if self.colour == 1:
            self.oppcolour=0
            self.mod=1
        else:
            self.oppcolour=1
            self.mod=-1

    def check_possible_moves(self,board):
        dots=[]
        newx=self.posx
        newy=self.posy+self.mod
        if board[newy][newx]==0:
            dots.append([self.posx,self.posy+self.mod])
            newy+=self.mod
            if self.move2 and board[newy][newx]==0:
                dots.append([newx,newy])

        newx=self.posx-1
        newy=self.posy+self.mod
        if self.check_valid_location(board,newx,newy):
            dots.append([newx,newy])
        newx=self.posx+1
        if self.check_valid_location(board,newx,newy):
            dots.append([newx,newy])
        
        return dots    

class knight(Piece):
    def __init__(self, colour,x,y):
        super().__init__()
        self.colour=colour
        self.posx,self.posy=x,y
        self.image=pieces[colour][1]
        self.rect = self.image.get_rect()
        self.rect.center = (x*100+50,y*100+50)
        self.type='KNIGHT'

        if self.colour == 1:
            self.oppcolour=0
        else:
            self.oppcolour=1

    def check_possible_moves(self,board):
        dots=[]
        mods=[[-1,2],[1,2],[2,1],[2,-1],[1,-2],[-1,-2],[-2,-1],[-2,1]]
        for i in mods:
            newx=self.posx+i[0]
            newy=self.posy+i[1]
            if self.check_valid_location(board,newx,newy):
                dots.append([newx,newy])
        return dots
    
class bishop(Piece):
    def __init__(self, colour,x,y):
        super().__init__()
        self.colour=colour
        self.posx,self.posy=x,y
        self.image=pieces[colour][2]
        self.rect = self.image.get_rect()
        self.rect.center = (x*100+50,y*100+50)
        self.type='BISHOP'

        if self.colour == 1:
            self.oppcolour=0
        else:
            self.oppcolour=1

    def check_possible_moves(self,board):
        return self.checks_for_lines(board,[[1,1],[1,-1],[-1,1],[-1,-1]])

class rook(Piece):
    def __init__(self, colour,x,y):
        super().__init__()
        self.colour=colour
        self.posx,self.posy=x,y
        self.image=pieces[colour][3]
        self.rect = self.image.get_rect()
        self.rect.center = (x*100+50,y*100+50)
        self.type='ROOK'
        self.moved=False

        if self.colour == 1:
            self.oppcolour=0
        else:
            self.oppcolour=1

    def check_possible_moves(self,board):
        return self.checks_for_lines(board,[[0,1],[0,-1],[1,0],[-1,0]])

class queen(Piece):
    def __init__(self, colour,x,y):
        super().__init__()
        self.colour=colour
        self.posx,self.posy=x,y
        self.image=pieces[colour][4]
        self.rect = self.image.get_rect()
        self.rect.center = (x*100+50,y*100+50)
        self.type='QUEEN'

        if self.colour == 1:
            self.oppcolour=0
        else:
            self.oppcolour=1

    def check_possible_moves(self,board):
        return self.checks_for_lines(board,[[0,1],[0,-1],[1,0],[-1,0],[1,1],[1,-1],[-1,1],[-1,-1]])

class king(Piece):
    def __init__(self, colour,x,y):
        super().__init__()
        self.colour=colour
        self.posx,self.posy=x,y
        self.image=pieces[colour][5]
        self.rect = self.image.get_rect()
        self.rect.center = (x*100+50,y*100+50)
        self.type='KING'
        self.moved=False

        if self.colour == 1:
            self.oppcolour=0
        else:
            self.oppcolour=1

    def check_possible_moves(self,board):
        dots=[]
        for i in range(-1,2):
            for j in range(-1,2):
                newx=self.posx+i
                newy=self.posy+j
                if self.check_valid_location(board,newx,newy):
                    dots.append([newx,newy])
        
        castleL=True
        for i in range(1,4):
            if board[self.posy][i]==0:
                pass
            else:
                castleL=False
                break

        castleR=True
        for i in range(5,7):
            if board[self.posy][i]==0:
                pass
            else:
                castleR=False
                break
        
        if not self.moved:
            if isinstance(board[self.posy][0],rook) and not board[self.posy][0].moved:
                if castleL:
                    dots.append([self.posx-2,self.posy])
            if isinstance(board[self.posy][7],rook) and not board[self.posy][7].moved:
                if castleR:
                    dots.append([self.posx+2,self.posy])

        return dots


def menu(start):
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


def show():
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


pygame.init()
pygame.mixer.init()

IMG_DIR='Chess_game/Images/'
pieces_orig=[[pygame.image.load(f'{IMG_DIR}Piece{i}.{j}.png') for i in range(1,7)] for j in range(1,3)]
pieces=[[pygame.transform.scale(j,(80,85)) for j in i] for i in pieces_orig]
for i in range(2):
    pieces[i][0]=pygame.transform.scale(pieces_orig[i][0],(60,70))
    pieces[i][3]=pygame.transform.scale(pieces_orig[i][3],(70,80))

SFX_DIR='Chess_game/Sounds/'
move_sound = pygame.mixer.Sound(SFX_DIR+'Move.wav')
move_sound.set_volume(0.4)
capture_sound = pygame.mixer.Sound(SFX_DIR + 'Capture.wav')
capture_sound.set_volume(0.8)



chess=game()
screen=pygame.display.set_mode((800,800))


hover = False
running=menu(True)
while running:
    show()
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx,my = pygame.mouse.get_pos()
            row,col=my//100,mx//100
            chess.select(row,col)
            if chess.moved:
                hover=False
            else:
                hover=True
                if isinstance(chess.action_piece,Piece):
                    chess.action_piece.follow(mx,my)
        elif event.type == pygame.MOUSEBUTTONUP and hover:
            mx,my = pygame.mouse.get_pos()
            row,col=my//100,mx//100
            if isinstance(chess.action_piece,Piece):
                chess.action_piece.cancel_follow()
            chess.select(row,col)
            hover=False
            
        elif event.type == pygame.MOUSEMOTION and hover:  
            mx,my=pygame.mouse.get_pos()
            if isinstance(chess.action_piece,Piece):
                chess.action_piece.follow(mx,my)

    if chess.checkmate:
        show()
        pygame.display.flip()
        pygame.time.wait(1500)
        running=menu(False)
        chess=game()