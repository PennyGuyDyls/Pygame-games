import pygame

def run():
  w=(30,30,30)
  r=(255,20,20)
  b=(0,150,255)

  class game():
    def __init__(self):
      self.board = [[w for i in range(7)] for j in range(6)]
      self.turn = b

    def turn_swap(self):
      if self.turn==r:
        self.turn=b
      else:
        self.turn=r

    def move(self,column):
      full=True
      if 0<=column<=6:
        pycol=(column+1)*120
        count=7
        for i in reversed(self.board):
          count-=1
          if i[column] == w:
            pyrow=(count)*120
            i[column]=self.turn
            full=False
            break

      if full:
        return None
      else:
        return pyrow,pycol

    def check_win(self):

      def check_h():
        x=0
        y=0
        ry=0
        for i in self.board:
          rx=0
          ry+=1
          x=0
          y=0
          for j in i:
            rx+=1
            if j==r:
              y=0
              x+=1
            elif j==b:
              x=0
              y+=1
            else:
              x=0
              y=0
            if x==4:
              return [True,'Red',r,rx,ry]
            elif y==4:
              return [True,'Blue',b,rx,ry]
        return [False]
      
      def check_v():
        for i in range(7):
          x=0
          y=0
          ry=0
          for j in self.board:
            ry+=1
            if j[i]==r:
              y=0
              x+=1
            elif j[i]==b:
              x=0
              y+=1
            else:
              x=0
              y=0
            if x==4:
              return [True,'Red',r,i+1,ry]
            elif y==4:
              return [True,'Blue',b,i+1,ry]
        return [False]
      
      def check_dr():
        x=0
        y=0
        z=0
        for i in range(-7,7):
          x=0
          y=0
          for j in range(6):
            if 0<=j+i<=6:
              if self.board[j][j+i] == r:
                x+=1
                y=0
              elif self.board[j][j+i] == b:
                x=0
                y+=1
              else:
                x=0
                y=0
              if x==4:
                return [True,'Red',r,j+i+1,j+1]
              elif y==4:
                return [True,'Blue',b,j+i+1,j+1]
        return [False]
      
      def check_dl():
        x=0
        y=0
        z=0
        for i in range(-7,7):
          x=0
          y=0
          for j in range(6):
            if 0<=7-i-j<=6:
              if self.board[j][7-i-j] == r:
                x+=1
                y=0
              elif self.board[j][7-i-j] == b:
                x=0
                y+=1
              else:
                x=0
                y=0
              if x==4:
                return [True,'Red',r,8-i-j,j-1]
              elif y==4:
                return [True,'Blue',b,8-i-j,j-1]
        return [False]
      
      h=check_h()
      v=check_v()
      dr=check_dr()
      dl=check_dl()

      if h[0]:
        h.append([-460,0])
        return h
      elif v[0]:
        v.append([0,-460])
        return v
      elif dr[0]:
        dr.append([-460,-460])
        return dr
      elif dl[0]:
        dl.append([460,-460])
        return dl
      else:
        return [False]

      


  def display():
    for i in range(8):
        pygame.draw.rect(screen, (220,220,220), (i*120+58, 40, 4, 750))
    for i in range(1,8):
        for j in range(1,7):
          pygame.draw.circle(screen, connect4.board[j-1][i-1], (i*120, j*120),40)

  def hover(column,colour):
    if 1<=column<=7:
      pycol=(column)*120
      screen.fill((0,0,0))
      display()
      pygame.draw.circle(screen, colour, (pycol, 1),40)
      pygame.display.flip()







  pygame.init()

  screen = pygame.display.set_mode((975,850))
  font = pygame.font.SysFont(None, 48)
  clock = pygame.time.Clock()
  connect4 = game()
  win = [False]

  running = True
  while running and not win[0]:
    clock.tick(500)
    win = connect4.check_win()
    display()
    pygame.display.flip()
    for event in pygame.event.get():
            
      if event.type == pygame.QUIT:
        running=0
        break
            
      if event.type == pygame.MOUSEBUTTONDOWN:         
        mx, my = pygame.mouse.get_pos()
        row,col= connect4.move((mx+60)//120-1)
        if row != None:
          for i in range(row+1):
            screen.fill((0,0,0))
            display()
            pygame.draw.circle(screen, w, (col, row),40)
            pygame.draw.circle(screen, connect4.turn, (col, i),40)
            pygame.display.flip()
            
          connect4.turn_swap()
          pygame.event.clear(pygame.MOUSEBUTTONDOWN)

      if event.type == pygame.MOUSEMOTION:
        mx, my = pygame.mouse.get_pos()
        hover((mx+60)//120,connect4.turn)

  if running:
    text= font.render((win[1]+" wins!"), True, win[2])
    screen.blit(text, (400, 400))
    startx,starty=(win[3]*120-50, win[4]*120)
    endx,endy=startx + win[5][0], starty + win[5][1]
    pygame.draw.line(screen, win[2], (startx, starty), (endx, endy), 10)
    
    pygame.display.flip()
    pygame.time.wait(5000)

            


