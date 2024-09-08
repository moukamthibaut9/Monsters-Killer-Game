import pygame
import os
import pickle

pygame.init()


(screen_width, screen_height) = (pygame.display.Info().current_w, pygame.display.Info().current_h)
(nbr_cell_x, nbr_cell_y) = (150, 100)
(cell_width, cell_height) = (screen_width//nbr_cell_x, screen_height//nbr_cell_y)
screen_size = (nbr_cell_x*cell_width, nbr_cell_y*cell_height)


def loading_image(img_name):
    """
    Cette fonction permet de charger plus convenablement une image via pygame
    """
    img_fullname = os.path.join(f"Images/{img_name}")
    try:
        image = pygame.image.load(img_fullname)
    except :
        print(f"Impossible de charger l'image {img_name}")
        
    return image

def loading_sound(sound_name):
    """
    Cette fonction permet de charger plus convenablement un son via pygame
    """
    sound_fullname = os.path.join("Sounds", sound_name)
    class NotSound:
        def play(self):
            pass
    try:
        sound = pygame.mixer.Sound(sound_fullname)
    except:
        sound = NotSound()
        print(f"Impossible de charger l'audio {sound_name}")

    return sound

def saving_player_data(attribut1,attribut2,attribut3,attribut4,file):
    """
    Cette fonction permet l'enregistrement des données du joueur lorsque celui-ci va quitter le jeu
    Attribut 1: Représente le dictionnaire associé à la sauvegarde dans le jeu
    Attribut 2: Représente le nom que va entrer le joueur ( elle représente aussi une clé du dictionnaire)
    Attribut 3: Représente le score qu'a atteint le joueur lorsque celui-ci quitte la partie
    Attribut 4: Représente le niveau qu'a atteint le joueur lorsque celui-ci quitte la partie 
    File: Représente le fichier dans lequel sera stocqué le dictionnaire une fois les données stocquées dedans
    """
    attribut1[attribut2.lower()]=[attribut3,attribut4]
    with open(os.path.join(file),'wb') as player_data_save_file:
        data_saving = pickle.Pickler(player_data_save_file)
        data_saving.dump(attribut1)

