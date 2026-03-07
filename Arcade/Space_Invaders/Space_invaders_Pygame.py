import pygame
from random import randint as r

def run():
    class cannon(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = cannon1
            self.rect = self.image.get_rect()
            self.rect.center = (100,screen.get_height()-200)
            self.state = 'LOADED'
            self.score = 0
            self.lives = 3

        def move(self,direction):
            if self.rect.centerx-self.rect.width+direction//2>=0 and self.rect.centerx+self.rect.width+direction<=screen.get_width():
                self.rect.centerx+=direction

        def shoot(self):
            shoot_sound.play()
            self.state = 'EMPTY'
            self.image = cannon2

        def reload(self):
            self.image = cannon1
            self.state = 'LOADED'

    class shot(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.Surface((3,20))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect()
            self.rect.center = (0,0)
            self.state = 'LOADED'

        def shoot(self):
            self.rect.centery-=5
            self.state = 'FIRING'

        def follow(self, player):
            self.rect.center = (player.rect.centerx,player.rect.centery)

        def reload(self):
            self.state = 'LOADED'

    class alien(pygame.sprite.Sprite):
        def __init__(self,x,y,img1,img2,score):
            super().__init__()
            self.img1 = img1
            self.img2 = img2
            self.score = score
            self.volume=score/100*2

            self.image = img1
            self.rect = self.image.get_rect()
            self.rect.center = (x*60+200,y) # leaving these for now
            
            self.state='ALIVE'
            self.bullets=0

            self.animstage=-1
            self.deathstage=0
            
            self.shotprob=500
            self.shotdelay=100
            self.lastshot=pygame.time.get_ticks()

        def update(self,function):
            if function=='animate':
                self.animate()
            elif function=='try_shoot':
                self.try_shoot()
            elif function=='die':
                self.die()

        def img_swap(self, img):
            self.image = img
            cen=self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center=cen

        def animate(self):
            if self.state=='ALIVE':
                self.animstage*=-1
                if self.animstage == -1:
                    self.img_swap(self.img1)
                else:
                    self.img_swap(self.img2)

        def try_shoot(self):
            if self.state == 'ALIVE' and self.bullets<3 and  pygame.time.get_ticks()-self.lastshot>self.shotdelay and r(1,self.shotprob)==1:
                self.lastshot=pygame.time.get_ticks()
                return True
            self.lastshot=pygame.time.get_ticks()
            return False
        
        def decrease_shotprob(self, amount):
            self.shotprob=max(100,self.shotprob-amount)

        def die(self):
            if self.deathstage==len(alsplode_anim)-1:
                self.image=pygame.Surface((100,100),pygame.SRCALPHA)
                self.state='DEAD'
            else:
                if self.state == 'ALIVE':
                    alien_die_sound.set_volume(self.volume)
                    alien_die_sound.play()
                    self.state = 'DYING'
                    player.score += self.score
                    self.img_swap(alsplode_anim[self.deathstage])
                elif self.state=='DYING':
                    self.deathstage+=1
                    self.img_swap(alsplode_anim[self.deathstage])
                        
    class alshot(pygame.sprite.Sprite):
        def __init__(self,alien):
            super().__init__()
            self.image = pygame.Surface((3,20))
            self.image.fill((255, 255, 255))
            self.rect = self.image.get_rect()
            self.owner = alien
            self.rect.center = self.owner.rect.center
            self.owner.bullets+=1

        def shoot(self):
            self.rect.centery+=3

    def menu():
        def show_pair(points,img,y):
            text=font.render('= '+str(points).upper()+' POINTS',True,(255,255,0))
            screen.blit(img,(screen.get_width()//2-img.get_width()-text.get_width()//2-10,y))
            screen.blit(text,(screen.get_width()//2-text.get_width()//2+10,y+10))
            pygame.display.flip()

        font=pygame.font.SysFont(None, 100)
        text=font.render('SPACE INVADERS',True,(255,255,0))
        screen.blit(text,(screen.get_width()//2-text.get_width()//2,100))
        pygame.display.flip()
        pygame.time.wait(1000)

        font=pygame.font.SysFont(None, 30)
        show_pair(100,alimages[0][0],240)
        pygame.time.wait(500)
        show_pair(200,alimages[1][0],340)
        pygame.time.wait(500)
        show_pair(500,alimages[2][0],440)
        pygame.time.wait(1000)

        stcolour=(0,200,0)
        excolour=(200,0,0)
        font=pygame.font.SysFont(None, 100)
        sttext=font.render('START',True,(255,255,255))
        extext=font.render('EXIT',True,(255,255,255))
        while True:

            pygame.draw.rect(screen, stcolour, (400,600, 300,200))
            screen.blit(sttext,(screen.get_width()//2-sttext.get_width()//2-200,700-sttext.get_height()//2))

            pygame.draw.rect(screen, excolour, (800,600, 300,200))
            screen.blit(extext,(screen.get_width()//2-extext.get_width()//2+200,700-extext.get_height()//2))
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if 600<=my<=800:
                        if 400<=mx<=700:
                            return True
                        elif 800<=mx<=1100:
                            return False
                elif event.type == pygame.MOUSEMOTION:
                    mx, my = pygame.mouse.get_pos()
                    if 600<=my<=800:
                        if 400<=mx<=700:
                            stcolour=(0,255,0)
                        else:
                            stcolour=(0,200,0)
                        if 800<=mx<=1100:
                            excolour=(255,0,0)
                        else:
                            excolour=(200,0,0)
                    else:
                        stcolour=(0,200,0)
                        excolour=(200,0,0)

    def initiate_aliens(gap_distance,starty):
        scores=[10,10,20,20,50]
        alientypes=[0,0,1,1,2]
        aliens=[[alien(i,gap_distance*(5-j)+starty,alimages[alientypes[j]][0],alimages[alientypes[j]][1],scores[j]) for i in range(row_number)] for j in reversed(range(5))]
        all_aliens = pygame.sprite.Group()
        for i in aliens:
            for j in i:
                all_aliens.add(j)
        return aliens[0],aliens,starty,all_aliens

    def show(all_aliens,player,bullet,albullets):
        all_aliens.draw(screen)
        for i in albullets:
            screen.blit(i.image,i.rect)
        screen.blit(player.image,player.rect)
        screen.blit(bullet.image,bullet.rect)
        text=font.render('Score:'+str(player.score),True,(255,255,0))
        screen.blit(text,(5,5))
        text=font.render('Lives:'+str(player.lives),True,(255,255,0))
        screen.blit(text,(screen.get_width()-text.get_width()-5,5))

    def check(aliens):
        for i in reversed(aliens):
            for j in range(len(i)):
                if i[j].state=='ALIVE' and i[j].rect.centery>=player.rect.centery-50:
                    return False
        if player.lives <= 0:
            return False
        return True

    def round_change(aliens,round):
        for i in aliens:
            for j in i:
                if j.state=='ALIVE':
                    return round,False
        return round + 1,True

    def alien_respawn(starty,dy):
        starty+=dy/2
        return initiate_aliens(dy,starty)

    pygame.init()
    pygame.mixer.init()
    screen=pygame.display.set_mode((1500,1000))
    clock=pygame.time.Clock()
    font=pygame.font.SysFont(None, 100)

    IMG_DIR='Arcade/Space_Invaders/Images/'
    alimages = [[pygame.image.load(f"{IMG_DIR}Alien {i} state {j}.png").convert_alpha() for j in range(1,3)] for i in range(1,4)]
    scalefactors= [[(40,40),(33,40)],[(30,50),(40,50)],[(40,50),(40,50)]]
    for i in range(len(alimages)):
        for j in range(len(alimages[i])):
            alimages[i][j] = pygame.transform.scale(alimages[i][j], scalefactors[i][j])

    alsplode_imgs = [pygame.image.load(f'{IMG_DIR}alsplode-{i}.png') for i in range(1,6)]
    alsplode_anim = [pygame.transform.scale(i, (50,50)) for i in alsplode_imgs]


    cannon1 = pygame.image.load(IMG_DIR+"Cannon_loaded.png").convert_alpha()
    cannon1 = pygame.transform.scale(cannon1, (90,45))
    cannon2 = pygame.image.load(IMG_DIR+"Cannon_empty.png").convert_alpha()
    cannon2 = pygame.transform.scale(cannon2, (90,45))

    SFX_DIR='Arcade/Space_Invaders/Sounds/'
    alien_die_sound = pygame.mixer.Sound(SFX_DIR+'Alien_death.wav')
    shoot_sound = pygame.mixer.Sound(SFX_DIR + 'Cannon_shot.wav')


    player=cannon()
    direction=0

    bullet=shot()

    row_number=11
    gap_distance=50
    starty=200
    aliens1,aliens,starty,all_aliens=initiate_aliens(gap_distance,starty)

    round=0
    aldirection=(40,0)
    down=False

    albullets=[]

    deathanim=0
    anifreq=1400
    movfreq=2500
    animtime=pygame.time.get_ticks()
    movtime=pygame.time.get_ticks()

    running=menu()
    while running and check(aliens):
        round,changed=round_change(aliens,round)
        if changed:
            aliens1,aliens,starty,all_aliens=alien_respawn(starty,gap_distance)
            player.lives+=1
            down=False
            aldirection=(40,0)
            anifreq=max(200,1400-round*200)
            movfreq=max(300,2500-round*300)
            for i in aliens:
                for j in i:
                    j.shotprob=max(50,500*len(aliens[2:])*len(aliens1)-round*1000)
        clock.tick(100)

        for i in aliens:
            for j in i:
                if j.state=='DYING' and pygame.time.get_ticks()-deathanim>75:
                    j.die()
                    deathanim=pygame.time.get_ticks()

        if pygame.time.get_ticks()-animtime>=anifreq:
            all_aliens.update('animate')
            animtime=pygame.time.get_ticks()

        if pygame.time.get_ticks()-movtime>=movfreq:
            left=aliens1[0].rect.centerx
            right=aliens1[-1].rect.centerx
            if down:
                down=False
                if left < 200:
                    aldirection = (40,0)
                elif right > screen.get_width()-200:
                    aldirection = (-40,0)
            else:
                if left<60 or right>screen.get_width()-60:
                    aldirection = (0,gap_distance)
                    movfreq=max(300,movfreq-100)
                    anifreq=max(200,anifreq-70)
                    for i in aliens:
                        for j in i:
                            j.decrease_shotprob(30)
                    down=True

            for i in aliens:
                for j in range(len(i)):
                    i[j].rect.centerx+=aldirection[0]
                    i[j].rect.centery+=aldirection[1]
            movtime=pygame.time.get_ticks()

        for i in aliens[:-2]:
            for j in i:
                if j.try_shoot():
                    albullets.append(alshot(j))

        player.move(direction)
        if player.state == 'LOADED':
            bullet.follow(player)
        else:      
            bullet.shoot()

        for i in albullets:
            i.shoot()

        for i in range(len(aliens)):
            for j in range(len(aliens1)):
                if bullet.rect.colliderect(aliens[i][j].rect) and aliens[i][j].state == 'ALIVE':
                    deathanim=pygame.time.get_ticks()
                    aliens[i][j].die()
                    player.reload()
                    bullet.reload()
                    if i>=2:
                        aliens[i][j].decrease_shotprob(300)
                    break
            if bullet.rect.centery<0:
                player.reload()
                bullet.reload()
        
        indexes=[]
        for i in range(len(albullets)):
            if player.rect.colliderect(albullets[i].rect):
                player.lives-=1
                indexes.append(i)
            elif albullets[i].rect.centery>screen.get_height():
                indexes.append(i)

        for i in reversed(indexes):
            albullets[i].owner.bullets-=1
            albullets.pop(i)



        screen.fill((0,0,0))
        show(all_aliens,player,bullet,albullets)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
                break

            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RIGHT:
                    direction = 5
                elif event.key==pygame.K_LEFT:
                    direction = -5
                elif event.key==pygame.K_SPACE and player.state == 'LOADED':
                    bullet.follow(player)
                    player.shoot()

            elif event.type==pygame.KEYUP:
                if event.key in (pygame.K_RIGHT,pygame.K_LEFT):
                    direction = 0
