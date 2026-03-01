import pygame

screen=pygame.display.set_mode((800,800))

pygame.mixer.init()

IMG_DIR='Chess_game/Images/'
pieces_orig=[[pygame.image.load(f'{IMG_DIR}Piece{i}.{j}.png') for i in range(1,7)] for j in range(1,3)]
pieces=[[pygame.transform.scale(j,(80,85)) for j in i] for i in pieces_orig]
for i in range(2):
    pieces[i][0]=pygame.transform.scale(pieces_orig[i][0],(60,70))
    pieces[i][3]=pygame.transform.scale(pieces_orig[i][3],(70,80))

SFX_DIR='Chess_game/Sounds/'
move_sound = pygame.mixer.Sound(SFX_DIR+'Move.wav')
move_sound.set_volume(0.4)
capture_sound = pygame.mixer.Sound(SFX_DIR + 'Capture.wav')
capture_sound.set_volume(0.8)

light=(150,255,150)
dark=(100,255,100)
grey=(0,0,0,150)
red=(255,0,0)