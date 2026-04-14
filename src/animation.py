import pygame


class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, name):
        super().__init__()
        self.sprite_sheet = pygame.image.load(f"../sprites/{name}.png")
        self.animation_index = 0
        self.clock = 0
        self.images = {
            'images32' : {
                "down": self.get_images(32, 0),
                "right": self.get_images(32, 32),
                "up": self.get_images(32, 64),  # Charge les images en fonction de la direction du joueur
                "left": self.get_images(32, 96)
            },
            "images64" : {
                "down": self.get_images(64, 0),
                "right": self.get_images(64, 64),
                "up": self.get_images(64, 128),  # Charge les images en fonction de la direction du joueur
                "left": self.get_images(64, 192),
        }}
        self.speed = 10  # Cette ligne semble inutile car les vitesses sont spécifiées à chaque PNJ

    def change_animation(self, taille, name):
        self.image = self.images[taille][name][self.animation_index]
        self.image.set_colorkey((0, 0, 0))
        self.clock += self.speed * 8

        if self.clock >= 100:

            self.animation_index += 1  # passer à l'image suivante

            if self.animation_index >= len(self.images[taille][name]):
                self.animation_index = 0        # Si on dépasse le nombre d'images définies, on revient à la première

            self.clock = 0

    def get_images(self, taille, y):
        images = []

        for i in range(0, 8):
            x = i * taille
            image = self.get_image(x, y, taille)
            images.append(image)

        return images

    def get_image(self, x, y, taille):
        image = pygame.Surface([taille, taille])
        image.blit(self.sprite_sheet, (0, 0), (x, y, taille, taille))
        return image
