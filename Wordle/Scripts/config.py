import pygame
from random import randint
pygame.init()

cell_width=50
guessnum=6

font=pygame.font.SysFont(None, cell_width)
screen=pygame.display.set_mode((5*cell_width*1.1+cell_width/10,guessnum*cell_width*1.1+cell_width/10+300))

LOAD_DIR='Wordle/Assets/'
answers=open(LOAD_DIR+'answers.txt','r')
for i in range(randint(1,1738)):
    answers.readline()
realword=[i for i in answers.readline().strip()]
answers.close()

guesses=open(LOAD_DIR+'guesses.txt','r')
possible = {line.strip() for line in guesses}
guesses.close()

backspace=pygame.image.load(LOAD_DIR+'backspace.png').convert_alpha()
enter=pygame.image.load(LOAD_DIR+'enter.png').convert_alpha()

grey=(100,100,100)
green=(0,255,0)
yellow=(230,230,0)
black=(20,20,20)