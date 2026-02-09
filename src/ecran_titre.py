import pygame
import sys
import subprocess
pygame.init()

#Fenêtre
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ecran titre")

#Ressources
background = pygame.image.load("../others/red_background.jpg")
background = pygame.transform.scale(background, (WIDTH,HEIGHT))

#Couleurs
WHITE = (255, 255, 255)
TRANSLUCENT_BLUE = (0, 80, 200, 180)
HOVER_BLUE = (0, 140, 255, 220)
SHADOW = (0, 0, 0)
#Polices
try:
    FONT_TITLE = pygame.font.Font('../dialog/dialog_font.ttf', 72)
    FONT_BUTTON = pygame.font.Font('../dialog/dialog_font.ttf', 36)

except:     #Si la police est introuvable
    FONT_TITLE = pygame.font.SysFont('Arial', 72)
    FONT_BUTTON = pygame.font.SysFont('Arial', 36)

class Button:
    def __init__(self, text, center_y, action):
        self.text = text
        self.action = action
        self.center_y = center_y
        self.width, self.height = 320, 70
        self.rect = pygame.Rect((0, 0, self.width, self.height))
        self.rect.center = (WIDTH // 2, center_y)

    def draw(self, win, mouse_pos):
        is_hover = self.rect.collidepoint(mouse_pos)
        color = HOVER_BLUE if is_hover else TRANSLUCENT_BLUE
        button_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, color, (0, 0, self.width, self.height), border_radius = 16)
        win.blit(button_surface, self.rect)

        text_surf = FONT_BUTTON.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center = self.rect.center)

        shadow = FONT_BUTTON.render(self.text, True, SHADOW)
        win.blit(shadow, (text_rect.x + 2, text_rect.y + 2))
        win.blit(text_surf, text_rect)

    def is_clicked(self, mouse_pos, mouse_pressed):
        return self.rect.collidepoint(mouse_pos) and mouse_pressed[0]

#Liste buttons

buttons = [
    Button("Nouvelle Partie", 320, "new"),
    Button("Charger Partie", 400, "load"),
    Button("Options", 480, "options"),
    Button("Quitter", 560, "quit")
]

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)
    screen.blit(background, (0, 0))

    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    title = FONT_TITLE.render("Mon Jeu", True, WHITE)
    shadow = FONT_TITLE.render("Mon Jeu", True, SHADOW)
    screen.blit(shadow, (WIDTH // 2 - title.get_width() // 2 + 3, 103))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))


    for btn in buttons:
        btn.draw(screen, mouse_pos)
        if btn.is_clicked(mouse_pos, mouse_pressed):
            pygame.time.delay(200)
            if btn.action == "new":
                print("Nouvelle partie")
                with open("../saves/logs.txt", "w") as logs:
                    logs.write(">>>>> LOGS DU JEU PYTHON <<<<<\n")
                with open("../saves/save_Python.txt", "w") as logs:
                    logs.write("___SAUVEGARDE DU PROJET PYTHON___")
                pygame.quit()
                subprocess.run(["python", "main.py"])
                sys.exit()
            elif btn.action == "load":
                print("Charger Partie")
                pygame.quit()
                subprocess.run(["python", "main.py"])
                sys.exit()
            elif btn.action == "options":
                print("Options")
            elif btn.action == "quit":
                running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
print("Fermeture du jeu")

