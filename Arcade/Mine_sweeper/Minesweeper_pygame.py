from random import randint as ran
import pygame

# NOTES:
# Minesweeper game!
# l = length of board
# h = width of board
# d = density of mines
# x = x axis
# y = y axis
# z = variable always True/False
# vis = board player sees
# board = pre-generated board before game start
# i = first priority for loop variable
# j = second priority for loop variable
# k = third priority for loop variable

def run():
  w=(255,255,255)
  g=(0,255,0)
  numcolours=[(200,200,200),(0,0,255),(0,128,0),(255,0,0),(0,0,128),(128,0,0),(0,128,128),(0,0,0),(128,128,128)]

  class game():
    def __init__(self,x,y,density):
      self.width=x
      self.height=y
      self.mines=x*y*density//100
      self.board=[[' ' for j in range(self.width)] for i in range(self.height)]
      self.vis=[[w for j in range(self.width)] for i in range(self.height)]
      self.lives=3


    def create_board(self):
      indexes=[[i,j] for i in range(self.width) for j in range(self.height)]

      while self.mines>0:
        a=indexes[ran(0,len(indexes)-1)]
        self.board[a[0]][a[1]]=-1
        self.mines-=1
        indexes.remove(a)

    def place_numbers(self):
      for i in range(self.height):
        for j in range(self.width):
          if self.board[i][j]==-1:
            pass
          else:
            num=0
            for k in range(-1,2):
              for l in range(-1,2):
                if 0<=i+k<self.height and 0<=j+l<self.width:
                  if self.board[i+k][j+l]==-1:
                    num+=1
            self.board[i][j]=num

    def genvis(self):
      for i in range(9):
        indexes=[[k,j] for j in range(self.width) for k in range(self.height) if self.board[k][j]==i]
        
        if indexes != []:
          break

      if indexes != []:
        a=indexes[ran(0,len(indexes)-1)]
        self.vis[a[0]][a[1]]=g

    def reveal(self,mode,x,y):
      z=1
      if mode == 'r':
        if self.vis[y][x] == w or self.vis[y][x] == g:
          self.vis[y][x]=self.board[y][x]

          if self.vis[y][x]==0: # flood fill
            check=[]
            while True:
              if self.vis==check:
                break
              
              check=[]
              for i in self.vis:
                check.append(i.copy())

              screen.fill((0,0,0))
              show()
              pygame.display.flip()
              clock.tick(20)
              z=0
              for y1 in range(self.height):
                for x1 in range(self.width):
                  if check[y1][x1]==0:
                    for i in range(-1,2):
                      for j in range(-1,2):
                        a=y1+j
                        b=x1+i
                        if 0<=b<self.width and 0<=a<self.height:
                          self.vis[a][b]=self.board[a][b]
                          
          elif self.vis[y][x]==-1:
            self.vis[y][x]=-2
            self.board[y][x]=-2
            self.lives-=1

      else:
        if self.vis[y][x]==w:
          self.vis[y][x]='f'
        elif self.vis[y][x]=='f':
          self.vis[y][x]=w

    def check(self):
      z=0
      for i in range(self.height):
        for j in range(self.width):
          if self.board[i][j]==-1:
            pass
          else:
            if self.board[i][j]!=self.vis[i][j]:
              z=1
              break
        if z:
          break
      if z==0:
        return [False,True]
      if self.lives>0:
        return [True]
      else:
        return [False,False]

  def time(set):
    mins=int((pygame.time.get_ticks()-set)/60000)
    if mins<10:
      mins='0'+str(mins)
    secs=int(((pygame.time.get_ticks()-set)/1000)%60)
    if secs<10:
      secs='0'+str(secs)
    return font.render(f'{mins}:{secs}', True, (w))

  def show():

    screen.blit(time(level_st), (minesweeper.width*40-100,10))

    for i in range(minesweeper.lives):
      screen.blit(heart_r, (i*60+10,3))
    for i in range(3-minesweeper.lives):
      screen.blit(heart_g, ((i+minesweeper.lives)*60+10,3))
    for i in range(minesweeper.height):
      for j in range(minesweeper.width):

        if minesweeper.vis[i][j] == -1 or minesweeper.vis[i][j] == -2:
          pygame.draw.rect(screen, (200,200,200), (j*40+10,i*40+50,39,39))
          screen.blit(explosion, (j*40,i*40+38))
        
        elif str(minesweeper.vis[i][j]) in "012345678":
          pygame.draw.rect(screen, (200,200,200), (j*40+10,i*40+50,39,39))
          text=font.render(str(minesweeper.vis[i][j]), True, (numcolours[minesweeper.vis[i][j]]))
          screen.blit(text, (j*40+20,i*40+55))
        elif minesweeper.vis[i][j]=='f':
          pygame.draw.rect(screen, (w), (j*40+10,i*40+50,39,39))
          screen.blit(flag, (j*40+10,i*40+50))
        else:
          pygame.draw.rect(screen, minesweeper.vis[i][j], (j*40+10,i*40+50,39,39))
      
  pygame.init()

  total_time=0
  font = pygame.font.SysFont(None, 48)
  clock = pygame.time.Clock()
  exit=False

  for i in range(3):
    try:
      pygame.event.clear(pygame.MOUSEBUTTONDOWN)
      total_time+=int((pygame.time.get_ticks()-level_st)//1000)
    except:pass
    if i == 0:
      l=10
      h=10
      d=11
    elif i == 1:
      l=15
      h=11
      d=15
    else:
      l=20
      h=20
      d=20

    screen = pygame.display.set_mode((l*40+20,h*40+60))

    screen.fill((0,0,0))
    text=font.render(f'Level {i+1}', True, (255,255,255))
    screen.blit(text, (l*20+10-text.get_width()//2,h*20+30-text.get_height()//2))
    pygame.display.flip()
    pygame.time.wait(3000)

    IMG_DIR='Arcade/Mine_sweeper/Images/'
    flag = pygame.image.load(IMG_DIR+"flag.png").convert_alpha()
    flag = pygame.transform.scale(flag, (40,40))
    explosion = pygame.image.load(IMG_DIR+"explosion.png").convert_alpha()
    explosion = pygame.transform.scale(explosion, (60,60))
    heart_r= pygame.image.load(IMG_DIR+"heart_r.png").convert_alpha()
    heart_r = pygame.transform.scale(heart_r, (43,43))
    heart_g= pygame.image.load(IMG_DIR+"heart_g.png").convert_alpha()
    heart_g = pygame.transform.scale(heart_g, (43,43))

    minesweeper=game(l,h,d)

    minesweeper.create_board()
    minesweeper.place_numbers()
    minesweeper.genvis()
    c=minesweeper.check()

    level_st=pygame.time.get_ticks()

    
    while c[0]:
      screen.fill((0,0,0))
      show()
      pygame.display.flip()
      z=1
      for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
          c=[False,False]
          exit=True

        if event.type == pygame.MOUSEBUTTONDOWN:
          mx,my=pygame.mouse.get_pos()
          col=(mx-10)//40
          row=(my-50)//40
          if 0<=col<l and 0<=row<h:
            if event.button == 1:
              m='r'
            else:
              m='f'
            minesweeper.reveal(m,col,row)
            c=minesweeper.check()
    if not c[1]:
      break

  if not exit:
    screen.fill((0,0,0))
    show()
    pygame.display.flip()
    pygame.time.wait(1000)

    total_time+=int((pygame.time.get_ticks()-level_st)//1000)-1

    screen.fill((0,0,0))

    if c[1]: 
      text=font.render(f'Victory!', True, (0,255,0))
    else:
      text=font.render(f'Defeat!', True, (255,0,0))

    screen.blit(text, (l*20+10-text.get_width()//2,h*20+30-text.get_height()//2))
    pygame.display.flip()
    pygame.time.wait(2000)

    font = pygame.font.SysFont(None, 30)
    text=font.render(f'In {total_time//60} minutes {int(total_time%60)} seconds', True, (255,255,255))
    screen.blit(text, (l*20+10-text.get_width()//2,h*20+text.get_height()//2+80))
    pygame.display.flip()
    pygame.time.wait(3000)

run()