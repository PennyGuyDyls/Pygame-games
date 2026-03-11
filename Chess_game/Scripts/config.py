import pygame

Cell_width=100

screen=pygame.display.set_mode((Cell_width*8,Cell_width*8))

pygame.mixer.init()

IMG_DIR='Chess_game/Images/'
pieces_orig=[[pygame.image.load(f'{IMG_DIR}Piece{i}.{j}.png') for i in range(1,7)] for j in range(1,5)]
pieces_scaled=[[pygame.transform.scale(j,(80*Cell_width/100,85*Cell_width/100)) for j in i] for i in pieces_orig]
for i in range(2):
    pieces_scaled[i][0]=pygame.transform.scale(pieces_orig[i][0],(60*Cell_width/100,70*Cell_width/100))
    pieces_scaled[i][3]=pygame.transform.scale(pieces_orig[i][3],(70*Cell_width/100,80*Cell_width/100))
    pieces_scaled[i+2][0]=pygame.transform.scale(pieces_orig[i+2][0],(60*Cell_width/100,70*Cell_width/100))
    pieces_scaled[i+2][3]=pygame.transform.scale(pieces_orig[i+2][3],(65*Cell_width/100,70*Cell_width/100))

pieces=pieces_scaled[0:2]

SFX_DIR='Chess_game/Sounds/'
move_sound = pygame.mixer.Sound(SFX_DIR+'Move.wav')
move_sound.set_volume(0.4)
capture_sound = pygame.mixer.Sound(SFX_DIR + 'Capture.wav')
capture_sound.set_volume(0.8)

themes=[
    ((150,255,150),(100,255,100)),     #green
    ((240,217,181), (181,136,99)),     #wood
    ((200,200,200), (120,120,120)),    #grey
    ((180,220,255), (100,150,200)),    #ice blue
    ((255,180,180), (200,60,60)),      #lava
    ((170,200,150), (90,120,80)),      #camo
    ((210,180,230), (140,100,170)),    #purple
    ((80,80,80), (40,40,40)),          #dust
    ((230,245,255), (80,200,220))      #cyan
]
current_theme=0




grey=(0,0,0,150)
red=(255,0,0)

