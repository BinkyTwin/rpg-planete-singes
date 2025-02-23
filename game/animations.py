import pygame

class FadeOutAnimation:
    def __init__(self, duration_ms=500):
        self.duration_ms = duration_ms
        self.start_time = None
        self.is_finished = False
        self.alpha = 255  # Opacité initiale

    def start(self):
        """Démarre l'animation"""
        self.start_time = pygame.time.get_ticks()
        self.is_finished = False
        self.alpha = 255

    def update(self):
        """Met à jour l'animation"""
        if not self.start_time or self.is_finished:
            return

        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time

        if elapsed >= self.duration_ms:
            self.alpha = 0
            self.is_finished = True
        else:
            # Calcul de l'opacité (255 -> 0)
            progress = elapsed / self.duration_ms
            self.alpha = int(255 * (1 - progress))

    def apply_to_surface(self, surface):
        """Applique l'effet de fade out à une surface"""
        # Créer une copie de la surface avec un canal alpha
        surface_alpha = surface.convert_alpha()
        # Définir l'opacité
        surface_alpha.fill((255, 255, 255, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)
        return surface_alpha
