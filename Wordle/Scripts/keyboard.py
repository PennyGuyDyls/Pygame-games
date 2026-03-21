import pygame
from Scripts.button import button
from Scripts.config import cell_width,guessnum,grey,screen,backspace,enter

keyboard = {}

row1 = "QWERTYUIOP"
row2 = "ASDFGHJKL"
row3 = "ZXCVBNM"

y_start = cell_width*guessnum+cell_width

key_w = 50
key_h = 70
gap = 5

def get_offset(row):
    return (screen.get_width()-(key_w+gap)*len(row))//2

def draw_image(key,img):
    imginuse=pygame.transform.scale(img,(key.rect.width,key.rect.height))
    screen.blit(imginuse,(key.rect.centerx-imginuse.get_width()//2,key.rect.centery-imginuse.get_height()//2))



for i, letter in enumerate(row1):
    keyboard[letter] = button(
        scale=100,
        x=i*(key_w+gap)+get_offset(row1),
        y=y_start,
        w=key_w,
        h=key_h,
        text=letter,
        colour=grey,
        hover_colour=(150,150,150)
    )


for i, letter in enumerate(row2):
    keyboard[letter] = button(
        scale=100,
        x=i*(key_w+gap)+get_offset(row2),
        y=y_start + key_h + gap,
        w=key_w,
        h=key_h,
        text=letter,
        colour=grey,
        hover_colour=(150,150,150)
    )



for i, letter in enumerate(row3):
    keyboard[letter] = button(
        scale=100,
        x=i*(key_w+gap)+get_offset(row3),
        y=y_start + 2*(key_h + gap),
        w=key_w,
        h=key_h,
        text=letter,
        colour=grey,
        hover_colour=(150,150,150)
    )

keyboard['BACKSPACE'] = button(
    scale=100,
    x=get_offset(row3)-key_w-gap-20,
    y=y_start + 2*(key_h + gap),
    w=key_w+20,
    h=key_h,
    text=None,
    colour=grey,
    hover_colour=(150,150,150),
    value='BACKSPACE'
)

keyboard['ENTER'] = button(
    scale=100,
    x=get_offset(row3)+len(row3)*(key_w+gap),
    y=y_start + 2*(key_h + gap),
    w=key_w+20,
    h=key_h,
    text=None,
    colour=grey,
    hover_colour=(150,150,150),
    value='ENTER'
)

def draw_keyboard(keyboard):
    mx, my = pygame.mouse.get_pos()
    for key in keyboard.values():
        key.update(mx, my)
        key.draw(screen)
    draw_image(keyboard['BACKSPACE'],backspace)
    draw_image(keyboard['ENTER'],enter)

def click_keyboard(keyboard):
    mx, my = pygame.mouse.get_pos()
    for key in keyboard.values():
        if key.clicked(mx,my):
            return key.value
    return False