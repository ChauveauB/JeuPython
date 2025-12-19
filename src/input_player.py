import pygame

# Boîte de saisie minimale réutilisée dans get_input
class InputBox:
    def __init__(self, rect, font, text_color=(255,255,255), box_color=(0,0,0), active_color=(50,50,50)):
        self.rect = pygame.Rect(rect)
        self.font = font
        self.text = ""
        self.active = True
        self.done = False
        self.text_color = text_color
        self.box_color = box_color
        self.active_color = active_color

    def handle_event(self, event):
        # Gère clics et frappes clavier
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.done = True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                # event.unicode gère accents et symboles
                self.text += event.unicode

    def draw(self, surface):
        color = self.active_color if self.active else self.box_color
        pygame.draw.rect(surface, color, self.rect)
        txt_surf = self.font.render(self.text, True, self.text_color)
        surface.blit(txt_surf, (self.rect.x + 5, self.rect.y + 5))

    def reset(self):
        self.text = ""
        self.done = False

def get_input(prompt, width=640, height=120):
    """
    Remplace input() : affiche une petite UI Pygame et attend l'appui sur Entrée.
    - prompt : texte affiché au-dessus de la zone de saisie.
    - Retourne la chaîne saisie.
    Note : get_input crée une surface temporaire si aucune surface pygame n'existe.
    """
    pygame.init()
    # réutilise la surface si elle existe, sinon crée une fenêtre temporaire
    existing_surface = pygame.display.get_surface()
    created_window = False
    if existing_surface is None:
        screen = pygame.display.set_mode((width, height))
        created_window = True
    else:
        screen = existing_surface

    font = pygame.font.Font(None, 26)
    input_box = InputBox((10, 48, width - 20, 40), font)
    clock = pygame.time.Clock()

    running = True
    while running and not input_box.done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # force la fermeture si nécessaire
                pygame.quit()
                raise SystemExit
            input_box.handle_event(event)

        screen.fill((30, 30, 30))
        # afficher le prompt
        prompt_surf = font.render(prompt, True, (255, 255, 255))
        screen.blit(prompt_surf, (10, 10))
        input_box.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    value = input_box.text
    input_box.reset()
    if created_window:
        # fermer la fenêtre si on l'a créée
        pygame.display.quit()
    return value