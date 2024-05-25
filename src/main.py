#coding:utf-8
import pygame, time

from game import Game

with open("../saves/logs.txt", "a") as logs:
    logs.write(f"Lancement du programme du {time.strftime("jour: %Y-%m-%d a %H:%M:%S", time.localtime())}\n")

if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()