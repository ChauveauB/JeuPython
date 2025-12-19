#coding:utf-8
import pygame, time
from save import Save
from game import Game
from syst_combat import combat_logique

Save.write_logs(f"Lancement du programme du {time.strftime("jour %Y-%m-%d à %H:%M:%S", time.localtime())}")
Save.get_save()

if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()