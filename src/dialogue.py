import pygame

class DialogBox:

    def __init__(self):
        self.box = pygame.image.load('../dialog/dialog_box.png')
        self.box = pygame.transform.scale(self.box, (700, 100))

        self.screen = pygame.display.set_mode((1000, 700))

        self.texts = ['Salut', 'Bonne aventure !' 'a bientôt']
        self.text_index = 0
        self.font = pygame.font.Font('../dialog/dialog_font.ttf', 15)
        self.reading = True

    def render(self, screen):
        if self.reading:
            height = self.screen.get_size()[1] * 0.65
            width = self.screen.get_size()[0] // 6
            screen.blit(self.box, (width, height))
            text = self.font.render(self.texts[self.text_index], False, (0, 0, 0))
            screen.blit(text, (width + 55, height + 10))

    def next_text(self):
            self.text_index += 1

            if self.text_index >= len(self.texts):
                self.reading = False