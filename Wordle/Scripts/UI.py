import pygame
from Scripts.config import screen,  cell_width,guessnum,  realword,possible,  grey,green,yellow,black

def background():
    for i in range(guessnum):
        for j in range(5):
            w=j*cell_width*1.1+cell_width/10 
            h=i*cell_width*1.1+cell_width/10
            pygame.draw.rect(screen,grey,(w,h,cell_width,cell_width))

def draw_box(x,y,colour,letter):
    x=x*cell_width*1.1+cell_width/10
    y=y*cell_width*1.1+cell_width/10
    pygame.draw.rect(screen,colour,(x,y,cell_width,cell_width))
    if letter!=None:
        font=pygame.font.SysFont(None, cell_width)
        letter=font.render(letter,True,(255,255,255))
        screen.blit(letter,(x+cell_width/2-letter.get_width()/2,y+cell_width/2-letter.get_height()/2))

def type_in(allwords):
    for i in range(5):
        draw_box(i,len(allwords)-1,grey,None)
    for index,i in enumerate(allwords[-1]):
        draw_box(index,len(allwords)-1,grey,i)

def complete_row(allwords):
    colours=[black for i in range(5)]

    check=allwords[-1].copy()
    fake=realword.copy()
    import Scripts.keyboard as keyboard

    for i in check:
        keyboard.keyboard[i].colour=black
        keyboard.keyboard[i].hover_colour=black
    for i in reversed(range(len(check))):
        if check[i] == fake[i]:
            keyboard.keyboard[check[i]].colour=(0,200,0)
            keyboard.keyboard[check[i]].hover_colour=green
            colours[i]=green
            fake.pop(i)

    for i in range(len(check)):
        if check[i] in fake and colours[i]==black:
            keyboard.keyboard[check[i]].colour=(200,200,0)
            keyboard.keyboard[check[i]].hover_colour=yellow
            colours[i]=yellow
            fake.remove(check[i])

    for index,i in enumerate(allwords[-1]):
        draw_box(index,len(allwords)-1,colours[index],i)

def valid_word(word):
    check=''
    for i in word:
        check+=i

    return check in possible
    
            