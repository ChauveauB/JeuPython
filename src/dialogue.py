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
        self.texts = []
        self.letter_index = 0
        self.font = pygame.font.Font('../dialog/dialog_font.ttf', 18)
        self.reading = False
        self.game_paused = False

    def execute(self, dialog=[]):
        if self.reading:        # le dialogue est ouvert
            self.next_text()
        else:
            self.reading = True
            if self.player.health <= 50:
                self.text_index = 1
            else:
                self.text_index = 0
            self.texts = dialog



    def render(self, screen):
        if self.reading:
            self.letter_index += 1

            if self.letter_index >= len(self.texts):
                self.letter_index = self.letter_index

            height = self.screen.get_size()[1] * 0.65
            width = self.screen.get_size()[0] // 6
            screen.blit(self.box, (width, height))
            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (0, 0, 0))
            screen.blit(text, (width + 55, height + 10))

    def next_text(self):
            self.text_index += 1
            self.letter_index = 0

            # le programme vérifie si le dialogue n'est pas autre chose que du texte
            if self.texts[self.text_index] is not str :
                self.reading = False
                # appel du menu dialogue qui disparaît tout de suite
                self.dialog_menu.display()

            if self.text_index >= len(self.texts):
               # fermer dialogue
                self.reading = False
