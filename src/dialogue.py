import pygame
from player import Player
from dialog_menu import DialogMenu

class DialogBox:

    def __init__(self):
        self.box = pygame.image.load('../dialog/dialog_box.png')
        self.box = pygame.transform.scale(self.box, (700, 100))

        self.screen = pygame.display.set_mode((1000, 700))

        self.player = Player()
        self.dialog_menu = DialogMenu(self.player)

        self.texts : list[str]
        self.texts = []
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font('../dialog/dialog_font.ttf', 18)
        self.reading = False
        self.game_paused = False
        #Si le joueur est en train de choisir une réponse dans les dialogues
        self.choising = False

    def execute(self, dialog=[]):
        if self.reading:        # le dialogue est ouvert
            self.next_text()
        else:
            self.reading = True
            self.texts = dialog
            self.text_index = 0



    def render(self, screen):
        if self.reading and self.texts[self.text_index] != "/menu_dialogue/":
            self.letter_index += 1

            if self.letter_index >= len(self.texts):
                self.letter_index = self.letter_index

            height = self.screen.get_size()[1] * 0.65
            width = self.screen.get_size()[0] // 6
            screen.blit(self.box, (width, height))

            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (0, 0, 0))
            screen.blit(text, (width + 55, height + 10))

    def next_text(self):
            self.letter_index = 0
            if not self.choising: self.text_index += 1

            if self.text_index >= len(self.texts):
               # fermer dialogue
                self.reading = False

            # le programme vérifie si le menu de dialogue doit être affiché
            elif self.texts[self.text_index] == "/menu_dialogue/" :
                # appel du menu dialogue qui disparaît tout de suite
                self.choising = True
