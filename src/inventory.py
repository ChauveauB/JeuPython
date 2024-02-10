import pygame

class Inventory:
    def __init__(self, player):

        # general setup
        self.screen = pygame.display.set_mode((1000, 800))
        self.player = player

    def display(self):
        self.screen.fill('black')