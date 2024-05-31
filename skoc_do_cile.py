import pygame
pygame.init()

clock = pygame.time.Clock()
fps = 60
#nastavení šířky, výšky
sirka = 800
vyska = 600

screen = pygame.display.set_mode((sirka, vyska))
pygame.display.set_caption('skoč do cíle')

#proměnné
velikost_kostky = 40
konec_hry = 0

# ořízne obrázky, kvůli hitboxu
def oriznuti_obrazku(image, left, top, right, bottom):
    width, height = image.get_size()
    
    new_width = width - left - right
    new_height = height - top - bottom
  
    crop_rect = pygame.Rect(left, top, new_width, new_height)
    cropped_image = image.subsurface(crop_rect).copy()
    return cropped_image


left, top, right, bottom = 17, 10, 17, 1

# načtení obrázků
restart_img = pygame.image.load('platform/restart2.png')
obrazky_doprava = [
    oriznuti_obrazku(pygame.image.load('Game/R1.png'), left, top, right, bottom), 
    oriznuti_obrazku(pygame.image.load('Game/R2.png'), left, top, right, bottom),
    oriznuti_obrazku(pygame.image.load('Game/R3.png'), left, top, right, bottom), 
    oriznuti_obrazku(pygame.image.load('Game/R4.png'), left, top, right, bottom),
    oriznuti_obrazku(pygame.image.load('Game/R5.png'), left, top, right, bottom), 
    oriznuti_obrazku(pygame.image.load('Game/R6.png'), left, top, right, bottom),
    oriznuti_obrazku(pygame.image.load('Game/R7.png'), left, top, right, bottom), 
    oriznuti_obrazku(pygame.image.load('Game/R8.png'), left, top, right, bottom),
    oriznuti_obrazku(pygame.image.load('Game/R9.png'), left, top, right, bottom)
]

obrazky_doleva = [
    oriznuti_obrazku(pygame.image.load('Game/L1.png'), left, top, right, bottom), 
    oriznuti_obrazku(pygame.image.load('Game/L2.png'), left, top, right, bottom),
    oriznuti_obrazku(pygame.image.load('Game/L3.png'), left, top, right, bottom), 
    oriznuti_obrazku(pygame.image.load('Game/L4.png'), left, top, right, bottom),
    oriznuti_obrazku(pygame.image.load('Game/L5.png'), left, top, right, bottom), 
    oriznuti_obrazku(pygame.image.load('Game/L6.png'), left, top, right, bottom),
    oriznuti_obrazku(pygame.image.load('Game/L7.png'), left, top, right, bottom), 
    oriznuti_obrazku(pygame.image.load('Game/L8.png'), left, top, right, bottom),
    oriznuti_obrazku(pygame.image.load('Game/L9.png'), left, top, right, bottom)
]



pozadí = pygame.image.load('data/background.png')

class Tlacitko():
    def __init__(self, x, y, image):
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.stisknute = False

    def draw(self):
        action = False
        #pozice myši
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.stisknute == False:
                action = True
                self.stisknute = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.stisknute = False

        screen.blit(self.image, self.rect)

        return action

    def center(self, sirka, vyska):
        self.rect.x = (sirka - self.rect.width) // 2
        self.rect.y = (vyska - self.rect.height) // 2

class Hrac():
    def __init__(self, x, y):
         self.reset(x, y)
         self.snimek_animace = 0

    def reset(self, x, y):
        self.obrazky_doprava = obrazky_doprava
        self.obrazky_doleva = obrazky_doleva
        self.index = 0

        self.obraz = self.obrazky_doprava[self.index]
        self.rect = self.obraz.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.obraz.get_width()
        self.height = self.obraz.get_height()
        self.pohyb_dolu_nahoru = 0
        self.skok = False
        self.direction = 0
        self.ve_vzduchu= True #je hráč ve vzduchu?
        self.snimek_animace = 0

    def update(self, konec_hry):
        pohyb_po_x = 0
        pohyb_po_y = 0
        rychlost_animace = 5  # určuje rychlost animace

        if konec_hry == 0:
            # kontroluje, jaké klávesy jsou zmáčknuté
            key = pygame.key.get_pressed()
            if key[pygame.K_w] and self.skok == False and self.ve_vzduchu== False:
                self.pohyb_dolu_nahoru = -15
                self.skok = True
            if key[pygame.K_w] == False:
                self.skok = False
            if key[pygame.K_a]:
                pohyb_po_x -= 5
                self.snimek_animace += 1
                self.direction = -1
            if key[pygame.K_d]:
                pohyb_po_x += 5
                self.snimek_animace += 1
                self.direction = 1
            if key[pygame.K_a] == False and key[pygame.K_d] == False:
                self.snimek_animace = 0
                self.index = 0

            # zpracování animace
            if self.snimek_animace > rychlost_animace:
                self.snimek_animace = 0
                self.index += 1
                if self.index >= len(self.obrazky_doprava):
                    self.index = 0
                if self.direction == 1:
                    self.obraz = self.obrazky_doprava[self.index]
                if self.direction == -1:
                    self.obraz = self.obrazky_doleva[self.index]

            # přidání gravitace
            self.pohyb_dolu_nahoru += 1
            if self.pohyb_dolu_nahoru > 10:
                self.pohyb_dolu_nahoru = 10
            pohyb_po_y += self.pohyb_dolu_nahoru

            # kontrola kolizí
            self.ve_vzduchu = True
            for tile in world.seznam_kostek:
                # kontrola kolize ve směru x
                if tile[1].colliderect(self.rect.x + pohyb_po_x, self.rect.y, self.width, self.height):
                    pohyb_po_x = 0
                # kontrola kolize ve směru y
                if tile[1].colliderect(self.rect.x, self.rect.y + pohyb_po_y, self.width, self.height):
                    # kontrola, zda je pod zemí (skákání)
                    if self.pohyb_dolu_nahoru < 0:
                        pohyb_po_y = tile[1].bottom - self.rect.top
                        self.pohyb_dolu_nahoru = 0
                    # kontrola, zda je nad zemí (padání)
                    elif self.pohyb_dolu_nahoru >= 0:
                        pohyb_po_y = tile[1].top - self.rect.bottom
                        self.pohyb_dolu_nahoru = 0
                        self.ve_vzduchu= False

            # kolize s nepřáteli
            if pygame.sprite.spritecollide(self, angry_man_group, False):
                konec_hry = -1

            # kolize s lávou
            if pygame.sprite.spritecollide(self, lava_group, False):
                konec_hry = -1

            # kolize s koncem hry
            if pygame.sprite.spritecollide(self, konec_hry_group, False):
                konec_hry = -1

            # aktualizace souřadnic hráče
            self.rect.x += pohyb_po_x
            self.rect.y += pohyb_po_y

            if self.rect.bottom > vyska:
                self.rect.bottom = sirka
                pohyb_po_y = 0

        # vykreslení hráče na obrazovku
        screen.blit(self.obraz, self.rect)
        

        return konec_hry


class World():
    def __init__(self, data):
        self.seznam_kostek = []

        # načtení obrázků
        obrazek_bloku = pygame.image.load('platform/stone.png')
        obrazek_bloku2 = pygame.image.load('platform/grass.png')

        pozice_v_radku = 0
        for row in data:
            pozice_v_sloupci = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(obrazek_bloku, (velikost_kostky, velikost_kostky))
                    img_rect = img.get_rect()
                    img_rect.x = pozice_v_sloupci * velikost_kostky
                    img_rect.y = pozice_v_radku * velikost_kostky
                    tile = (img, img_rect)
                    self.seznam_kostek.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(obrazek_bloku2, (velikost_kostky, velikost_kostky))
                    img_rect = img.get_rect()
                    img_rect.x = pozice_v_sloupci * velikost_kostky
                    img_rect.y = pozice_v_radku * velikost_kostky
                    tile = (img, img_rect)
                    self.seznam_kostek.append(tile)
                if tile == 3:
                    angry_man = Enemy(pozice_v_sloupci * velikost_kostky, pozice_v_radku * velikost_kostky)
                    angry_man_group.add(angry_man)
                if tile == 4:
                    lava = Lava(pozice_v_sloupci * velikost_kostky, pozice_v_radku * velikost_kostky)
                    lava_group.add(lava)
                if tile == 5:
                    konec_hry =konecHry(pozice_v_sloupci * velikost_kostky, pozice_v_radku * velikost_kostky)
                    konec_hry_group.add(konec_hry)

                pozice_v_sloupci += 1
            pozice_v_radku += 1

    def draw(self):
        for tile in self.seznam_kostek:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2) #vykresluje bílé čáry, aby nebyly mezery

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_enemy = pygame.image.load('platform/blockerMad.png')
        self.image = pygame.transform.scale(self.image_enemy, (velikost_kostky, velikost_kostky))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vpravo_nebo_vlevo = 1 #určuje jakým směrem se nepřítel pohybuje
        self.pocet_kroku = 0 #sleduje počet kroků

    def update(self):
        self.rect.x += self.vpravo_nebo_vlevo
        self.pocet_kroku += 1
        if abs(self.pocet_kroku) > 50:
            self.vpravo_nebo_vlevo *= -1
            self.pocet_kroku *= -1

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img_lava = pygame.image.load('platform/lava.png')
        self.image = pygame.transform.scale(img_lava, (velikost_kostky, velikost_kostky))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class konecHry(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img_flag = pygame.image.load('platform/flagRed.png')
        self.image = pygame.transform.scale(img_flag, (velikost_kostky, velikost_kostky))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

hrac_pozice = Hrac(100, vyska - 130)

angry_man_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
konec_hry_group = pygame.sprite.Group()

data_sveta = [
    [1, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 2, 2, 2, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 1],
    [1, 0, 0, 0, 2, 2, 0, 0, 2, 0, 0, 0, 2, 0, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 2, 1, 1, 4, 4, 1, 4, 4, 4, 1, 4, 4, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

world = World(data_sveta)

restart_button = Tlacitko(sirka // 2 - 50, vyska // 2 + 100, restart_img)
restart_button.center(sirka, vyska)

run = True
pygame.mixer.music.load("platform/music.mp3")  
pygame.mixer.music.play(-1)  
while run:
    

    clock.tick(fps)

    screen.blit(pozadí, (0, 0))
    world.draw()

    if konec_hry == 0:
        angry_man_group.update()
    angry_man_group.draw(screen)
    lava_group.draw(screen)
    konec_hry_group.draw(screen)

    konec_hry = hrac_pozice.update(konec_hry)

    

    if konec_hry == -1:
        if restart_button.draw():
            hrac_pozice.reset(100, vyska - 130)
            konec_hry = 0

    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()