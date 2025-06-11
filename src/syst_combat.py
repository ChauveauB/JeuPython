import pygame, math
from random import *
from time import sleep

class Combat:
    def __init__(self):
        self.ennemy_stat = {"1" : 1, "2" : 2}
        self.screen = pygame.display.set_mode((1000, 800))
        self.attack_button = pygame.image.load('../image_combat/attack_button.png')
        self.attack_button_rect = self.attack_button.get_rect()
        self.attack_button_rect.x = math.ceil(self.screen.get_width() / 3.33)
        self.attack_button_rect.y = math.ceil(self.screen.get_height() / 2)

        self.magic_button = pygame.image.load('../image_combat/magic_button.png')
        self.magic_button_rect = self.magic_button.get_rect()
        self.magic_button_rect.x = math.ceil(self.screen.get_width() / 3.33)
        self.magic_button_rect.y = math.ceil(self.screen.get_height() / 2)
        self.running = False

    def beginning(self):
        # génère un nombre aléatoire d'ennemis et leur attribue à chacun 100 PV
        ennemies = randint(1, 4)
        for i in range(ennemies):
            self.ennemy_stat[f"ennemy_{i + 1}"] = 100

    def display(self):
        self.screen.fill('white')
        self.screen.blit(self.attack_button, self.attack_button_rect)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.attack_button_rect.collidepoint(event.pos):
                    self.screen.blit(self.magic_button, (0, 0))
                    self.screen.blit(self.magic_button, self.magic_button_rect)