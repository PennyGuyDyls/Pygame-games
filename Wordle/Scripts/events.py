import pygame
from Scripts.UI import valid_word
from Scripts.keyboard import click_keyboard,draw_keyboard,keyboard
def event_handle(currentword):
    running=True
    newline=False
    for event in pygame.event.get():
        
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
            letter=click_keyboard(keyboard)
            if letter:
                if letter == 'ENTER' and len(currentword)==5:
                    if valid_word(currentword):
                        newline=True
                elif len(currentword)!=0 and letter == 'BACKSPACE':
                    currentword.pop(-1)   
                elif len(letter)==1 and 'A'<=letter<='Z' and len(currentword)<5:
                    currentword.append(letter)
                
    return running,currentword,newline

    
