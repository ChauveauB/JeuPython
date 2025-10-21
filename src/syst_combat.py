import random
import pygame, math
from random import *
from time import sleep

class Personnage: # classe de creation des personnages, monstres y compris
    def __init__(self, nom, pv_max, attaque, defense, mana_max): # initialisation des parametres du monstre
        self.nom = nom
        self.pv_max = pv_max
        self.pv = pv_max
        self.attaque = attaque
        self.defense = defense
        self.mana_max = mana_max
        self.mana = mana_max

    def est_vivant (self) : #verifie si chaque personnage est vivant
       return self.pv > 0

    def attaquer (self, cible) : #calcul des degats
        base_degats = self.attaque
        degats = max(0, base_degats - cible.pv + random.randint(-2, 2))
        cible.pv -= degats

class combat_logique : #controle du combat en arriere-plan
    def __init__(self, joueur, ennemi):
        self.joueur = joueur
        self.ennemi =ennemi
        self.en_cours = True
        self.gagnant = None

    def lancer_tour (self, action_joueur) : #toutes les actions qui peuvent se derouler pendant le combat
        if action_joueur == "attack" :
            self.joueur.attaquer(self.ennemi)
        elif action_joueur == "magic" :
            self.joueur.magie(self.ennemi)

        if not self.ennemi.est_vivant :
            self.gagnant = self.joueur
            self.en_cours = False

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