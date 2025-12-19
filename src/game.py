import math, pygame, pyscroll, pytmx

from player import Player
from map import MapManager
from inventory import Inventory
from death_menu import Death_menu
from dialogue import DialogBox
from dialog_menu import DialogMenu
from save import Save
from syst_combat import combat_logique
from random import *

class Game:

    def __init__(self):
        #Début de la défénition des caractéristiques
        self.display_surface = pygame.display.get_surface()

        # créer la fenetre
        self.screen = pygame.display.set_mode((500, 500), pygame.FULLSCREEN)  # surface (hauteur, largeur)
        pygame.display.set_caption("Jeu Python")    # titre de la fenêtre

        self.running = False
        self.game_paused = False
        self.game_end = False

        # importer et charger les images de l'écran titre
        self.background = pygame.image.load("../others/red_background.jpg")

        self.banner = pygame.image.load("../others/banner.png")
        self.banner = pygame.transform.scale(self.banner, (500, 500))
        self.banner_rect = self.banner.get_rect()
        self.banner_rect.x = math.ceil(self.screen.get_width() / 4)     # l'utilisation du module math permet d'éviter un chiffre a virgule et d'arrondir à l'entier suivant

        self.play_button = pygame.image.load("../others/button.png")
        self.play_button = pygame.transform.scale(self.play_button, (400, 150))
        self.play_button_rect = self.play_button.get_rect()
        self.play_button_rect.x = math.ceil(self.screen.get_width() / 3.33)
        self.play_button_rect.y = math.ceil(self.screen.get_height() / 2)

        self.reset_button = pygame.image.load("../others/comet.png")
        self.reset_button_rect = self.reset_button.get_rect()


        # générer un joueur
        self.player = Player()
        #self.map_manager = MapManager(self.screen, self.player)
        self.dialog_menu = DialogMenu(self.player, len(self.player.player_choice), -5500, 350)
        self.dialog_box = DialogBox(self.player, self.dialog_menu)

        # inventaire
        self.inventory = Inventory(self.player)
        self.syst_combat = combat_logique(self.player)
        self.death = Death_menu(self.player)

        #if self.player.stats["health"] <= 0:
        #    self.game_over()

    def handle_input(self):                         # déplacement du joueur avec les flèches du clavier
        pressed = pygame.key.get_pressed()

        # quitter le jeu avec échap
        if pressed[pygame.K_ESCAPE]:
            self.running = False

        if self.dialog_box.reading:
            pass
        else:
            # déplacer le perso avec les flèches
            if pressed[pygame.K_UP]:
                self.player.move_up()
            elif pressed[pygame.K_DOWN]:
                self.player.move_down()
            elif pressed[pygame.K_LEFT]:
                self.player.move_left()
            elif pressed[pygame.K_RIGHT]:
                self.player.move_right()

    def game_over(self):
        self.player.health = 100
        self.running = False

    def update(self):
        self.map_manager.update()
    def death_menu(self):
        self.game_end = not self.game_end

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def saver(self):
        with open("../saves/save_Python.txt", "w") as save_fic:
            save_fic.write("___SAUVEGARDE DU PROJET PYTHON___\n")
            Save.dict_values["x_perso"], Save.dict_values["y_perso"], Save.dict_values["speed_perso"], Save.dict_values["health_perso"], Save.dict_values["world_perso"] = self.player.position[0], self.player.position[1], self.player.speed, self.player.health, self.map_manager.current_map
            for key in Save.dict_values.keys():
                save_fic.write(f"{key}:{Save.dict_values[key]}\n")


    def run(self):
        # boucle du jeu

        if self.running:
            self.running_game()
        else:
            while not self.running:
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.play_button, self.play_button_rect)
                self.screen.blit(self.banner, self.banner_rect)
                self.screen.blit(self.reset_button, self.reset_button_rect)

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # vérification si la souris est en colision avec le bouton jouer
                        if self.play_button_rect.collidepoint(event.pos):   # event.pos = position de l'évènement citer dans la condition au-dessus
                            # lancer le jeu
                            self.running = True
                            self.running_game()
                        elif self.reset_button_rect.collidepoint(event.pos):
                            with open("../saves/logs.txt", "w") as logs:
                                logs.write(">>>>> LOGS DU JEU PYTHON <<<<<\n")

                            self.running = True
                            self.running_game()

    def running_game(self):
        clock = pygame.time.Clock()

        while self.running:

            pygame.display.flip()

            self.syst_combat.run_combat()


            if self.game_paused and not self.dialog_menu.choising:      # afficher l'inventaire
                self.inventory.display()
                self.player.update_health_bar(self.screen)

                
            elif self.dialog_menu.choising:
                self.dialog_menu.display(list(self.player.player_choice))
                if not self.dialog_menu.choising:
                    self.map_manager.check_npc_collisions(self.dialog_box)
                self.handle_input()

            else:
                self.player.save_location()
                self.handle_input()
                self.update()
                self.map_manager.draw()
                self.dialog_box.render(self.screen)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:           # quitter avec la croix du haut de la fenêtre
                    self.running = False

                # création d'un menu/inventaire

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:     # inventaire
                        self.toggle_menu()

                    if event.key == pygame.K_SPACE:     # dialogue avec un PNJ
                        self.map_manager.check_npc_collisions(self.dialog_box)

                    #sauvegarde
                    if event.key == pygame.K_x and not self.game_end:
                        Save.write_logs("Tentative de sauvegarde des infos")
                        self.saver()
                    
                    #Ajuster la taille en jeu (ptêtre trouver de meilleures touches)
                    if event.key == pygame.K_z:
                        self.screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h + 35))

                    if event.key == pygame.K_s and pygame.display.Info().current_h >= 535:
                        self.screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h - 35))

                    if event.key == pygame.K_q:
                        self.screen = pygame.display.set_mode((pygame.display.Info().current_w + 50, pygame.display.Info().current_h))

                    if event.key == pygame.K_d and pygame.display.Info().current_w >= 850:                   
                        self.screen = pygame.display.set_mode((pygame.display.Info().current_w - 50, pygame.display.Info().current_h))
                        
                if self.player.stats['health'] <= 0:        # fermeture du jeu quand le joueur n'a plus de vie
                    self.game_end = True

            if self.game_end:
                self.death.display()

            clock.tick(60)

        pygame.quit()
