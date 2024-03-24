import time

import pygame
from player import Player
from map import MapManager
from inventory import Inventory
from death_menu import Death_menu


class Game:

    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.running = True
        self.map = "world"

        # créer la fenetre
        self.screen = pygame.display.set_mode((1000, 700))
        pygame.display.set_caption("Jeupython")
        self.game_paused = False
        self.game_end = False

        # générer un joueur

        self.player = Player()
        self.map_manager = MapManager(self.screen, self.player)

        # inventaire
        self.inventory = Inventory(self.player)

        self.death = Death_menu(self.player)

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        # quitter le jeu avec échap
        if pressed[pygame.K_ESCAPE]:
            self.running = False

        # déplacer le perso avec les flèches
        elif pressed[pygame.K_UP]:
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

    def run(self):

        clock = pygame.time.Clock()

        # boucle du jeu

        self.running = True

        while self.running:

            pygame.display.flip()
            if self.game_paused:
                self.inventory.display()
                self.player.update_health_bar(self.screen)
                # afficher le menu
            else:
                self.player.save_location()
                self.handle_input()
                self.update()
                self.map_manager.draw()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # création d'un menu/inventaire
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.toggle_menu()

                if self.player.stats['health'] == 0:
                    self.game_end = True

            if self.game_end:
                self.death.display()

            clock.tick(60)

        pygame.quit()
