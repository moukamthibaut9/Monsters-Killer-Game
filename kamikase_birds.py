import pygame
import animation
import media_and_screen as ms
from random import randint


pygame.init()

class Kamikase_Birds(animation.Sprite_Animation):

    def __init__(self,game):
        super().__init__('bird','simple_bird', game)
        self.game=game
        self.explosion_image=pygame.transform.scale(ms.loading_image('explosion.png'),
                            (self.game.player.rect.w,self.game.player.rect.h))
        self.bird_speed=ms.cell_width
        self.allow_kamikase_birds=False
        self.bird_rects=[
            pygame.Rect(randint(-50,-25)*ms.cell_width,10*ms.cell_height,20*ms.cell_width,15*ms.cell_height),
            pygame.Rect(randint(-50,-25)*ms.cell_width,35*ms.cell_height,20*ms.cell_width,15*ms.cell_height)
        ]

    def bliting_birds(self):
        for rect in self.bird_rects:
            # On fait appel a la fonction 'bliting_animate_sprite' de la classe mere Sprite_Animation pour 
            # un affichage animé des oiseaux kamikases
            self.bliting_animate_sprite('flying','right',rect)

    def moving_birds(self):
        for i in range(len(self.bird_rects)):
            self.bird_rects[i].x+=self.bird_speed
            # Si un oiseau kamikaze sort de la surface de jeu, on reinitialise sa position
            if self.bird_rects[i].left>=2*ms.screen_size[0]:
                self.bird_rects[i].x=randint(-50,-25)*ms.cell_width
            # Lorsqu'un oiseau kamikaze entre en contact avec le joueur
            elif self.bird_rects[i].colliderect(self.game.player.rect):
                # Si le joueur n'est pas blindé, il lui inflige dix fois plus de dégats qu'une attaque de
                # monstre, et ensuite on reinitialise sa position ; sinon l'oiseau explose simplement, mais 
                # rien n arrive au joueur, puis  on reinitialise sa position.
                if self.game.player.player_shielded==False:
                    if self.game.monster.monster_attack_marks>=3*0.6:
                        self.game.player.player_health_marks_rect.w-= \
                            10*(self.game.monster.monster_attack_marks-self.game.monster.monster_attack_marks%0.6)
                    else:
                        self.game.player.player_health_marks_rect.w-=10*3*0.6
                    # On joue l'audio correspondant au cri du joueur lorsqu'il subit un grand dégat
                    self.game.player_very_touched.play()
                    # On affiche une image d'explosion
                    self.game.screen.blit(self.explosion_image,(self.bird_rects[i].centerx,
                        self.game.player.rect.y,self.game.player.rect.w,self.game.player.rect.h))
                    self.bird_rects[i].x=randint(-50,-25)*ms.cell_width
                else:
                    # On affiche une image d'explosion
                    self.game.screen.blit(self.explosion_image,(self.bird_rects[i].centerx,
                        self.game.player.rect.y,self.game.player.rect.w,self.game.player.rect.h))
                    self.bird_rects[i].x=randint(-50,-25)*ms.cell_width

