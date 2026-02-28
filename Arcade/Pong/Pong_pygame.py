import pygame

def run():
    class Paddle1(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.Surface((8,200))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect()
            self.rect.center = (100, 500)

        def update(self,d):
            if 100<self.rect.centery+d<900:
                self.rect.centery+=d

    class Paddle2(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.Surface((8,200))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect()
            self.rect.center = (1400, 500)

        def update(self,d):
            if 100<self.rect.centery+d<900:
                self.rect.centery+=d

    class Ball(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.Surface((50,50),pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 255, 255), (25,25), 25)
            self.rect = self.image.get_rect()
            self.rect.center = (750,500)

        def update(self,ang,speed):
            
            self.rect.centerx+=speed
            self.rect.centery+=ang




    pygame.init()
    screen=pygame.display.set_mode((1500,1000))
    clock=pygame.time.Clock()
    font=pygame.font.SysFont(None, 100)

    padSpr1=Paddle1()
    padSpr2=Paddle2()
    ballspr=Ball()

    direction1,direction2 = 0,0
    angle=0
    speed=-10

    running=True
    score=[0,0]
    while 2 not in score and running:
        clock.tick(30)

        if 0>ballspr.rect.centerx:
            score[1]+=1
            pygame.draw.line(screen, (255,0,0),(0,0),(0,1000),10)
            pygame.display.flip()
            pygame.time.wait(1000)
            ballspr.rect.center=(750,500)
            padSpr1.rect.centery=500
            padSpr2.rect.centery=500
            angle=0
            speed=-10
        elif ballspr.rect.centerx>1500:
            score[0]+=1
            pygame.draw.line(screen, (255,0,0),(0,0),(0,1000),10)
            pygame.display.flip()
            pygame.time.wait(1000)
            ballspr.rect.center=(750,500)
            padSpr1.rect.centery=500
            padSpr2.rect.centery=500
            angle=0
            speed=-10
        text= font.render((f'{score[0]}:{score[1]}'),True,(255,255,255))

        screen.fill((0,0,0))
        
        screen.blit(text,(700,30))
        padSpr1.update(direction1*-10)
        screen.blit(padSpr1.image,padSpr1.rect)
        padSpr2.update(direction2*-10)
        screen.blit(padSpr2.image,padSpr2.rect)

        if 25>ballspr.rect.centery:
            angle*=-1
        elif ballspr.rect.centery>975:
            angle*=-1

        ballspr.update(angle,speed)
        screen.blit(ballspr.image,ballspr.rect)
        pygame.display.flip()

        for event in pygame.event.get():

            if event.type==pygame.QUIT:
                running=False

            elif event.type==pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    direction1=1
                elif event.key == pygame.K_s:
                    direction1=-1
                elif event.key == pygame.K_UP:
                    direction2=1
                elif event.key == pygame.K_DOWN:
                    direction2=-1

            elif event.type==pygame.KEYUP:
                if event.key in (pygame.K_w,pygame.K_s):
                    direction1=0
                elif event.key in (pygame.K_UP,pygame.K_DOWN):
                    direction2=0

        if pygame.sprite.collide_rect(ballspr,padSpr1) or pygame.sprite.collide_rect(ballspr,padSpr2):
            if speed>0:
                speed+=1
            else:
                speed-=1
            speed*=-1
            if pygame.sprite.collide_rect(ballspr,padSpr1):
                angle=(ballspr.rect.centery - padSpr1.rect.centery)//11
            elif pygame.sprite.collide_rect(ballspr,padSpr2):
                angle=(ballspr.rect.centery - padSpr2.rect.centery)//11

            
            
            
run() 