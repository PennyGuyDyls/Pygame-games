import pygame
from Scripts.pieces import Piece
from Scripts.UI import pause_menu,screen
from Scripts.config import light, dark, pieces

def event_handle(chess,hover):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False,False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx,my = pygame.mouse.get_pos()
            row,col=my//100,mx//100
            chess.select(row,col)
            if chess.moved:
                return True,False
            else:
                if isinstance(chess.action_piece,Piece):
                    chess.action_piece.follow(mx,my)
                    return True,True
                
        elif event.type == pygame.MOUSEBUTTONUP and hover:
            mx,my = pygame.mouse.get_pos()
            row,col=my//100,mx//100
            if isinstance(chess.action_piece,Piece):
                chess.action_piece.cancel_follow()
            chess.select(row,col)
            return True,False
            
        elif event.type == pygame.MOUSEMOTION and hover:  
            mx,my=pygame.mouse.get_pos()
            if isinstance(chess.action_piece,Piece):
                chess.action_piece.follow(mx,my)

        elif event.type == pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                pause_menu()
                if isinstance(chess.action_piece,Piece):
                    chess.action_piece.cancel_follow()
                return True,False
            
    return True,hover
