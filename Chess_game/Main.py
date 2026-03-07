import pygame
from Scripts.board import game
from Scripts.UI import menu, show
from Scripts.events import event_handle
from Scripts.pieces import Piece


pygame.init()

chess=game()
hover = False
running=menu(True,chess)
while running:
    
    show(chess)
    pygame.display.flip()

    running,hover = event_handle(chess,hover)

    if chess.checkmate or chess.draw:
        show(chess)
        pygame.display.flip()
        pygame.time.wait(1500)
        running=menu(False,chess)
        chess=game()