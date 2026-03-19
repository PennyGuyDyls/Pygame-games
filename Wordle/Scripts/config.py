import pygame
from random import randint
pygame.init()

cell_width=100
guessnum=6

font=pygame.font.SysFont(None, cell_width//5)
screen=pygame.display.set_mode((5*cell_width*1.1+cell_width/10,guessnum*cell_width*1.1+cell_width/10+300))

TXT_DIR='Wordle/Assets/'
answers=open(TXT_DIR+'answers.txt','r')
for i in range(randint(1,1738)):
    answers.readline()
realword=[i for i in answers.readline().strip()]
answers.close()

guesses=open(TXT_DIR+'guesses.txt','r')
possible = {line.strip() for line in guesses}
guesses.close()

grey=(100,100,100)
green=(0,255,0)
yellow=(255,255,0)
black=(20,20,20)