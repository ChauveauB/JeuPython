import pygame
from player import Player
from dialog_menu import DialogMenu
from save import Save
from syst_combat import Combat
from random import *

class DialogBox:

    def __init__(self, player: Player, dialog_menu: DialogMenu):
        self.box = pygame.image.load('../dialog/dialog_box.png')
        self.box = pygame.transform.scale(self.box, (700, 100))

        self.screen = pygame.display.set_mode((1000, 700))

        self.player = player
        self.dialog_menu = dialog_menu

        self.texts : list[str]
        self.texts = []
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font('../dialog/dialog_font.ttf', 15)
        self.reading = False
        self.game_paused = False

        self.syst_combat = Combat()

        self.names = {}

    def execute(self, sprite):
        if self.reading:        # le dialogue est ouvert
            self.next_text(sprite)
        else:
            self.reading = True
            self.texts = sprite.dialog[:]
            self.text_index = 0



    def render(self, screen):
        if self.reading and self.texts[self.text_index] != "/menu_dialogue/":
            self.letter_index += 1

            if self.letter_index >= len(self.texts):
                self.letter_index = self.letter_index       # Les lettres apparaissent les unes après les autres

            height = self.screen.get_size()[1] * 0.65
            width = self.screen.get_size()[0] // 6
            screen.blit(self.box, (width, height))

            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (0, 0, 0))
            screen.blit(text, (width + 55, height + 10))

    def next_text(self, sprite):        # On passe au prochain texte du PNJ
            self.letter_index = 0
            if not self.dialog_menu.choising: 
                self.text_index += 1

                if self.text_index >= len(self.texts):
                    self.reading = False

                #Le programme cherche la réponse du joueur et à actionner ses concéquences
                elif sprite.dialog[self.text_index] == "*choix":
                    self.choice = ""
                    self.player.react_player(self.dialog_menu.answer, sprite, self)
                    self.texts[self.texts.index("/menu_dialogue/") + 1] = self.choice

                    Save.write_logs(f"Numero de réponse : {self.dialog_menu.answer}")
                    Save.write_logs(f"Choix : {self.choice}")
                    Save.write_logs(f"Les dialogues : {self.texts}")
                    Save.write_logs(f"Les dialogues du perso : {sprite.dialog}")

                # le programme vérifie si le menu de dialogue doit être affiché
                elif self.texts[self.text_index] == "/menu_dialogue/":
                    #Gérer quand le menu est ouvert et doit être fermé ou considéré que la joueur ait bien chosi une option
                    self.dialog_menu.choising = True
                    self.dialog_menu.wait = True

                elif self.texts[self.text_index] == "/combat/":
                    Save.write_logs(f"Les dialogues du perso qui entre en combat sont : {sprite.dialog}")
                    #Rajouter une variable aux entités pour que si on rentre en combat avec elles, elles nous renvoie une liste d'adversaire 
                    self.syst_combat.running = True
                    self.dialog_menu.wait = True

