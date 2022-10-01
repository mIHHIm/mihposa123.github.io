import pygame, random, time, sys

WIDTH = 1830
HEIGHT = 1005
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()
ancho_play = 120
alto_play = 119.125
player123 = pygame.image.load("assets/nave.png").convert()
player200 = pygame.image.load("assets/player1.png").convert()
player300 = pygame.image.load("assets/player.png").convert()
def draw_text(surface, text, size, x, y):       
    font = pygame.font.SysFont("serif", size)  
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)                      #midtop?
    surface.blit(text_surface, text_rect)
    
def draw_shield_bar(surface, x ,y, percentage):   #barra de salud
    BAR_LENGHT = 100
    BAR_HEIGHT = 10
    fill = (percentage / 100) * BAR_LENGHT           #que tanto lo va a llenar segun porcentage
    border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill) 
    pygame.draw.rect(surface, WHITE, border, 2)  #grosor linea


class Player(pygame.sprite.Sprite):
    def __init__(self):                          
        super().__init__()
        self.image = pygame.transform.scale(player123, (ancho_play, alto_play))  #descomenta para habilitar player123
        self.image.set_colorkey(WHITE)          #elimina el color de fondo
        #self.image = pygame.transform.scale(player200, (ancho_play, alto_play))   #descomenta para habilitar player200
        #self.image.set_colorkey(BLACK)          #elimina el color de fondo
        #self.image = pygame.transform.scale(player300, (ancho_play, alto_play))     #descomenta para habilitar player300
        #self.image.set_colorkey(BLACK)            #elimina el color de fondo
        self.rect = self.image.get_rect()  
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0  #se mueve si presionan la tecla
        self.speed_y = 0    #se mueve si presionan la tecla
        self.shield = 100    #barra de salud
        
    def update(self):
        self.speed_x = 0     #se mueve sin limite
        self.speed_y = 0      #se mueve sin limite
        keystate = pygame.key.get_pressed() 
        if keystate[pygame.K_LEFT]:
            self.speed_x = - 5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        if keystate[pygame.K_UP]:
            self.speed_y = - 5
        if keystate[pygame.K_DOWN]:
            self.speed_y = 5
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y  
        if self.rect.right > WIDTH: 
            self.rect.right = WIDTH 
        if self.rect.left < 0: 
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0       
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        laser_sound.play()
            
class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #self.image = pygame.image.load("assets/meteorGrey_med1.png")
        self.image = random.choice(meteor_images)#selecciona aleatoriamente de meteor_images
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width) 
        #self.rect.y = random.randrange(-100, -40)
        self.rect.y = random.randrange(-140, -100) #agranda su rango de alcance
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)
    def update(self):
        self.rect.y += self.speedy 
        self.rect.x += self.speedx 
        #if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25: 
        if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40: 
            self.rect.x = random.randrange(WIDTH - self.rect.width) 
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 10)

class Planet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #self.image = pygame.image.load("assets/meteorGrey_med1.png")
        self.image = random.choice(planet_anim)#selecciona aleatoriamente de meteor_images
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width) 
        #self.rect.y = random.randrange(-100, -40)
        self.rect.y = random.randrange(-140, -100) #agranda su rango de alcance
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)
    def update(self):
        self.rect.y += self.speedy 
        self.rect.x += self.speedx 
        #if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25: 
        if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40: 
            self.rect.x = random.randrange(WIDTH - self.rect.width) 
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 10)
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/laser1.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y 
        self.rect.x = x
        self.rect.centerx = x 
        self.speedy = -10 
        
    def update(self):
        self.rect.y += self.speedy 
        if self.rect.bottom < 0: 
            self.kill() 
            
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_anim[0] #empieza con la priimera imagen
        self.rect = self.image.get_rect()
        self.rect.center = center 
        self.frame = 0 # anima la animacion
        self.last_update = pygame.time.get_ticks()# me permite saber cuanto ha transcurrido
        self.frame_rate = 50 #velocidad de la explosion
        
    def update(self):
        now = pygame.time.get_ticks() #me permite saber cuanto tiempo transcurrido la explosion
        if now - self.last_update > self.frame_rate:  # si lo que transcurrio es mayor que 50
            self.last_update = now        #si es mayor que 50 inicia la explosion
            self.frame += 1 # por todos los elementos de la lista
            if self.frame == len(explosion_anim): #aveigua si llego al final de la lista
                self.kill() # si es cierto elimina los sprites
            else: #inicia con la explosion
                center = self.rect.center
                self.image = explosion_anim[self.frame]  #frame itera en la lista
                self.rect = self.image.get_rect()
                self.rect.center = center 
                
def show_go_screen():
    draw_text(screen, "SHOTTER", 65, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "instrucciones van aqui", 27, WIDTH // 2, HEIGHT // 2)
    draw_text(screen, "press Key", 20, WIDTH // 2, HEIGHT * 3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False       
    
meteor_images = [] #es una lsita vacia
meteor_list = ["assets/meteorGrey_big1.png", "assets/meteorGrey_big2.png", "assets/meteorGrey_big3.png", "assets/meteorGrey_big4.png",
               "assets/meteorGrey_med1.png", "assets/meteorGrey_med2.png", "assets/meteorGrey_small1.png", "assets/meteorGrey_small2.png", 
               "assets/meteorGrey_tiny1.png", "assets/meteorGrey_tiny2.png"]  
 
for img in meteor_list: #guarda las imagenes en meteor images
    meteor_images.append(pygame.image.load(img).convert())
 
############------explosiones-------------------------------
explosion_anim = []
for i in range(9):
    file = "assets/regularExplosion0{}.png".format(i)#remplaza lo que hay en llaves por i
    img = pygame.image.load(file).convert()
    img.set_colorkey(BLACK)
    img_scale = pygame.transform.scale(img, (70, 70))
    explosion_anim.append(img_scale) # agrega la imagen escalada

planet_anim = []
for i in range(3):
    file_planet = "assets/planet0{}.png".format(i)#remplaza lo que hay en llaves por i
    img_planet = pygame.image.load(file_planet).convert()
    img_planet.set_colorkey(BLACK)
    img_scale_planet = pygame.transform.scale(img_planet, (170, 170))
    planet_anim.append(img_scale_planet)
    
                                       
background = pygame.image.load("assets/espacio.jpg").convert()

#cargar sonidos
laser_sound = pygame.mixer.Sound("assets/audio/laser5.ogg") 
explosion_sound = pygame.mixer.Sound("assets/audio/explosion.wav")
pygame.mixer.music.load("assets/audio/music.ogg")   #carga la musica
pygame.mixer.music.set_volume(4)    #controla el volumen
metal_sound = pygame.mixer.Sound("assets/audio/golpe-metalico.ogg")
            
######---game_over
game_over = True    
runnig = True             
while runnig: 
    if game_over:
        
        show_go_screen()
        
        game_over = False
        all_sprites = pygame.sprite.Group()  
        meteor_list =pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        planet1_list = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player)
        for i in range(24):
            meteor = Meteor()
            all_sprites.add(meteor)
            meteor_list.add(meteor)
        for i in range(2):
            planet1 = Planet()
            all_sprites.add(planet1)
            meteor_list.add(planet1)
        
        score = 0
        pygame.mixer.music.play(loops=-1)# loop define indefinadamente

        mih_score = "SCORE: "
        
    clock.tick(60) #pasar el juego para ver los cambios  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:
            #runnig = False      #cierra la ventana
            game_over = True        #a terminado y me paso a game_over
        
        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE:
                player.shoot()  
    
    all_sprites.update() 
    
    
    hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True) 
    for hit in hits:   
        explosion_sound.play()
        score += 10 
        #explosion
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)
    
    hits = pygame.sprite.spritecollide(player, meteor_list, True)
    for hit in hits:                               #se crea un for loop cada vez que impacte
        metal_sound.play()
        player.shield -= 15                         #resta vidas
                                                            
        meteor = Meteor()                   #crea nuevos asteroides
        all_sprites.add(meteor)
        meteor_list.add(meteor)                           
        if player.shield <= 0:               
            game_over = True 
            
    
    screen.blit(background, [0, 0]) 
     
    all_sprites.draw(screen)
    
     
    draw_text(screen, str(score) , 25, WIDTH // 2, 10) 
    draw_text(screen, str(mih_score) ,25, 345, 10 )
    #escudo
    draw_shield_bar(screen, 5, 5, player.shield)# 5,5 cordenadas, porcentaje de la vida
    pygame.display.flip()
pygame.quit()