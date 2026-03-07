from Scripts.pieces import Piece

class history():
    def __init__(self):
        self.poslog=[]
        self.movelog=[]
        self.prevmove=[]
    def update(self,board,turn):
        self.poslog.append([board,turn])


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
    
    def calc_last_move(self,boardA,boardB):
        goto=None
        comefrom=None
        for i in range(8):
            for j in range(8):
                a = boardA[i][j]
                b = boardB[i][j]

                if type(a)==type(b):
                    continue

                if isinstance(b,Piece):
                    goto=[i,j]

                if isinstance(a,Piece):
                    comefrom=[i,j]

logs=history()