import pygame, pytmx, pyscroll
from dataclasses import dataclass
from player import *
from save import Save

@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str

@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    npcs: list[NPC]

class MapManager:
    def __init__(self, screen, player):

        # initailisation de MapManager, avec création d'un dictionnaire vide pour les maps
        self.maps = dict()
        self.screen = screen
        self.player = player

        if Save.Saved:
            self.current_map = Save.dict_values["world_perso"]
        else:
            self.current_map = "Couloir"

        self.register_map('Couloir', portals=[
            Portal(from_world='Couloir', origin_point='enter_salle10', target_world='Salle10', teleport_point='spawn_salle10'),
            Portal(from_world='Couloir', origin_point='enter_salle11', target_world='Salle11', teleport_point='spawn_salle11'),
            Portal(from_world='Couloir', origin_point='enter_salle12', target_world='Salle12', teleport_point='spawn_salle12')
        ])
        self.register_map('Salle10', portals=[
            Portal(from_world='Salle10', origin_point='exit_salle', target_world='Couloir', teleport_point='exit_salle10')
        ], npcs=[
            NPC("paul", 4,1, dialog=["Bonne aventure", "Tu voudrais te soigner ?", "/menu_dialogue/", "*choix", "a bientot"]),
        ]),
        self.register_map('Salle11', portals=[
            Portal(from_world='Salle11', origin_point='exit_salle', target_world='Couloir', teleport_point='exit_salle11')
        ], npcs=[
            NPC("robin", 2, 1, dialog=["Salut, ça va"]),
        ]),
        self.register_map('Salle12', portals=[
            Portal(from_world='Salle12', origin_point='exit_salle', target_world='Couloir', teleport_point='exit_salle12')
        ])

        # déplacement du joueur à son point de départ (ou aux coordonnées enregistrées par la save)
        if Save.Saved:
            self.player.position[0] = Save.dict_values["x_perso"]
            self.player.position[1] = Save.dict_values["y_perso"]
        else:
            self.teleport_player("player_spawn")

        # placement PNJ
        self.teleport_npcs()

        # Utilisé pour les dialogues : checker si on peut obtim en définissant une méthodes pour avoir les PNJ et pas passer par les sprites

    def check_npc_collisions(self, dialog_box):
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC:
                dialog_box.execute(sprite)

    def check_collisions(self):
        # portails
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)

                    # perdre de la vie en passant par ce portail
                    self.player.stats['health'] -= 10
                    if self.current_map == "Couloir":
                        self.player.speed = self.player.speed_base
                    else:
                        self.player.speed -= 1

        # verifier les collisions
        for sprite in self.get_group().sprites():
            if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = sprite.stats['speed']

            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()
    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x -15
        self.player.position[1] = point.y -20
        self.player.save_location()
    def register_map(self, name, portals=[], npcs=[]):

        tmx_data = pytmx.util_pygame.load_pygame(f'../map/{name}.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        walls = []

        for obj in tmx_data.objects:
            if obj.type == 'collision':
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)
        group.add(self.player)

        # récupérer tous les NPC pour les ajouter au groupe

        for npc in npcs:
            group.add(npc)

        # créer un objet map
        self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs)

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    # dans toutes les maps, aller chercher les NPC dans map_data et les mettre en position
    def teleport_npcs(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs

            for npc in npcs:
                npc.load_points(map_data.tmx_data)

                npc.teleport_spawn()

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collisions()