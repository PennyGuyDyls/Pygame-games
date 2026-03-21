import pygame
from Scripts.events import event_handle
from Scripts.UI import background,complete_row,type_in
from Scripts.keyboard import draw_keyboard,keyboard

pygame.init()
clock=pygame.time.Clock()

allwords=[[]]
background()

running=True
newline=False
while running:
    clock.tick(50)

    type_in(allwords)
    draw_keyboard(keyboard)
    pygame.display.flip()

    running,allwords[-1],newline=event_handle(allwords[-1])

    if newline:
        complete_row(allwords)
        newline=False
        allwords.append([])
