import pygame
from player import Player

class DialogMenu:
    def __init__(self, player):

        # general setup
        self.screen = pygame.display.set_mode((1000, 800))
        self.player = player

        # initialisation des valeurs (nr -> nombres de réponses du joueur)
        self.attribute_nr = len(player.player_answers)
        self.attribute_names = list(player.player_answers.keys())
        self.attribute_values = list(player.player_answers.values())

        self.font = pygame.font.Font('../dialog/dialog_font.ttf', 18)

        # item creation, taille des carrés
        self.height = self.screen.get_size()[1] * 0.065
        self.width = self.screen.get_size()[0] // 6.5
        self.create_items()

        # selection system
        self.answer = None
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True
        self.choising = False


    def input(self):
        #Pour la sélection des réponses du joueur 
        keys = pygame.key.get_pressed()
        if not keys[pygame.K_SPACE]:
            self.wait = False
        

        if self.can_move:
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_nr - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_SPACE] and not self.wait:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.answer = self.selection_index
                self.choising = False


    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True

    def create_items(self):
        self.item_list = []

        for item, index in enumerate(range(self.attribute_nr)):
            # horizontal position, position X du carré
            full_width = self.screen.get_size()[0]
            increment = full_width // 6
            left = (item * increment) + (increment - self.width) // 2 + 205

            # vertical position, position Y du carré
            top = self.screen.get_size()[1] * 0.615

            # create object
            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)
    
    def display(self):
        self.input()
        self.selection_cooldown()
        #self.display_stats()

        for index, item in enumerate(self.item_list):

            # get attributes

            name = self.attribute_names[index]

            value = self.player.get_value_by_index(index)

            item.display(self.screen, self.selection_index, name, value)


class Item:
    def __init__(self, l, t, w, h, index, font):
        self.rect = pygame.Rect(l, t, w, h)
        self.index = index
        self.font = font

        # color
        self.BG_COLOR = '#222222'
        self.TEXT_COLOR = '#EEEEEE'
        self.TEXT_COLOR_SELECTED = '#111111'
        self.BG_COLOR_SELECTED = '#F8F8F8'

    def display_names(self, surface, name, value, selected):
        color = self.TEXT_COLOR if selected else self.TEXT_COLOR_SELECTED       # Change la couleur quand une case est sélectionnée

        # title text
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0, 20))

        # draw
        surface.blit(title_surf, title_rect)

    def display(self, surface, selection_num, name, value):

            if self.index == selection_num:
                pygame.draw.rect(surface, self.BG_COLOR, self.rect)
            else:
                pygame.draw.rect(surface, self.BG_COLOR_SELECTED, self.rect)
            self.display_names(surface, name, value, self.index == selection_num)

            # appel de cette fonction display avant celle au dessus
            # essayer de trouver le code pour inverser l'appel de ces fonctions
