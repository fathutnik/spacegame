import pygame
import random
import time
from pygame.transform import scale

b = False
max_time = 0

fps = 60

#
pygame.init()
display_width = 800
display_height = 600
sky = scale(pygame.image.load("sky.png"), (800, 600))
font = pygame.font.SysFont('Comic Sans MS', 30)


black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (102, 255, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

car_width = 73

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Space')
clock = pygame.time.Clock()

carImg = pygame.image.load('ship.png')

pause = False



def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(screen, color, [thingx, thingy, thingw, thingh])


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    screen.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

    game_loop()



def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)





def game_intro():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(white)
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects("Space game", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        screen.blit(TextSurf, TextRect)

        button("Старт",150,450,100,50,green,bright_green,game_loop)
        button("Рекроды",550,450,100,50,red,bright_red,record)

        pygame.display.update()
        clock.tick(15)



def game_loop():

    global recording
    recording = False
    start_time = time.time()
    class Bullet(pygame.sprite.Sprite):
            def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                self.rect = pygame.Rect(x, y, 10, 36)
                self.image = scale(pygame.image.load("bullet.png"), (10, 36))
                self.yvel = 5

            def draw(self, screen):
                screen.blit(self.image, (self.rect.x, self.rect.y))

            def update(self):
                self.rect.y += self.yvel

    class Asteroid(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = scale(pygame.image.load("asteroid.png"), (50, 50))
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(display_width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            self.speedx = random.randrange(-3, 3)

        def update(self):
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.top > display_height + 10 or self.rect.left < -25 or self.rect.right > display_width + 20:
                self.rect.x = random.randrange(display_width - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(1, 8)

    class Explosion(pygame.sprite.Sprite):
        def __init__(self, x, y):
            self.rect = pygame.Rect(x, y, 40, 40)
            self.images = []
            self.index = 0

            for i in range(8):
                image = scale(pygame.image.load(f"explosion/tile00{i}.png"), (40, 40))
                self.images.append(image)

        def draw(self, screen):
            if self.index < 8:
                screen.blit(self.images[self.index], (self.rect.x, self.rect.y))
                self.index += 1

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = scale(pygame.image.load("bullet.png"), (10, 20))
            self.rect = self.image.get_rect()
            self.rect.bottom = y
            self.rect.centerx = x
            self.speedy = -10

        def update(self):
            self.rect.y += self.speedy
            if self.rect.bottom < 0:
                self.kill()

    class Spaceship(pygame.sprite.Sprite):

        def shoot(self):
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

        def __init__(self, x, y):
            self.rect = pygame.Rect(x, y, 50, 100)
            self.image = scale(pygame.image.load("ship.png"), (50, 100))
            self.xvel = 0
            self.life = 100
            self.explosions = []

        def draw(self, screen):
            screen.blit(self.image, (self.rect.x, self.rect.y))

            for explosion in self.explosions:
                explosion.draw(screen)

        def update(self, left, right, up, down, asteroids):
            if left:
                self.xvel += -3

            if right:
                self.xvel += 3

            if up:
                self.yvel += -3

            if down:
                self.yvel += 3

            if not (left or right or up or down):
                self.xvel = 0
                self.yvel = 0

            for asteroid in asteroids:
                if self.rect.colliderect(asteroid.rect):
                    self.life -= 1
                    rx = random.randint(-5, 40)
                    ry = random.randint(-5, 40)
                    explosion = Explosion(self.rect.x + rx, self.rect.y + ry)
                    self.explosions.append(explosion)

            self.rect.x += self.xvel
            self.rect.y += self.yvel

            if self.rect.y > 600:
                self.rect.y = 0
            if self.rect.x > 800:
                self.rect.x = 0
            if self.rect.y < 0:
                self.rect.y = 600
            if self.rect.x < 0:
                self.rect.x = 800

    pygame.display.set_caption("Asteroids")

    timer = pygame.time.Clock()

    sky = scale(pygame.image.load("sky.png"), (800, 600))
    ship = Spaceship(400, 400)

    left = False
    right = False
    up = False
    down = False
    space = False

    bullets = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 30)
    global a
    a = 2
    for i in range(30):
        m = Asteroid()
        all_sprites.add(m)
        asteroids.add(m)
    while a != 1:
        hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
        for hit in hits:
            m = Asteroid()
            all_sprites.add(m)
            asteroids.add(m)

        timer.tick(60)

        for e in pygame.event.get():

            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    ship.shoot()

            if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
                left = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
                right = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
                up = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN:
                down = True

            if e.type == pygame.KEYUP and e.key == pygame.K_UP:
                up = False
            if e.type == pygame.KEYUP and e.key == pygame.K_DOWN:
                down = False
            if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
                left = False
            if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
                right = False


            if e.type == pygame.QUIT:
                raise SystemExit("QUIT")
        if ship.life < 0:
            a = 1
        global times
        times = time.time() - start_time
        global max_time
        if max_time < times:
            max_time = times
        print(max_time//1)
        screen.blit(sky, (0, 0))

        ship.update(left, right, up, down, asteroids)
        ship.draw(screen)




        textsurface = font.render(f'HP: {ship.life}', False, (255, 255, 255))
        screen.blit(textsurface, (20, 20))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.update()

    while a != 2:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                raise SystemExit("QUIT")
        screen.blit(sky, (0, 0))
        seconds = font.render(f"Ваше время: {times//1} секунд", False, (255, 255, 255))
        screen.blit(seconds, (300, 400))
        return game_intro2()
    pygame.display.update()




def game_intro2():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(white)
        largeText = pygame.font.SysFont("comicsansms",115)
        text = font.render("Вы проиграли ваше время: "+str(times//1), True, black)
        screen.blit(text,(400,300))
        button("Старт",150,450,100,50,green,bright_green,game_loop)
        button("Рекроды",550,450,100,50,red,bright_red,record)

        pygame.display.update()
        clock.tick(15)



def record():
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
               raise SystemExit("QUIT")
        screen.fill(white)
        font = pygame.font.SysFont("comicsansms", 50)
        text = font.render("Рекорд: "+str(max_time//1), True, black)
        button("Старт",150,450,100,50,green,bright_green,game_intro)
        screen.blit(text,(400,300))
        pygame.display.update()

game_intro()
game_loop()
pygame.quit()
quit()
