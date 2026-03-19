import pygame
from Scripts.UI import valid_word
from Scripts.keyboard import click_keyboard,draw_keyboard,keyboard
def event_handle(currentword):
    running=True
    newline=False
    for event in pygame.event.get():
        draw_keyboard(keyboard)
        if event.type==pygame.QUIT:
            running=False
            break
        elif event.type==pygame.KEYDOWN:

            if len(currentword)!=0 and event.key == pygame.K_BACKSPACE:
                currentword.pop(-1)

            elif event.key == pygame.K_RETURN and len(currentword)==5:
                if valid_word(currentword):

                    newline=True

            elif pygame.K_a <= event.key <= pygame.K_z and len(currentword)<5:
                letter = chr(event.key).upper()
                currentword.append(letter)
        
        elif event.type==pygame.MOUSEBUTTONDOWN:
            if click_keyboard(keyboard):
                letter=click_keyboard(keyboard)
                currentword.append(letter)

    return running,currentword,newline

    
