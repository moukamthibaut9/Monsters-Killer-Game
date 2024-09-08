import pygame
import media_and_screen as ms
from random import randint, choice


pygame.init()

class Comets_Rain(pygame.sprite.Sprite):

    def __init__(self,game):
        super().__init__()
        self.game=game
        self.allow_comets_rain=False
        self.comet_image=pygame.transform.scale(
                        ms.loading_image('comet.png'),(5*ms.cell_width,5*ms.cell_height))
        self.comet_rects=[
        pygame.Rect(randint(0,20)*ms.cell_width,randint(-30,-10)*ms.cell_height,5*ms.cell_width,5*ms.cell_height),
        pygame.Rect(randint(25,40)*ms.cell_width,randint(-30,-10)*ms.cell_height,5*ms.cell_width,5*ms.cell_height),
        pygame.Rect(randint(45,65)*ms.cell_width,randint(-30,-10)*ms.cell_height,5*ms.cell_width,5*ms.cell_height),
        pygame.Rect(randint(70,90)*ms.cell_width,randint(-30,-10)*ms.cell_height,5*ms.cell_width,5*ms.cell_height),
        pygame.Rect(randint(95,105)*ms.cell_width,randint(-30,-10)*ms.cell_height,5*ms.cell_width,5*ms.cell_height),
        pygame.Rect(randint(110,130)*ms.cell_width,randint(-30,-10)*ms.cell_height,5*ms.cell_width,5*ms.cell_height),
        pygame.Rect(randint(130,145)*ms.cell_width,randint(-30,-10)*ms.cell_height,5*ms.cell_width,5*ms.cell_height)
        ]
        self.comet_speed=ms.cell_height/2

    def bliting_comets(self):
        for rect in self.comet_rects:
            self.game.screen.blit(self.comet_image,rect)

    def moving_comets(self):
        for i in range(len(self.comet_rects)):
            self.comet_rects[i].y+=self.comet_speed
            # Si une comete entre en contact avec le sol, on reinitialise sa position
            if self.comet_rects[i].bottom>=ms.screen_size[1]:
                (self.comet_rects[i].x,self.comet_rects[i].y)=\
                    (randint(20*i,23*(i+1))*ms.cell_width,randint(-30,-10)*ms.cell_height)
            # Lorsqu'une comète entre en contact avec le joueur
            elif self.comet_rects[i].colliderect(self.game.player.rect):
                # Si le joueur n'est pas blindé, elle lui inflige cinq fois plus de dégats qu'une attaque de
                # monstre, et ensuite on reinitialise sa position ; sinon rien ne se passe et la comete passe
                # sur le joueur comme si de rien n'etait.
                if self.game.player.player_shielded==False:
                    if self.game.monster.monster_attack_marks>=3*0.6:
                        self.game.player.player_health_marks_rect.w-= \
                            5*(self.game.monster.monster_attack_marks-self.game.monster.monster_attack_marks%0.6)
                    else:
                        self.game.player.player_health_marks_rect.w-=5*3*0.6
                    (self.comet_rects[i].x,self.comet_rects[i].y)=(randint(20*i,23*(i+1))*ms.cell_width,randint(-30,-10)*ms.cell_height)
                    # On joue l'audio correspondant au cri du joueur lorsqu'il subit un grand dégat
                    self.game.player_very_touched.play()