import pygame
from save import Save

class Death_menu:
    def __init__(self, player):
        self.screen = pygame.display.set_mode((1000, 700))
        self.player = player

        self.font = pygame.font.Font('../dialog/dialog_font.ttf', 100)

    def display(self):
        Save.write_logs("Le joueur est mort : partie terminée")
        self.screen.fill('black')
        death = self.font.render('Game Over', 1, 'red')
        self.screen.blit(death, (110, 300))

        # Ecran Game Over