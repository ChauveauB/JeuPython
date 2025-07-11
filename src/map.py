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

        if Save.Saved:      # Si fichier de sauvergarde --> charger la carte enregistrée
            self.current_map = Save.dict_values["world_perso"]
        else:               # Sinon charger la carte de base
            self.current_map = "Couloir"

        self.register_map('Couloir', portals=[
            Portal(from_world='Couloir', origin_point='enter_salle10', target_world='Salle10', teleport_point='spawn_salle10'),
            Portal(from_world='Couloir', origin_point='enter_salle11', target_world='Salle11', teleport_point='spawn_salle11'),
            Portal(from_world='Couloir', origin_point='enter_salle12', target_world='Salle12', teleport_point='spawn_salle12'),
            Portal(from_world='Couloir', origin_point='enter_foret_A1', target_world='foret_A1', teleport_point='spawn_foret')
        ])              # Définitions des différentes transitions entre les cartes
        self.register_map('Salle10', portals=[
            Portal(from_world='Salle10', origin_point='exit_salle', target_world='Couloir', teleport_point='exit_salle10')      # Pour sortir de la carte Salle10
        ], npcs=[
            NPC("paul", 4,1, dialog=["Bonne aventure", "Tu voudrais te soigner ?", "/menu_dialogue/", "*choix", "a bientot"]),      # PNJ de cette carte
        ]),
        self.register_map('Salle11', portals=[
            Portal(from_world='Salle11', origin_point='exit_salle', target_world='Couloir', teleport_point='exit_salle11')      # Pour sortir de la carte Salle11
        ], npcs=[
            NPC("robin", 2, 1, dialog=["Nous allons nous combattre !", "/combat/", "a bientot"]),      # PNJ de cette carte
        ]),
        self.register_map('Salle12', portals=[
            Portal(from_world='Salle12', origin_point='exit_salle', target_world='Couloir', teleport_point='exit_salle12')      # Pour sortir de la carte Salle12
        ])
        self.register_map('foret_A1', portals=[
            Portal(from_world='foret_A1', origin_point='exit_foret', target_world='Couloir',teleport_point='exit_foret'),
            Portal(from_world='foret_A1', origin_point='enter_foret_E10', target_world='foret_E10',teleport_point='spawn_foret_A1'),
            Portal(from_world='foret_A1', origin_point='enter_foret_D2', target_world='foret_D2',teleport_point='spawn_foret_A1'),
            Portal(from_world='foret_A1', origin_point='enter_foret_B9', target_world='foret_B9',teleport_point='spawn_foret_A1')
        ])
        self.register_map('foret_A3', portals=[
            Portal(from_world='foret_A3', origin_point='exit_foret_A3', target_world='foret_D2',teleport_point='spawn_foret_A3'),
            Portal(from_world='foret_A3', origin_point='enter_foret_A5', target_world='foret_A5',teleport_point='spawn_foret_A3'),
            Portal(from_world='foret_A3', origin_point='dead_end', target_world='foret_A1',teleport_point='spawn_foret')
        ])
        self.register_map('foret_A5', portals=[
            Portal(from_world='foret_A5', origin_point='exit_foret_A5', target_world='foret_A3',teleport_point='spawn_foret_A5'),
            Portal(from_world='foret_A5', origin_point='enter_foret_B6', target_world='foret_B6',teleport_point='spawn_foret_A5'),
            Portal(from_world='foret_A5', origin_point='enter_foret_B7', target_world='foret_B7',teleport_point='spawn_foret_A5'),
            Portal(from_world='foret_A5', origin_point='dead_end', target_world='foret_A1',teleport_point='spawn_foret')
        ])
        self.register_map('foret_A8', portals=[
            Portal(from_world='foret_A8', origin_point='exit_foret_A8', target_world='foret_B7',teleport_point='spawn_foret_A8'),
            Portal(from_world='foret_A8', origin_point='dead_end', target_world='foret_A1',teleport_point='spawn_foret')
        ])
        self.register_map('foret_A13', portals=[
            Portal(from_world='foret_A13', origin_point='exit_foret_A13', target_world='foret_B11',teleport_point='spawn_foret_A13'),
            Portal(from_world='foret_A13', origin_point='enter_foret_B14', target_world='foret_B14',teleport_point='spawn_foret_A13'),
            Portal(from_world='foret_A13', origin_point='dead_end', target_world='foret_A1',teleport_point='spawn_foret')
        ])
        self.register_map('foret_A17', portals=[
            Portal(from_world='foret_A17', origin_point='exit_foret_A17', target_world='foret_E16',teleport_point='spawn_foret_A17'),
            Portal(from_world='foret_A17', origin_point='enter_foret_C20', target_world='foret_C20',teleport_point='spawn_foret_A17'),
            Portal(from_world='foret_A17', origin_point='enter_foret_E18', target_world='foret_E18',teleport_point='spawn_foret_A17'),
            Portal(from_world='foret_A17', origin_point='dead_end', target_world='foret_A1',teleport_point='spawn_foret')
        ])
        self.register_map('foret_A21', portals=[
            Portal(from_world='foret_A21', origin_point='exit_foret_A21', target_world='foret_C20', teleport_point='spawn_foretA21'),
            Portal(from_world='foret_A21', origin_point='dead_end', target_world='foret_A1',teleport_point='spawn_foret')
        ])
        self.register_map('foret_B6', portals=[
            Portal(from_world='foret_B6', origin_point='exit_foret_B6', target_world='foret_A5',teleport_point='spawn_foret_B6'),
            Portal(from_world='foret_B6', origin_point='dead_end', target_world='foret_A1',teleport_point='spawn_foret')
        ])
        self.register_map('foret_B7', portals=[
            Portal(from_world='foret_B7', origin_point='exit_foret_B7', target_world='foret_A5',teleport_point='spawn_foret_B7'),
            Portal(from_world='foret_B7', origin_point='enter_foret_A8', target_world='foret_A8',teleport_point='spawn_foret_B7'),
            Portal(from_world='foret_B7', origin_point='dead_end', target_world='foret_A1',teleport_point='spawn_foret')
        ])
        self.register_map('foret_B9', portals=[
            Portal(from_world='foret_B9', origin_point='exit_foret_B9', target_world='foret_A1',teleport_point='spawn_foret_B9'),
            Portal(from_world='foret_B9', origin_point='dead_end', target_world='foret_A1',teleport_point='spawn_foret')
        ])
        self.register_map('foret_B11', portals=[
            Portal(from_world='foret_B11', origin_point='exit_foret_B11', target_world='foret_E10',teleport_point='spawn_foret_B11'),
            Portal(from_world='foret_B11', origin_point='enter_foret_A13', target_world='foret_A13',teleport_point='spawn_foret_B11'),
            Portal(from_world='foret_B11', origin_point='enter_foret_B12', target_world='foret_B12',teleport_point='spawn_foret_B11')
        ])
        self.register_map('foret_B12', portals=[
            Portal(from_world='foret_B12', origin_point='exit_foret_B12', target_world='foret_B11',teleport_point='spawn_foret_B12'),
            Portal(from_world='foret_B12', origin_point='dead_end', target_world='foret_A1',teleport_point='spawn_foret')
        ])
        self.register_map('foret_B14', portals=[
            Portal(from_world='foret_B14', origin_point='exit_foret_B14', target_world='foret_A13',teleport_point='spawn_foret_B14'),
            Portal(from_world='foret_B14', origin_point='enter_foret_A15', target_world='foret_A15',teleport_point='spawn_foret_B14'),
            Portal(from_world='foret_B14', origin_point='dead_end', target_world='foret_A1',teleport_point='spawn_foret')
        ])
        self.register_map('foret_B19', portals=[
            Portal(from_world='foret_B19', origin_point='exit_foret_B19', target_world='foret_E18',teleport_point='spawn_foret_B19'),
            Portal(from_world='foret_B19', origin_point='dead_end', target_world='foret_A1',teleport_point='spawn_foret')
        ])
        self.register_map('foret_C20', portals=[
            Portal(from_world='foret_C20', origin_point='exit_foret_C20', target_world='foret_A17',teleport_point='spawn_foret_C20'),
            Portal(from_world='foret_C20', origin_point='enter_foret_A21', target_world='foret_A21',teleport_point='spawn_foret_C20')
        ])
        self.register_map('foret_D2', portals=[
            Portal(from_world='foret_D2', origin_point='exit_foret_D2', target_world='foret_A1',teleport_point='spawn_foret_D2'),
            Portal(from_world='foret_D2', origin_point='enter_foret_A3', target_world='foret_A3',teleport_point='spawn_foret_D2'),
            Portal(from_world='foret_D2', origin_point='dead_end', target_world='foret_A1',teleport_point='spawn_foret')
        ])
        self.register_map('foret_E10', portals=[
            Portal(from_world='foret_E10', origin_point='exit_foret_E10', target_world='foret_A1',teleport_point='spawn_foret_E10'),
            Portal(from_world='foret_E10', origin_point='enter_foret_B11', target_world='foret_B11',teleport_point='spawn_foret_E10'),
            Portal(from_world='foret_E10', origin_point='dead_end', target_world='foret_A1',teleport_point='spawn_foret')
        ])
        self.register_map('foret_E16', portals=[
            Portal(from_world='foret_E16', origin_point='exit_foret_E16', target_world='foret_A15',teleport_point='spawn_foret_E16'),
            Portal(from_world='foret_E16', origin_point='enter_foret_A17', target_world='foret_A17',teleport_point='spawn_foret_E16'),
            Portal(from_world='foret_E16', origin_point='dead_end', target_world='foret_A1',teleport_point='spawn_foret')
        ])
        self.register_map('foret_E18', portals=[
            Portal(from_world='foret_E18', origin_point='exit_foret_E18', target_world='foret_A17',teleport_point='spawn_foret_E18'),
            Portal(from_world='foret_E18', origin_point='enter_foret_B19', target_world='foret_B19',teleport_point='spawn_foret_E18'),
            Portal(from_world='foret_E18', origin_point='dead_end', target_world='foret_A1',teleport_point='spawn_foret')
        ])

        # déplacement du joueur à son point de départ (ou aux coordonnées enregistrées par la save), si il y a un fichier de sauvegarde
        if Save.Saved:
            self.player.position[0] = Save.dict_values["x_perso"]
            self.player.position[1] = Save.dict_values["y_perso"]
        else:       # Sinon envoyer le joueur à son point de spawn de base
            self.teleport_player("player_spawn")

        # placement PNJ
        self.teleport_npcs()

        # Utiliser pour les dialogues : checker si on peut obtimiser en définissant une méthodes pour avoir les PNJ et pas passer par les sprites

    def check_npc_collisions(self, dialog_box):         # Vérifier si on est en contact avec un sprite
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC:       # Si oui et que c'est un PNJ --> lancer la boîte de dialogue
                dialog_box.execute(sprite)

    def check_collisions(self):
        # portails
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:       # Définition du rectangle de collision du portail
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):      # Si on est en collision avec ce dernier, téléporter le joueur au point de spawn de la carte ciblée
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)

                    # perdre de la vie en passant par ce portail
                    if self.player.health - 10 > 10:
                        self.player.health -= 10
                    #else:
                        # si le joueur n'a plus de vie


        # verifier les collisions
        for sprite in self.get_group().sprites():
            if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):       # Si on rentre en collision avec un objet, le joueur ne peut plus avancer
                    sprite.speed = 0
                else:
                    sprite.speed = sprite.stats['speed']

            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()
    def teleport_player(self, name):        # Cherche les coordonnées x et y du point de spawn du joueur
        point = self.get_object(name)
        self.player.position[0] = point.x - 15
        self.player.position[1] = point.y - 20
        self.player.save_location()
    def register_map(self, name, portals=[], npcs=[]):

        tmx_data = pytmx.util_pygame.load_pygame(f'../map/{name}.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2
        # Charger la carte et l'afficher sur l'écran avec un zoom spécifique
        walls = []

        for obj in tmx_data.objects:
            if obj.type == 'collision':         # Si le type de l'objet est collision, alors ajouter ce dernier à la liste de "murs"
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=0)        # Définition du calque d'origine sur lequel est placer le joueur
        group.add(self.player)

        # récupérer tous les NPC pour les ajouter au groupe

        for npc in npcs:
            group.add(npc)

        # créer un objet map
        self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs)

    def get_map(self):          # On "prend"  la carte actuelle
        return self.maps[self.current_map]

    def get_group(self):        # On "prend" le groupe de quelque chose de spécifique
        return self.get_map().group

    def get_walls(self):        # On "prend" les murs (objets avec des collisions)
        return self.get_map().walls

    def get_object(self, name):        # On "prend" les objets dont on a besoin
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

