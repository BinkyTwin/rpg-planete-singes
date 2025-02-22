import pygame

class PNJ:
    def __init__(self, position=(20, 27), faction=None):
        self.position = position
        self.faction = faction
        self.sprite = self.load_sprite('assets/tilesets/images/orang_outan.png')

    def load_sprite(self, image_file):
        try:
            # Load the sprite sheet with transparency
            sheet = pygame.image.load(image_file).convert_alpha()
            # Assuming the sprite sheet contains 4 frames horizontally
            frame_width = sheet.get_width() // 4
            # Extract only the first frame to ensure the sprite remains stable
            frame_rect = (0, 0, frame_width, sheet.get_height())
            frame = sheet.subsurface(frame_rect)
            return frame
        except Exception as e:
            raise FileNotFoundError(f"Impossible de charger l'image {image_file}: {str(e)}")

if __name__ == '__main__':
    # Minimal initialization to test sprite display
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pnj = PNJ()
    # Display the static frame for verification
    screen.fill((0, 0, 0))
    screen.blit(pnj.sprite, (100, 100))
    pygame.display.flip()
    # Wait loop for window close
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()
