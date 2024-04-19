import pygame
from animation import AnimateSprite


class Entity(AnimateSprite):

    def __init__(self, name, x, y, speed, health=3):
        super().__init__(name)

        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]

        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()

        # stats
        self.stats = {"health": health, "attack": 10, "defense": 10, "speed": speed}
        self.health = self.stats["health"]
        self.max_health = 200
        self.speed = self.stats["speed"]

    # affichage d'une barre de vie
    def update_health_bar(self, surface):
        # draw the bar
        pygame.draw.rect(surface, (55, 55, 55), [10, 10, self.max_health, 10])
        pygame.draw.rect(surface, (255, 0, 0), [10, 10, self.stats['health'], 10])

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def save_location(self):
        self.old_position = self.position.copy()

    def move_right(self):
        self.change_animation("right")
        self.position[0] += self.speed

    def move_left(self):
        self.change_animation("left")
        self.position[0] -= self.speed

    def move_up(self):
        self.change_animation("up")
        self.position[1] -= self.speed

    def move_down(self):
        self.change_animation("down")
        self.position[1] += self.speed

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom


class Player(Entity):

    def __init__(self):
        super().__init__("player", 0, 0, 3, 95)


class NPC(Entity):

    def __init__(self, name, nb_points, speed, dialog):
        super().__init__(name, 0, 0, speed)
        # récupère la vitesse grace a la class entity
        self.dialog = dialog
        self.nb_points = nb_points
        self.points = []
        self.name = name

        self.current_point = 0

    def move(self):
        current_point = self.current_point
        target_point = self.current_point + 1

        if target_point >= self.nb_points:
            target_point = 0

        current_rect = self.points[current_point]
        target_rect = self.points[target_point]

        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_down()
        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_up()

        elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_left()

        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_right()

        if self.rect.colliderect(target_rect):
            self.current_point = target_point

    # envoyer au point prévu de départ
    def teleport_spawn(self):
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def load_points(self, tmx_data):
        for num in range(1, self.nb_points + 1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)
