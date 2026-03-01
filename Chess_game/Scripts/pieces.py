import pygame
from Scripts.config import pieces,move_sound,capture_sound
from Scripts.promotion import pawn_promotion

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
            if y==7 or y==0:
                type=pawn_promotion(self.colour,x,y)
                if type == 'QUEEN':
                    self=queen(self.colour,self.posx,self.posy)
                elif type == 'KNIGHT':
                    self=knight(self.colour,self.posx,self.posy)
                elif type == 'ROOK':
                    self=rook(self.colour,self.posx,self.posy)
                elif type == 'BISHOP':
                    self=bishop(self.colour,self.posx,self.posy)

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

            checked = self.in_check(fakeboard)
            if checked:
                dots.pop(i)
        return dots

    def in_check(self,board):
        for i in range(8):
            for j in range(8):
                if isinstance(board[i][j],king) and board[i][j].colour==self.colour:
                    if is_attacked(board, j,i ,self.oppcolour):
                        return True
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
                if is_attacked(board, i,self.posy, self.oppcolour):
                   castleL=False 
            else:
                castleL=False
                break

        castleR=True
        for i in range(5,7):
            if board[self.posy][i]==0:
                if is_attacked(board, i,self.posy, self.oppcolour):
                   castleR=False 
            else:
                castleR=False
                break
        
        if is_attacked(board, self.posx,self.posy, self.oppcolour):
            castleL,castleR=False,False

        if not self.moved:
            if isinstance(board[self.posy][0],rook) and not board[self.posy][0].moved:
                if castleL:
                    dots.append([self.posx-2,self.posy])
            if isinstance(board[self.posy][7],rook) and not board[self.posy][7].moved:
                if castleR:
                    dots.append([self.posx+2,self.posy])

        return dots

def is_attacked(board, x,y, bycolour):
    def by_knight():
        mods=[[-1,2],[1,2],[2,1],[2,-1],[1,-2],[-1,-2],[-2,-1],[-2,1]]
        for i in mods:
            xcheck=x+i[0]
            ycheck=y+i[1]
            if 0<=xcheck<8 and 0<=ycheck<8 and isinstance(board[ycheck][xcheck],knight):
                if board[ycheck][xcheck].colour == bycolour:
                    return True
        return False
    
    def by_rook():
        directions=[[0,1],[0,-1],[1,0],[-1,0]]
        for i in directions:
            xcheck,ycheck=x,y
            while True:
                xcheck+=i[0]
                ycheck+=i[1]
                if 0<=xcheck<8 and 0<=ycheck<8:
                    if isinstance(board[ycheck][xcheck],(rook,queen)) and board[ycheck][xcheck].colour == bycolour:
                        return True
                    elif board[ycheck][xcheck]!=0:
                        break
                else:
                    break
        return False
    
    def by_bishop():
        directions=[[1,1],[1,-1],[-1,1],[-1,-1]]
        for i in directions:
            xcheck,ycheck=x,y
            while True:
                xcheck+=i[0]
                ycheck+=i[1]
                if 0<=xcheck<8 and 0<=ycheck<8:
                    if isinstance(board[ycheck][xcheck],(bishop,queen)) and board[ycheck][xcheck].colour == bycolour:
                        return True
                    elif board[ycheck][xcheck]!=0:
                        break
                else:
                    break
        return False
    
    def by_pawn():
        if bycolour==0:
            mod=1
        else:
            mod=-1
        if 0<=x+1<8 and 0<=y+mod<8:
            if isinstance(board[y+mod][x+1],pawn) and board[y+mod][x+1].colour == bycolour:
                return True
        if 0<=x-1<8 and 0<=y+mod<8:
            if isinstance(board[y+mod][x-1],pawn) and board[y+mod][x-1].colour == bycolour:
                return True
            
        return False
    
    return by_knight() or by_bishop() or by_rook() or by_pawn()

