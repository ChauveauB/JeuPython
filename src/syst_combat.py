import random
import pygame, math
from random import *
from time import sleep
from inventory import Inventory
from input_player import get_input

class Personnage: # classe de creation des personnages, monstres y compris
    def __init__(self, player): # initialisation des parametres du monstre
        self.inventaire = Inventory(player)
        self.stats_perso = {"PV max": 200, "PV": 200, "Attaque": 5, "Défense": 6, "Mana max": 15, "Mana": 15}

    def est_vivant(self, cible): #verifie si chaque personnage est vivant
       return cible.stats_perso["PV"] > 0

    def attaquer(self, cible): #calcul des degats
        base_degats = self.stats_perso["Attaque"]
        degats = max(0, base_degats - cible.stats_perso["PV"] + random.randint(-2, 2))
        cible.stats_perso["PV"] -= degats

    def soigner(self):
        if "potion de vie" in self.inventaire.objets_possede and self.inventaire.objets_possede["potion de vie"] > 0:
            if self.stats_perso["PV"] + 40 >= self.stats_perso["PV max"]:
                self.stats_perso["PV"] = self.stats_perso["PV max"]
            else:
                self.stats_perso["PV"] += 40

            self.inventaire.objets_possede["potion de vie"] -= 1

            print(self.stats_perso["PV"])
            print(self.inventaire.objets_possede["potion de vie"])

    def magie(self, cible):
        if self.stats_perso["Mana"] - 3 > 0:
            self.attaquer(cible)

class combat_logique: #controle du combat en arriere-plan
    def __init__(self, player, ennemi):

        self.personnage = Personnage(player)

        self.player = player
        self.ennemi = ennemi
        self.en_cours = True
        self.gagnant = None

    def lancer_tour (self, action_joueur) : #toutes les actions qui peuvent se derouler pendant le combat
        if action_joueur == "attaque":
            self.personnage.attaquer(self.ennemi)
        elif action_joueur == "magie":
            self.personnage.magie(self.ennemi)
        elif action_joueur == "soin":
            self.personnage.soigner()

        """if not self.personnage.est_vivant(self.ennemi):
            self.gagnant = self.player
            self.en_cours = False"""
    def reaction_joueur(self):
        pass

    def run_combat(self):
        if self.en_cours:
            reponse = get_input("que voulez vous faire (attaque/magie/soin) ?")
            self.lancer_tour(reponse)



class Combat: #interface accesible par le joueur lors du combat
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
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