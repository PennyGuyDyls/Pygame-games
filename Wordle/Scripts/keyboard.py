import pygame
from Scripts.button import button
from Scripts.config import cell_width,guessnum,grey,screen

keyboard = {}

row1 = "QWERTYUIOP"
row2 = "ASDFGHJKL"
row3 = "ZXCVBNM"

y_start = cell_width*guessnum+cell_width
key_w = 50
key_h = 70
gap = 5


for i, letter in enumerate(row1):
    keyboard[letter] = button(
        scale=100,
        x=i*(key_w+gap)+gap,
        y=y_start,
        w=key_w,
        h=key_h,
        text=letter,
        colour=grey,
        hover_colour=(150,150,150)
    )

offset = key_w//2
for i, letter in enumerate(row2):
    keyboard[letter] = button(
        scale=100,
        x=offset + i*(key_w+gap)+gap,
        y=y_start + key_h + gap,
        w=key_w,
        h=key_h,
        text=letter,
        colour=grey,
        hover_colour=(150,150,150)
    )


offset = key_w
for i, letter in enumerate(row3):
    keyboard[letter] = button(
        scale=100,
        x=offset + i*(key_w+gap)+gap,
        y=y_start + 2*(key_h + gap),
        w=key_w,
        h=key_h,
        text=letter,
        colour=grey,
        hover_colour=(150,150,150)
    )

def draw_keyboard(keyboard):
    mx, my = pygame.mouse.get_pos()
    for key in keyboard.values():
        key.update(mx, my)
        key.draw(screen)

def click_keyboard(keyboard):
    mx, my = pygame.mouse.get_pos()
    for key in keyboard.values():
        if key.clicked(mx,my):
            return key.text
    return False