import time

import pygame
from player import Player
from map import MapManager
from inventory import Inventory
from death_menu import Death_menu
from dialogue import DialogBox
from dialog_menu import DialogMenu
from save import Save

class Game:

    def __init__(self):
        self.save = Save()

        #Début de la défénition des caractéristiques
        self.display_surface = pygame.display.get_surface()
        self.running = True

        # créer la fenetre
        self.screen = pygame.display.set_mode((1000, 700))
        pygame.display.set_caption("Jeupython")
        self.game_paused = False
        self.game_end = False

        # générer un joueur
        self.player = Player()
        self.map_manager = MapManager(self.screen, self.player)
        self.dialog_box = DialogBox()
        self.dialog_menu = DialogMenu(self.player)

        # inventaire
        self.inventory = Inventory(self.player)

        self.death = Death_menu(self.player)




    def handle_input(self):
        pressed = pygame.key.get_pressed()

        # quitter le jeu avec échap
        if pressed[pygame.K_ESCAPE]:
            self.running = False

        if self.dialog_box.reading == True:
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

    def update(self):
        self.map_manager.update()

    def death_menu(self):
        self.game_end = not self.game_end

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def saver(self):
        self.save_fic = open('../saves/save_Pythonjeu.txt', "w")
        self.save_fic.write("___SAUVEGARDE DU PROJET PYTHON___\n")
        self.save_fic.write(f"{self.player.position[0]}\n{self.player.position[1]}\n{self.player.speed}\n{self.player.health}\n{self.map_manager.current_map}")
        self.save_fic.close

    def run(self):

        clock = pygame.time.Clock()

        # boucle du jeu

        self.running = True

        while self.running:

            pygame.display.flip()
            if self.game_paused:
                self.inventory.display()
                #self.player.update_health_bar(self.screen)
                # afficher le menu
            elif self.dialog_box.choising:
                self.dialog_box.dialog_menu.display()
                self.handle_input()
            else:
                self.player.save_location()
                self.handle_input()
                self.update()
                self.map_manager.draw()
                self.dialog_box.render(self.screen)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # création d'un menu/inventaire

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.toggle_menu()

                    if event.key == pygame.K_SPACE:
                        self.map_manager.check_npc_collisions(self.dialog_box)

                    #Ajuster la taille en jeu (ptêtre trouver de meilleures touches)
                    if event.key == pygame.K_z:
                        self.screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h + 35))

                    if event.key == pygame.K_s:
                        self.screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h - 35))

                    if event.key == pygame.K_q:
                        self.screen = pygame.display.set_mode((pygame.display.Info().current_w + 50, pygame.display.Info().current_h))

                    if event.key == pygame.K_d:                   
                        self.screen = pygame.display.set_mode((pygame.display.Info().current_w - 50, pygame.display.Info().current_h))

                    if event.key == pygame.K_x:
                        #Logs et sauvegarde
                        with open("../saves/logs.txt", "a") as logs:
                            logs.write(f"Tentative de sauvegarde des infos en remplacant par x:{self.player.position[0]}, y:{self.player.position[1]}, speed:{self.player.speed}, health:{self.player.health} et monde:{self.map_manager.current_map}\n")
                        self.saver()
                        
                if self.player.stats['health'] <= 0:
                    self.game_end = True

            if self.game_end:
                self.death.display()

            clock.tick(60)

        pygame.quit()
