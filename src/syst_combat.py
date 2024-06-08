import pygame
from player import Player, Entity

class Combat:
    player : Player
    ennemies : list[Entity]
    nb_ennemies : int
    fighting = False

    @staticmethod
    def display(screen : pygame.Surface):
        h = screen.get_rect().h
        w = screen.get_rect().w
        h_ent = h/500 * 32
        w_ent = w/800 * 32

        #Mettre le fond de combat
        fond = pygame.image.load("../others/fond_blanc.jpg")
        screen.blit(fond, (0,0))

        #Charger les différents personnages en combat
        screen.blit(Combat.player.images["right"][0], (w*1/6, h*1/3))
        for index in range(Combat.nb_ennemies):
            screen.blit(Combat.ennemies[index].images["left"][0], (w-w_ent-20 if index%2==0 else w-2*w_ent-30, (index+1)*2/15*h))

    @classmethod
    def start(cls, player:Player, ennemies:list[Entity]):
        Combat.fighting = True
        Combat.player = player
        Combat.ennemies = ennemies
        Combat.nb_ennemies = len(Combat.ennemies)

    @classmethod
    def end():
        Combat.fighting = False