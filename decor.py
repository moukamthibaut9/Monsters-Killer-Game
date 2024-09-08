import pygame
import media_and_screen as ms



pygame.init()

class Decor:

    def __init__(self,game):
        self.game=game
        self.bg_rect = pygame.Rect(0, 0, ms.screen_size[0], ms.screen_size[1])
        self.supports_rects = [
                        pygame.Rect(25*ms.cell_width, 55*ms.cell_height, 20*ms.cell_width, 2*ms.cell_height),
                        pygame.Rect(65*ms.cell_width, 30*ms.cell_height, 20*ms.cell_width, 2*ms.cell_height),
                        pygame.Rect(105*ms.cell_width, 55*ms.cell_height, 20*ms.cell_width, 2*ms.cell_height)
                        ]
        # On initialise l'image d'arriere plan en fonction du niveau de jeu du joueur
        self.bg_img = ms.loading_image("terrain"+str(self.game.game_level)+".jpg")
        self.support_img = ms.loading_image("support.png")
        self.supports_images = [
            self.support_img.subsurface((148, 115, 85, 19)),
            self.support_img.subsurface((342, 115, 85, 19)),
            self.support_img.subsurface((148, 115, 85, 19))
            ]
    def bliting_decor(self, screen):
        self.bg_img = pygame.transform.scale(self.bg_img,(self.bg_rect.w,self.bg_rect.h))
        screen.blit(self.bg_img, self.bg_rect)
        for i in range(len(self.supports_rects)):
            self.supports_images[i] = pygame.transform.scale(self.supports_images[i],
                                    (self.supports_rects[i].w,self.supports_rects[i].h))
            screen.blit(self.supports_images[i], self.supports_rects[i])
