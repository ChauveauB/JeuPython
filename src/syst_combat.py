import pygame
from random import *

class Combat:
    def __init__(self):
        self.ennemy_stat = {"1" : 1, "2" : 2}
        #premiers choix du joueur
        #nom des cases du menu

    def beginning(self):
        # génère un nombre aléatoire d'ennemis et leur attribue à chacun 100 PV
        ennemies = randint(1, 4)
        for i in range(ennemies):
            self.ennemy_stat[f"ennemy_{i + 1}"] = 100
