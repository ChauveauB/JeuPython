import pygame, pytmx, pyscroll
from UI import UI
from player import Player


class Game:

    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.running = True
        self.map = "world"

        # user interface
        self.ui = UI()

        # créer la fenetre
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Jeupython")

        #charger la carte

        tmx_data=pytmx.util_pygame.load_pygame('../map/carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # générer un joueur

        player_position = tmx_data.get_object_by_name("player")

        self.player = Player(player_position.x, player_position.y)

        # liste pour les rectangles de collision

        self.walls=[]

        for obj in tmx_data.objects :
            if obj.type == "collision" :
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calque

        self.group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer=5)
        self.group.add(self.player)

        # définir le rectangle de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name('enter_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)
    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_ESCAPE]:
            self.running = False
        elif pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation("right")

    def switch_house(self):
        
        self.map = 'house'
        # charger la carte

        tmx_data = pytmx.util_pygame.load_pygame('../map/house.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # liste pour les rectangles de collision

        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calque

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        # définir le rectangle de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name('exit_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        # récupérer le point de spawn de la maison
        spawn_house_point = tmx_data.get_object_by_name('spawn_house')
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y - 20

    def switch_world(self):
        
        self.map = "world"
        # charger la carte

        tmx_data = pytmx.util_pygame.load_pygame('../map/carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # liste pour les rectangles de collision

        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calque

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        # définir le rectangle de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name('enter_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        # récupérer le point de spawn devant la maison
        spawn_house_point = tmx_data.get_object_by_name('enter_house_exit')
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y +  20
    def update(self):
        self.group.update()

        #vérifier l'entrée dans la maison
        if self.map == "world" and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()

        # vérifier l'entrée dans la maison
        if self.map == "house" and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_world()

        # vérification collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1 :
                sprite.move_back()
    def run(self):

        clock = pygame.time.Clock()

        # boucle du jeu

        running = True

        while running:
            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            self.ui.display(self.player)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)

        pygame.quit()