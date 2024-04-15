import pygame

class Death_menu:
    def __init__(self, player):
        self.screen = pygame.display.set_mode((1000, 700))
        self.player = player

        self.font = pygame.font.Font('../dialogue/font.ttf', 100)

    def display(self):
        self.screen.fill('black')
        death = self.font.render('Game Over', 1, 'red')
        self.screen.blit(death, (110, 300))