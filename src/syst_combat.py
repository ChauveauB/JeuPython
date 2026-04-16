import random
import pygame, math
from random import *
from time import sleep
from inventory import Inventory
from input_player import get_input

class Personnage: # classe de creation des personnages, monstres y compris
    def __init__(self, player, ennemi, screen, name): # initialisation des parametres du monstre
        self.inventaire = Inventory(player)
        self.player = player
        self.ennemi = ennemi
        self.screen = screen
        self.stats_base = {"player": self.player.stats, "ennemi": self.ennemi.stats_base}        #stats arbitraires
        self.player_PV_max = self.stats_base["player"]["PV max"]
        self.player_PV = self.stats_base["player"]["PV"]
        self.ennemi_PV_max = self.stats_base["ennemi"][name]["PV max"]
        self.ennemi_PV = self.stats_base["ennemi"][name]["PV"]



    def est_vivant(self, cible, name): #verifie si un personnage ciblé est vivant --> Booléen
        if cible == "ennemi":
            return self.ennemi_PV > 0
        else:
            return self.player_PV > 0

    def attaquer(self, cible, name): #calcul des degats
        if cible == "ennemi":
            base_degats = self.stats_base["player"]["Attaque"]
            degats = base_degats + randint(-2, 2)
            self.ennemi_PV -= degats
            print(f"L'{cible} a {self.ennemi_PV} PV restant")
            self.update_health_bar(self.screen, cible, self.ennemi_PV)
        else:
            base_degats = self.stats_base["ennemi"][name]["Attaque"]
            degats = base_degats + randint(-2, 2)
            self.player_PV -= degats
            self.update_health_bar(self.screen, cible, self.player_PV)
            print(f"Le {cible} a {self.player_PV} PV restant")

    def soigner(self):  #Soigner le perso s'il possède des potions
        cible = "player"
        if "potion de vie" in self.inventaire.objets_possede and self.inventaire.objets_possede["potion de vie"] > 0:
            if self.player_PV + 40 >= self.player_PV_max:
                self.player_PV = self.player_PV_max
            else:
                self.player_PV += 40

            self.inventaire.objets_possede["potion de vie"] -= 1
            self.update_health_bar(self.screen, cible, self.player_PV)

            print(self.player_PV)
            print(self.inventaire.objets_possede["potion de vie"])

    def magie(self, cible, name):     #Attaque magique
        if self.stats_base["player"]["Mana"] - 3 > 0:
            self.stats_base["player"]["Mana"] -= 3
            self.update_mana_bar(self.screen)
            self.attaquer(cible, name)

    def update_health_bar(self, surface, cible, PV):
        # draw the bar
        if cible == "ennemi":
            PV_max = pygame.Rect(0, 0, self.ennemi_PV_max * 3, 10)
            PV_max.topright = (self.screen.get_width() - 230, 91)
            pygame.draw.rect(surface, (55, 55, 55), PV_max)

            PV_ennemi = pygame.Rect(0, 0, (PV) * 3, 10)
            PV_ennemi.topright = (self.screen.get_width() - 230, 91)
            pygame.draw.rect(surface, (174, 58, 46), PV_ennemi)
            """
            pygame.draw.rect(surface, (55, 55, 55), [150, 91, self.stats_base[cible][name]['PV max']*3, 11])
            pygame.draw.rect(surface, (175, 53, 41), [150, 91, self.stats_base[cible][name]['PV']*3, 10])"""
        else:
            pygame.draw.rect(surface, (55, 55, 55), [150, 91, self.player_PV_max * 3, 11])
            pygame.draw.rect(surface, (175, 53, 41), [150, 91, PV * 3, 10])

    def update_mana_bar(self, surface):
        pygame.draw.rect(surface, (55, 55, 55), [150, 102, self.stats_base["player"]['Mana max']*3, 11])
        pygame.draw.rect(surface, (32, 76, 145), [150, 102, self.stats_base["player"]['Mana']*3, 10])

class combat_logique: #controle du combat en arriere-plan
    def __init__(self, player):

        self.personnage = Personnage(player)

        self.player = Personnage(player)
        self.ennemi = Personnage(player)        # L'ennemi est une instance de la classe personnage ci-dessus
        self.en_cours = True            #Boucle du combat
        self.gagnant = None


    def lancer_tour (self, action_joueur, cible):      #toutes les actions qui peuvent se derouler pendant le combat
        if not self.personnage.est_vivant(self.ennemi):
            self.gagnant = self.player
            self.en_cours = False
        elif not self.personnage.est_vivant(self.player):
            self.gagnant = self.ennemi
            self.en_cours = False
        else:
            if action_joueur == "attaque":
                self.personnage.attaquer(cible)
            elif action_joueur == "magie":
                self.personnage.magie(cible)
            elif action_joueur == "soin":
                self.personnage.soigner()



    def run_combat(self):       #Boucle du combat
        while self.en_cours:
            #Tour player
            if self.personnage.est_vivant(self.player):
                action = get_input("que voulez vous faire (attaque/magie/soin) ?")     #Similaire à la méthode input, avec une interface pygame
                print("Tour joueur")
                print(action)
                self.lancer_tour(action, self.ennemi)

            #Tour ennemi
            if self.personnage.est_vivant(self.ennemi):
                action = choice(["attaque", "magie"])
                print("Tour ennemi")
                print(action)
                self.lancer_tour(action, self.player)

            if not self.personnage.est_vivant(self.player) or not self.personnage.est_vivant(self.ennemi):
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