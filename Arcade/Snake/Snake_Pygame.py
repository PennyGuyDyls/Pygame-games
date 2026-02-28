import pygame
from random import randint

def run():
    class game():
        def __init__(self,x,y):
            self.width=x
            self.height=y
            self.board=[[0 for i in range(x)] for j in range(y)]
            self.snake=[[5,i] for i in range(1,4)]

        def place_apple(self):
            indexes=[[i,j] for i in range(self.height) for j in range(self.width) if self.board[i][j]==0]
            if indexes != []:
                a=indexes[randint(0,len(indexes)-1)]
                self.board[a[0]][a[1]]=1

        def move(self, direction):
            head=self.snake[-1]
            new_head=[head[0]+direction[0], head[1]+direction[1]]

            if new_head == self.snake[-2]:
                direction=(-direction[0], -direction[1])
                new_head=[head[0]+direction[0], head[1]+direction[1]]

            if new_head == self.snake[0]:
                self.snake.append(new_head)
                self.snake.pop(0)
                return True
            
            if 0<=new_head[0]<self.height and 0<=new_head[1]<self.width and self.board[new_head[0]][new_head[1]]!=2:
                self.snake.append(new_head)
                if self.board[new_head[0]][new_head[1]]==1:
                    self.board[self.snake[0][0]][self.snake[0][1]]=0
                    self.place_apple()
                else:
                    self.board[self.snake[0][0]][self.snake[0][1]]=0
                    self.snake.pop(0)
                for i in self.snake:
                    self.board[i[0]][i[1]]=2
                return True
            return False

    def show(snake,cw,ch):
        screen.fill((0,0,0))
        colour=(150,255,150)
        swap=True
        for i in range(snake.height):
            if len(snake.board[i]) % 2 == 0:
                swap=False
            for j in range(snake.width):
                if swap:
                    if colour==(150,255,150):
                        colour=(100,255,100)
                    else:
                        colour=(150,255,150)
                swap=True
                
                pygame.draw.rect(screen,colour,(j*cw,i*ch,cw,ch))

                if snake.board[i][j]==1:
                    screen.blit(apple,((j+0.1)*cw,(i+0.1)*ch))

                if snake.board[i][j]==2:
                    pygame.draw.rect(screen,(255,0,0),((j+0.1)*cw,(i+0.1)*ch,cw*0.8,ch*0.8))
                    for k in range(1,len(snake.snake)):
                        if snake.snake[k][0]>snake.snake[k-1][0]:
                            pygame.draw.rect(screen,(255,0,0),((snake.snake[k][1]+0.1)*cw,(snake.snake[k][0]-0.3)*ch,cw*0.8,ch))
                        elif snake.snake[k][0]<snake.snake[k-1][0]:
                            pygame.draw.rect(screen,(255,0,0),((snake.snake[k][1]+0.1)*cw,(snake.snake[k][0]+0.3)*ch,cw*0.8,ch))
                        elif snake.snake[k][1]>snake.snake[k-1][1]:
                            pygame.draw.rect(screen,(255,0,0),((snake.snake[k][1]-0.3)*cw,(snake.snake[k][0]+0.1)*ch,cw,ch*0.8))
                        else:
                            pygame.draw.rect(screen,(255,0,0),((snake.snake[k][1]+0.3)*cw,(snake.snake[k][0]+0.1)*ch,cw,ch*0.8))

    width=10
    height=10
    cell_w=100
    cell_h=100
    pygame.init()

    screen=pygame.display.set_mode((width*cell_w,height*cell_h))

    IMG_DIR='Arcade/Snake/Images/'
    apple=pygame.image.load(IMG_DIR+'apple.png').convert_alpha()
    apple=pygame.transform.scale(apple,(cell_w*0.8,cell_h*0.8))
    clock=pygame.time.Clock()

    lost=True
    running=True
    while running:
        clock.tick(7)

        if lost:

            direction=(0,1)
            start=True
            font=pygame.font.SysFont(None, 100)

            snake=game(width,height)
            snake.place_apple()

            for i in range(3,0,-1):
                screen.fill((0,0,0))
                text = font.render(f"Starting in {i}", True, (255,255,255))
                screen.blit(text, (width*cell_w//2-text.get_width()//2,height*cell_h//2-text.get_height()//2))
                pygame.display.flip()
                pygame.time.wait(1000)

            lost=False

        
        
        for event in pygame.event.get():

            if event.type==pygame.QUIT:
                running=False
            
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RIGHT:
                    direction=(0,1)
                elif event.key==pygame.K_LEFT:
                    direction=(0,-1)
                elif event.key==pygame.K_UP:
                    direction=(-1,0)
                elif event.key==pygame.K_DOWN:
                    direction=(1,0)

        running=snake.move(direction)
        if running:
            show(snake,cell_w,cell_h)
            pygame.display.flip()
        else:
            lost=True
            screen.fill((0,0,0))
            text = font.render("Game Over", True, (255,0,0))
            screen.blit(text, (width*cell_w//2-text.get_width()//2,height*cell_h//2-text.get_height()//2))
            pygame.display.flip()
            pygame.time.wait(2000)
            font=pygame.font.SysFont(None, 40)
            pygame.draw.rect(screen,(0,255,0),(width*cell_w//4-150,height*cell_h//4*3-50,300,100))
            text = font.render("Play Again", True, (0,0,0))
            screen.blit(text, (width*cell_w//4-text.get_width()//2,height*cell_h//4*3-text.get_height()//2))
            pygame.draw.rect(screen,(255,0,0),(width*cell_w//4*3-150,height*cell_h//4*3-50,300,100))
            text = font.render("Exit", True, (0,0,0))
            screen.blit(text, (width*cell_w//4*3-text.get_width()//2,height*cell_h//4*3-text.get_height()//2))
            pygame.display.flip()
            waiting=True
            while waiting:
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        waiting=False
                        running=False

                    elif event.type==pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        if width*cell_w//4-150<=mx<=width*cell_w//4+150 and height*cell_h//4*3-50<=my<=height*cell_h//4*3+50:
                            running=True
                            waiting=False
                        elif width*cell_w//4*3-150<=mx<=width*cell_w//4*3+150 and height*cell_h//4*3-50<=my<=height*cell_h//4*3+50:
                            running=False
                            waiting=False