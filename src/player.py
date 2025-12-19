import pygame
from animation import AnimateSprite
from save import Save
from random import randint
from syst_combat import Combat


class Entity(AnimateSprite):

    def __init__(self, name, x, y, speed, health=3):
        super().__init__(name)

        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]

        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()

        # stats
        self.stats = {"health": health,
                      "attack": 10,
                      "defense": 10,
                      "speed": speed
                      }
        self.health = self.stats["health"]
        self.max_health = 200
        self.speed = self.stats["speed"]
        self.can_move = True

        self.ennemies = randint(1, 3)
        self.combat = Combat()


    # affichage d'une barre de vie
    def update_health_bar(self, surface):
        # draw the bar
        pygame.draw.rect(surface, (55, 55, 55), [10, 10, self.max_health, 10])
        pygame.draw.rect(surface, (255, 0, 0), [10, 10, self.stats['health'], 10])

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def save_location(self):        # Pour y revenir quand on entre en collision avec un objet/mur
        self.old_position = self.position.copy()

    def move_right(self):
        if self.can_move:
            self.change_animation("right")
            self.position[0] += self.speed

    def move_left(self):
        if self.can_move:
            self.change_animation("left")
            self.position[0] -= self.speed

    def move_up(self):
        if self.can_move:
            self.change_animation("up")
            self.position[1] -= self.speed

    def move_down(self):
        if self.can_move:
            self.change_animation("down")
            self.position[1] += self.speed

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):        # Recule le joueur quand il est en collision
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom


class Player(Entity):
    def __init__(self):
        self.speed_base = 3
        self.health_base = 100
        self.npc_answers = {"cable hdmi": {"Oui": 0, "Non": 1}, "paul": {"Quête": 0, "Au revoir": 1}, "robin": {"Combat": 0, "Fuite": 1}}
        self.player_choice = {}
        self.fighting = False
        self.cable_hdmi = False


        if Save.Saved:      # Location du joueur en début de partie si on a une sauvegarde
            x = Save.dict_values["x_perso"]
            y = Save.dict_values["y_perso"]
            speed = Save.dict_values["speed_perso"]
            health = Save.dict_values["health_perso"]
        else:
            x = 0
            y = 0
            speed = self.speed_base
            health = self.health_base
        super().__init__("player", x, y, speed, health)

    def react_player(self, answer, npc, dialoguer):
        if npc.name == "cable hdmi":
            self.cable_hdmi = True
            #if self.cable_hdmi:
            #    npc.position[0] += 1000


        elif npc.name == "paul":
            if answer == 0:
                if not self.cable_hdmi:
                    dialoguer.choice = "J'aimerais te confier une quête. Trouve moi un cable HDMI."
                else:
                    dialoguer.choice = "Merci beaucoup"
            else:
                dialoguer.choice = "Au revoir"


        elif npc.name == "robin":
            if answer == 0:
                self.player_choice = {"ennemy_1": 0, "ennemy_2": 1, "ennemy_3": 2}
                dialoguer.choice = "attaque"
                print(self.player_choice)
            elif answer == 1:
                print(1)
                dialoguer.choice = "inventaire"
            elif answer == 2:
                print(2)
                dialoguer.choice = "fuite"



class NPC(Entity):

    def __init__(self, name, nb_points, speed, dialog):
        super().__init__(name, 0, 0, speed)
        # récupère la vitesse grace a la class entity
        self.dialog = dialog
        self.nb_points = nb_points
        self.points = []
        self.name = name
        self.player = Player()

        self.current_point = 0


    def dialogue_answers(self):
        if self.name == "cable hdmi":
            self.player.player_choice = self.player.npc_answers["cable hdmi"]
        elif self.name == "paul":
            self.player.player_choice = self.player.npc_answers["paul"]
        elif self.name == "robin":
            self.player.player_choice = self.player.npc_answers["robin"]

    def move(self):
        current_point = self.current_point
        target_point = self.current_point + 1       # Passe au point suivant

        if target_point >= self.nb_points:
            target_point = 0

        current_rect = self.points[current_point]
        target_rect = self.points[target_point]

        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_down()
        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_up()

        elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_left()

        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_right()

        if self.rect.colliderect(target_rect):
            self.current_point = target_point

    # envoyer au point prévu de départ
    def teleport_spawn(self):       # Téléporte le PNJ à son point de spawn
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def load_points(self, tmx_data):        # Charge les points où passe les PNJ
        for num in range(1, self.nb_points + 1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)
