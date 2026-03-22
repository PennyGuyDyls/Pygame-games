import pygame
from Scripts.solver_input import get_inputs,screen
from Scripts.config import cell_width
def download_words(filename):
    LOAD_DIR='Wordle/Assets/'
    guesses=open(LOAD_DIR+filename,'r')
    all_words = {line.strip() for line in guesses}
    guesses.close()
    return all_words

all_words=download_words('answers.txt')
possible=all_words.copy()

def cancel_out(word,empty):
    for i in empty:
        if i in word:
            return False
        
    return True

def yellow(word,letter,pos):
    if letter not in word:
        return False
    if word[pos-1]==letter:
        return False
    return True

def allyellows(word,yellows):
    for i in yellows:
        if yellow(word,i[0],i[1]):
            continue
        return False
    return True

def green(word,letter,pos):
    return word[pos-1]==letter

def allgreens(word,greens):
    for i in greens:
        if not green(word,i[0],i[1]):
            return False
    return True

collists=[],[],[]

running=True
while running:
    running,collists=get_inputs(collists,possible)
    if collists == ([], [], []):
        possible = all_words.copy()
        continue
    greens,yellows,blacks=collists
    possible={i for i in possible if allgreens(i,greens) and allyellows(i,yellows) and cancel_out(i,blacks)}
    if len(possible)==0:
        possible=download_words('guesses.txt')
    possible={i for i in possible if allgreens(i,greens) and allyellows(i,yellows) and cancel_out(i,blacks)}
    font=pygame.font.SysFont(None, 100)
    