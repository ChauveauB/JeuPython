from syst_combat import Personnage
import pygame

class combatscreen :

    def __init__(self, screen):
        self.screen = screen
        #on definit les sprites de chaque element de l'ecran de combat
        self.atk_button_img = pygame.image.load('../image_combat/attack_button.png')
        self.inv_button_img = pygame.image.load('../image_combat/inventory_button.png')
        self.mgc_button_img = pygame.image.load('../image_combat/magic_button.png')

        self.my_lifebar_imb = pygame.image.load(('../image_combat/'))

        #on definit les positions de chaque boutton d'action
        self.atk_button_pos = (850, 600)
        self.inv_button_pos = (100, 600)
        self.mgc_button_pos = (1050, 600)

    def draw_fight_screen (self) :
        #on rempli le fond pour cacher la carte
        self.screen.fill((50, 50, 50))


        self.screen.blit(self.atk_button_img, self.atk_button_pos)
        self.screen.blit(self.inv_button_img, self.inv_button_pos)
        self.screen.blit(self.mgc_button_img, self.mgc_button_pos)

#ce qui suit n'est la que pour tester, il faudra le supprimer pour l'inclure correctement dasn le jeu
pygame.init()
screen = pygame.display.set_mode((1080, 720), pygame.FULLSCREEN) # Crée la fenêtre
ui = combatscreen(screen)

while True: # Boucle infinie simple
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    ui.draw_fight_screen()
    pygame.display.flip()

