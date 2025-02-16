import pygame
from player import Player, Entity

class Combat:
    player : Player
    ennemies : list[Entity]
    nb_ennemies : int
    fighting = False


    @classmethod
    def start(cls, player:Player, ennemies:list[Entity]):
        Combat.fighting = True
        Combat.player = player
        Combat.ennemies = ennemies
        Combat.nb_ennemies = len(Combat.ennemies)

    @staticmethod
    def display(screen : pygame.Surface):
        h = screen.get_rect().h
        w = screen.get_rect().w
        h_ent = h/500 * 32
        w_ent = w/800 * 32

        #Mettre le fond de combat: >>>>juste faire en sorte que les tailles des blit soient adptables<<<<<
        fond = pygame.image.load("../others/fond_blanc.jpg")
        fond = pygame.transform.scale(fond, (h +300, w))
        screen.blit(fond, (0,0))

        Combat.load_ent(screen, w, h, w_ent, h_ent)
        
    @staticmethod
    def load_ent(screen, w, h, w_ent, h_ent):
        #Charger les différents personnages en combat
        player = Combat.player.images["right"][0]
        player = pygame.transform.scale(player, (64, 64))
        screen.blit(player, (w*1/6, h*1/3))
        for index in range(Combat.nb_ennemies):
            ennemy = Combat.ennemies[index].images["left"][0]
            ennemy = pygame.transform.scale(ennemy, (64, 64))
            screen.blit(ennemy, (w-w_ent-20 if index%2==0 else w-2*w_ent-30, (index+1)*2/15*h))

    @classmethod
    def end():
        Combat.fighting = False