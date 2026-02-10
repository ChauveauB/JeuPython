from syst_combat import combat_logique
from animation import AnimateSprite
import pygame

class combatscreen :

    def __init__(self, screen):
        self.screen = screen
        #on definit les sprites de chaque element de l'ecran de combat
        self.atk_button_img = pygame.image.load('../image_combat/attack_button.png')
        self.inv_button_img = pygame.image.load('../image_combat/inventory_button.png')
        self.mgc_button_img = pygame.image.load('../image_combat/magic_button.png')

        self.player_lifebar_img = pygame.image.load('../image_combat/vie_player.png')
        self.ennemy_lifebar_img = pygame.image.load('../image_combat/vie_ennemi.png')

        self.blob_img = pygame.image.load("../image_ennemi/Blob_peinture1.png")
        on_screen_blob_size = (self.blob_img.get_width() * 5, self.blob_img.get_height() * 5)
        self.blob_img = pygame.transform.scale(self.blob_img, on_screen_blob_size)

        #on s'occupe de l'affichage du personnage
        self.animate_sprite = AnimateSprite("player")
        self.player_img = self.animate_sprite.get_image(0, 64)
        on_screen_player = (self.player_img.get_width() * 5, self.player_img.get_height() * 5)
        self.player_img = pygame.transform.scale(self.player_img, on_screen_player)
        self.player_img.set_colorkey((0, 0, 0))


        #on definit la taille des barres de vie pour qu'elles ne soient pas trop grosses
        on_screen_lifebar_size = (int(self.player_lifebar_img.get_width() * 0.4), int(self.player_lifebar_img.get_height()*0.4))
        self.player_lifebar_img = pygame.transform.scale(self.player_lifebar_img, on_screen_lifebar_size)
        self.ennemy_lifebar_img = pygame.transform.scale(self.ennemy_lifebar_img, on_screen_lifebar_size)


        #on definit les positions de chaque boutton d'action
        self.atk_button_pos = (850, 600)
        self.inv_button_pos = (100, 600)
        self.mgc_button_pos = (1050, 600)


        #on definit les positions des barres de vie
        self.player_lifebar_pos = (100, 50)
        self.ennemy_lifebar_pos = (800, 50)

        self.player_pos = (200, 300)
        self.blob_pos = (900, 200)


        #on definit les hitbox des bouttons pour permettre le clic
        self.atk_rect = self.atk_button_img.get_rect(topleft = self.atk_button_pos)
        self.mgc_rect = self.mgc_button_img.get_rect(topleft = self.mgc_button_pos)
        self.inv_rect = self.inv_button_img.get_rect(topleft = self.inv_button_pos)


    def draw_fight_screen (self) :
        #on rempli le fond pour cacher la carte
        self.screen.fill((50, 50, 50))

        #on dessine les elements de l'ecran
        self.screen.blit(self.atk_button_img, self.atk_button_pos)
        self.screen.blit(self.inv_button_img, self.inv_button_pos)
        self.screen.blit(self.mgc_button_img, self.mgc_button_pos)

        self.screen.blit(self.player_lifebar_img, self.player_lifebar_pos)
        self.screen.blit(self.ennemy_lifebar_img, self.ennemy_lifebar_pos)

        self.screen.blit(self.player_img, self.player_pos)
        self.screen.blit(self.blob_img, self.blob_pos)

#ce qui suit n'est la que pour tester, il faudra le supprimer pour l'inclure correctement dans le jeu
pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN) # Crée la fenêtre
ui = combatscreen(screen)

while True: # Boucle infinie simple
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN :
            if event.button == 1 and combatscreen.atk_rect.collidepoint(event.pos) :
                combat_logique.lancer_tour('attaque', )



    ui.draw_fight_screen()
    pygame.display.flip()
