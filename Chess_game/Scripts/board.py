import pygame
from Scripts.pieces import Piece, pawn, knight, bishop, rook, queen, king, is_attacked
from Scripts.config import light,dark


class game():
    def __init__(self):
        self.backboard = [[dark if (row + col) % 2 == 1 else light for col in range(8)] for row in range(8)]

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

        self.movelog=[]
        self.turn=0

        self.dots=[]
        self.action_piece=None
        self.moving=None
        self.moved=False

        self.blackincheck=False
        self.whiteincheck=False
        self.red_square=None
        
        self.checkmate=False
        self.draw=False

    def select(self,row,col):

        if [col,row] in self.dots:
            self.board=self.action_piece.move(self.board,row,col)
            self.moved=True
            self.swap_turn()
            self.dots=[]
            self.action_piece=None
            pos = self.in_check()
            if pos:
                x,y = pos
            else:
                self.red_square=None

            self.movelog.append([Piece.clone_board(None,self.board),self.turn])
            game_end=self.check_game_end()

            if self.blackincheck or self.whiteincheck:
                self.red_square=[x,y]
                if game_end and self.blackincheck:
                    self.checkmate='BLACK'
                elif game_end and self.whiteincheck:
                    self.checkmate='WHITE'
            else:
                if game_end:
                    self.draw=True

                

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
                if isinstance(self.board[i][j],king):
                    if is_attacked(self.board, j,i,self.board[i][j].oppcolour):
                        if self.board[i][j].colour == 1:
                            self.whiteincheck=True
                        else:
                            self.blackincheck=True
                        return j,i

        return False

    def check_game_end(self):
        count=0
        for i in self.movelog:
            if self.same_pos(i[0],self.board,i[1],self.turn):
                count+=1
        if count >= 3:
            self.draw=True
            return True
        for i in range(8):
            for j in range(8):
                if isinstance(self.board[i][j],Piece) and self.board[i][j].colour == self.turn:
                    if self.board[i][j].check_legality(self.board,(self.board[i][j].check_possible_moves(self.board))) != []:
                        return False
        
        return True
    
    def same_pos(self,oldboard,newboard,oldturn,newturn):
        def boards_equal(boardA, boardB):
            for i in range(8):
                for j in range(8):
                    a = boardA[i][j]
                    b = boardB[i][j]

                    if type(a) != type(b):
                        return False

                    if a == 0 and b == 0:
                        continue

                    if a.colour != b.colour:
                        return False

                    if hasattr(a, 'moved') and a.moved != b.moved:
                        return False

                    if hasattr(a, 'enpassant_target') and a.enpassant_target != b.enpassant_target:
                        return False

            return True

        if boards_equal(oldboard, Piece.clone_board(None,newboard)) and oldturn==newturn:
            return True
        return False