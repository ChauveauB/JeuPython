import pygame

class Inventory:
    def __init__(self, player):

        # general setup
        self.screen = pygame.display.set_mode((1000, 800))
        self.player = player
        self.attribute_nr = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.font = pygame.font.Font('../joystix.ttf', 18)

        # item dimensions
        self.height = self.screen.get_size()[1] * 0.5
        self.width = self.screen.get_size()[0] // 6

        # selection system
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_nr - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_UP]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                print(self.selection_index)
            elif keys[pygame.K_DOWN]:
                pass

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True

    def create_items(self):
        pass

    def display(self):
        self.screen.fill('black')
        self.input()
        self.selection_cooldown()