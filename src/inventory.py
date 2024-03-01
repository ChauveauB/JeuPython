import pygame

class Inventory:
    def __init__(self, player):

        # general setup
        self.screen = pygame.display.set_mode((1000, 800))
        self.player = player

        # initialisation des valeurs
        self.attribute_nr = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.attribute_values = list(player.stats.values())

        self.font = pygame.font.Font('../joystix.ttf', 18)

        # item creation
        self.height = self.screen.get_size()[1] * 0.25
        self.width = self.screen.get_size()[0] // 5
        self.create_items()

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
        self.item_list = []

        for item, index in enumerate(range(self.attribute_nr)):
            # horizontal position
            full_width = self.screen.get_size()[0]
            increment = full_width // self.attribute_nr
            left = (item * increment) + (increment - self.width) // 2

            # vertical position
            top = self.screen.get_size()[1] * 0.05

            # create object
            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)

    def display(self):
        self.screen.fill('black')
        self.input()
        self.selection_cooldown()

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
        self.BG_COLOR_SELECTED = '#EEEEEE'

    def display_names(self, surface, name, value, selected):
        color = self.TEXT_COLOR_SELECTED if selected else self.TEXT_COLOR

        # title text
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0, 20))

        # stats value
        value_surf = self.font.render(f'{int(value)}', False, color)
        value_rect = value_surf.get_rect(midbottom=self.rect.midbottom - pygame.math.Vector2(0, 20))

        # draw
        surface.blit(title_surf, title_rect)
        surface.blit(value_surf, value_rect)

    def display(self, surface, selection_num, name, value):
        if self.index == selection_num:
            pygame.draw.rect(surface, self.BG_COLOR_SELECTED, self.rect)
        else:
            pygame.draw.rect(surface, self.BG_COLOR, self.rect)
        self.display_names(surface, name, value, self.index == selection_num)