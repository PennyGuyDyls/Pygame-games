import pygame
from Scripts.config import cell_width,font,black,grey,yellow,green
from Scripts.button import button

pygame.init()
screen=pygame.display.set_mode((14.4*cell_width,13*cell_width))


class letter():
    def __init__(self,letter,x,y,cell_width):
        self.letter=letter
        self.w=cell_width
        sca=self.w/100
        self.x=sca*x
        self.y=sca*y
        self.rect=self.x,self.y,self.w,self.w
        self.colour=grey


        colours=[black,grey,yellow,green]
        hover_colours=[black,grey,yellow,green]
        self.buttons=[button(
            cell_width,
            x+i*25,
            y+110,
            20,
            20,
            None,
            colours[i],
            hover_colours[i])
            for i in range(4)]
        
        self.text=font.render(letter,True,(255,255,255))

        self.pos_choice=False
        self.poses=[button(
            cell_width,
            x,
            y+150+i*30,
            100,
            20,
            str(i+1),
            black,
            black)
            for i in range(5)]
        for i in self.poses:
            i.font=pygame.font.SysFont(None, round(self.w/100*30))

    def draw(self):
        pygame.draw.rect(screen,self.colour,self.rect)
        screen.blit(self.text,(self.x+self.w//2-self.text.get_width()//2,self.y+self.w//2-self.text.get_height()//2))
        for i in self.buttons:
            i.draw(screen)
        if self.pos_choice:
            for i in self.poses:
                i.draw(screen)

    def update(self,mx,my):
        
        for i in self.buttons:
            if i.clicked(mx,my):
                self.colour=i.colour
        if self.colour==green or self.colour==yellow:
            self.pos_choice=True
        else:
            self.pos_choice=False
            for i in self.poses:
                i.current_colour=black

        if self.pos_choice:
            for i,pos in enumerate(self.poses):
                if pos.clicked(mx,my):
                    if pos.current_colour==self.colour:
                        self.poses[i].current_colour=black
                    else:
                        self.poses[i].current_colour=self.colour

def init_letters(collists):
    lettervals='abcdefghijklmnopqrstuvwxyz'.upper()
    letters=[letter(
        lettervals[i*13+j],
        j*110+10,
        i*300+10,
        cell_width)
        for j in range(13)
        for i in range(2)]
    
    for i in collists[0]:
        for j in letters:
            if j.letter==i[0]:
                j.colour=green
                j.pos_choice=True
                j.poses[i[1]-1].current_colour=green
    for i in collists[1]:
        for j in letters:
            if j.letter==i[0]:
                j.colour=yellow
                j.pos_choice=True
                j.poses[i[1]-1].current_colour=yellow
    for j in letters:
        if j.letter in collists[2]:
            j.colour=black
    return letters
    
def draw_letters(letters):
    for i in letters:
        i.draw()

def update_letters(letters,mx,my):
    for i in letters:
        i.update(mx,my)

def get_inputs(collists,possible):
    if len(possible)<100:
        show_poss=True
        possible=list(possible)
        possible.sort()
    else:
        show_poss=False
    
    pygame.display.flip()
    letters=init_letters(collists)
    submit=button(
        cell_width,
        1440//2-350,700,300,70,
        'SUBMIT',
        (0,200,0),
        green
    )
    reset=button(
        cell_width,
        1440//2+50,700,300,70,
        'RESET',
        (200,0,0),
        (255,0,0)
    )

    running=True
    while running:
        screen.fill((0,0,0))
        pygame.draw.line(screen,(255,255,255),(0,8*cell_width),(screen.get_width(),8*cell_width),3)
        if show_poss:
            for place,i in enumerate(possible):
                text=font.render(i, True, (255,255,255))
                screen.blit(text,((place%5)*150,8*cell_width+(place//5)*60*1.1+10))

        draw_letters(letters)
        submit.draw(screen)
        reset.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return False,(None,None,None)
            
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mx,my=pygame.mouse.get_pos()
                update_letters(letters,mx,my)
                if submit.clicked(mx,my):
                    return True,calc_inputs(letters)
                if reset.clicked(mx,my):
                    return True,([],[],[])
                
def calc_inputs(letters):
    greens=[]
    yellows=[]
    blacks=[]
    for i in letters:
        if i.colour==green:
            for pos,j in enumerate(i.poses):
                if j.current_colour==green:
                    greens.append([i.letter,pos+1])
        
        elif i.colour==yellow:
            for pos,j in enumerate(i.poses):
                if j.current_colour==yellow:
                    yellows.append([i.letter,pos+1])

        elif i.colour==black:
            blacks.append(i.letter)

    return greens,yellows,blacks

