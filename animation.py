import pygame
import media_and_screen as ms
import os


def get_all_elements(path):
    return os.listdir(os.path.join(path))

def get_folders(path):
    return [elt for elt in os.listdir(os.path.join(path)) if os.path.isdir(os.path.join(path,elt))]

def get_files(path):
    return [elt for elt in os.listdir(os.path.join(path)) if os.path.isfile(os.path.join(path,elt))]


"""
Cette succession de boucles va permettre de parcourrir tous les sous repertoires du repertoire 'Images' de facon 
recursive afin d'en recuperer les images presentes pour les stocquer dans des dictionnaires qui seront contenus 
dans des dictionnaires qui seront contenus dans des dictionnaires qui eux memes seront contenus dans le dictionnaire 
'all_sprites_dico'. Chacun de ces dictionnaires a pour cles les noms des dossiers fils d'un dossier parent dont 
le nom represente une cle  du dictionnaire qui le contient.   

"""
all_sprites_dico = {}
for sprite in get_folders('Images'):
    particular_sprite_dico = {}
    for category in get_folders(f"Images/{sprite}"):
        category_sprite_dico = {}
        for level in get_folders(f"Images/{sprite}/{category}"):
            level_sprite_dico = {}
            for state in get_folders(f"Images/{sprite}/{category}/{level}"):
                states_sprite_list = [[],[]]
                for image in get_files(f"Images/{sprite}/{category}/{level}/{state}"):
                    if os.path.exists(f"Images/{sprite}/{category}/{level}/{state}/{image}"):
                        # On verifie la categorie de l'entité et le niveau de jeu avant de 
                        # definir l'image qui sera considerée comme normale
                        if (category == 'simple_monster' and '3' in level) \
                        or (category == 'main_monster' and ('2' in level or '3' in level)):
                            # On stocque les images normales d'une entité dans la premiere 
                            # liste de la liste 'states_sprite_list'
                            states_sprite_list[0].append(pygame.transform.flip(
                                ms.loading_image(f"{sprite}/{category}/{level}/{state}/{image}"),True,False))
                        else:
                            states_sprite_list[0].append(
                                ms.loading_image(f"{sprite}/{category}/{level}/{state}/{image}"))
                for image in get_files(f"Images/{sprite}/{category}/{level}/{state}"):
                    if os.path.exists(f"Images/{sprite}/{category}/{level}/{state}/{image}"):
                        # On verifie la categorie de l'entité et le niveau de jeu avant de 
                        # definir l'image qui sera considerée comme renversée
                        if (category == 'simple_monster' and '3' in level) \
                        or (category == 'main_monster' and ('2' in level or '3' in level)):
                            # On stocque les images renversées d'une entité dans la deuxieme 
                            # liste de la liste 'states_sprite_list'
                            states_sprite_list[1].append(
                                ms.loading_image(f"{sprite}/{category}/{level}/{state}/{image}"))
                        else:
                            states_sprite_list[1].append(pygame.transform.flip(
                                ms.loading_image(f"{sprite}/{category}/{level}/{state}/{image}"),True,False))
                level_sprite_dico[state] = states_sprite_list
            category_sprite_dico[level] = level_sprite_dico
        particular_sprite_dico[category] = category_sprite_dico
    all_sprites_dico[sprite] = particular_sprite_dico



class Sprite_Animation(pygame.sprite.Sprite):

    def __init__(self,sprite_label,sprite_category,game):
        super().__init__()
        self.game = game
        self.sprite_label = sprite_label
        self.sprite_category = sprite_category
        if sprite_category == 'simple_bird':
            self.image = ms.loading_image(
                f"{self.sprite_label}/{sprite_category}/level{self.game.game_level}/flying/{sprite_category}{self.game.game_level}1.png")
        else:
            self.image = ms.loading_image(
                f"{self.sprite_label}/{sprite_category}/level{self.game.game_level}/stand_up/{sprite_category}{self.game.game_level}1.png")
        self.sprite_states_images = all_sprites_dico[sprite_label][sprite_category][f"level{self.game.game_level}"]
        self.image_index = 0

    def bliting_animate_sprite(self,sprite_state,sprite_direction,sprite_rect):
        if self.image_index >= len(self.sprite_states_images[sprite_state][0]):
            self.image_index = 0
        self.image = self.sprite_states_images[sprite_state][0][self.image_index]
        if self.sprite_label == 'monster':
            # On adapte l'image du monstre en fonction du coté vers lequel il est tourné(gauche ou droit)
            if sprite_direction=='left' or (sprite_direction=='' and sprite_rect.right>self.game.player.rect.centerx \
            and  sprite_rect.left>self.game.player.rect.centerx):
                    self.image = self.sprite_states_images[sprite_state][0][self.image_index]
            elif sprite_direction=='right' or (sprite_direction=='' and sprite_rect.right<self.game.player.rect.centerx \
            and  sprite_rect.left<self.game.player.rect.centerx):
                self.image = self.sprite_states_images[sprite_state][1][self.image_index]
        self.image=pygame.transform.scale(self.image,(sprite_rect.w,sprite_rect.h))
        self.game.screen.blit(self.image,sprite_rect)
        if self.sprite_category == 'main_monster' and sprite_state == 'running':
            pygame.time.wait(5)
        self.image_index +=1
        
