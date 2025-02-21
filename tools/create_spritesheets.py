import os
from PIL import Image, ImageDraw

def create_character_spritesheet(race_name, color):
    """Crée un spritesheet basique pour une race de singe donnée"""
    # Dimensions pour chaque frame
    frame_width = 64  # Augmenté à 64x64
    frame_height = 64
    
    # Dimensions totales du spritesheet (4x4)
    sheet_width = frame_width * 4  # 4 frames par animation
    sheet_height = frame_height * 4  # 4 directions
    
    # Créer une nouvelle image avec fond transparent
    spritesheet = Image.new('RGBA', (sheet_width, sheet_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(spritesheet)
    
    # Pour chaque direction (down, left, right, up)
    for dir_idx in range(4):
        # Pour chaque frame d'animation
        for frame_idx in range(4):
            # Calculer la position de la frame
            x = frame_idx * frame_width
            y = dir_idx * frame_height
            
            # Animation : faire bouger légèrement le personnage
            offset = frame_idx % 2 * 4
            
            # Corps principal (plus grand et plus détaillé)
            draw.ellipse(
                [x + 16, y + 16, x + 48, y + 48],
                fill=color
            )
            
            # Tête (plus grande)
            head_color = tuple(max(0, min(255, c + 30)) for c in color[:3]) + (color[3],)
            draw.ellipse(
                [x + 20, y + 8, x + 44, y + 32],
                fill=head_color
            )
            
            # Détails en fonction de la direction
            if dir_idx == 0:  # down
                # Yeux
                draw.ellipse([x + 26, y + 16, x + 32, y + 22], fill='white')
                draw.ellipse([x + 34, y + 16, x + 40, y + 22], fill='white')
                # Pupilles
                draw.ellipse([x + 28, y + 18, x + 30, y + 20], fill='black')
                draw.ellipse([x + 36, y + 18, x + 38, y + 20], fill='black')
            elif dir_idx == 1:  # left
                # Œil gauche
                draw.ellipse([x + 22, y + 16, x + 28, y + 22], fill='white')
                draw.ellipse([x + 23, y + 18, x + 25, y + 20], fill='black')
            elif dir_idx == 2:  # right
                # Œil droit
                draw.ellipse([x + 36, y + 16, x + 42, y + 22], fill='white')
                draw.ellipse([x + 39, y + 18, x + 41, y + 20], fill='black')
            else:  # up
                # Dos de la tête
                draw.ellipse([x + 24, y + 12, x + 40, y + 28], fill=head_color)
            
            # Jambes
            leg_offset = offset // 2
            draw.ellipse([x + 24 - leg_offset, y + 40, x + 32 - leg_offset, y + 56], fill=color)  # Jambe gauche
            draw.ellipse([x + 32 + leg_offset, y + 40, x + 40 + leg_offset, y + 56], fill=color)  # Jambe droite
            
            # Bras
            arm_offset = offset // 2
            draw.ellipse([x + 12, y + 24, x + 20, y + 32], fill=color)  # Bras gauche
            draw.ellipse([x + 44, y + 24, x + 52, y + 32], fill=color)  # Bras droit
    
    # Créer le dossier de sortie s'il n'existe pas
    os.makedirs('assets/character', exist_ok=True)
    
    # Sauvegarder le spritesheet
    output_path = os.path.join('assets/character', f'{race_name}.png')
    spritesheet.save(output_path)
    print(f"Spritesheet créé : {output_path}")

def main():
    # Définir les races et leurs couleurs avec plus de variété
    characters = {
        'chimpanze': (139, 69, 19, 255),      # Marron
        'gorille': (64, 64, 64, 255),         # Gris foncé
        'orang outan': (205, 133, 63, 255),   # Orange-brun
        'bonobo': (101, 67, 33, 255),         # Marron clair
        'singe hurleur': (165, 42, 42, 255)   # Rouge-brun
    }
    
    # Créer un spritesheet pour chaque race
    for race, color in characters.items():
        create_character_spritesheet(race, color)

if __name__ == '__main__':
    main()
