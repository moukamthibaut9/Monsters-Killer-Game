import pygame
import media_and_screen as ms
from random import randint
from time import time

pygame.init()

class Bonus:
    def __init__(self,bonus_category,game):
        self.game=game
        self.bonus_category=bonus_category
        self.rect=pygame.Rect(randint(0,140)*ms.cell_width,randint(10,80)*ms.cell_height,5*ms.cell_width,5*ms.cell_height)
        if self.bonus_category=='health_bonus':
            self.image=pygame.transform.scale(ms.loading_image('bonus1.png'),(self.rect.w,self.rect.h))
        if self.bonus_category=='shield_bonus':
            self.image=pygame.transform.scale(ms.loading_image('bonus2.png'),(self.rect.w,self.rect.h))

    def bliting_bonus(self):
        for bonus in self.game.game_all_bonus:
            self.game.screen.blit(bonus.image,bonus.rect)
            # Definitions des instructions en cas de contact du joueur avec un bonus
            if self.game.player.rect.colliderect(bonus.rect):
                if bonus.bonus_category=='health_bonus':
                    if self.game.player.player_health_marks_rect.w<=self.game.player.player_max_health_marks_rect.w-10*ms.cell_width:
                        self.game.player.player_health_marks_rect.w+=10*ms.cell_width
                    else:
                        self.game.player.player_health_marks_rect.w=self.game.player.player_max_health_marks_rect.w
                    self.game.health_bonus.play()
                elif bonus.bonus_category=='shield_bonus':
                    self.game.player.player_shielded=True
                    self.game.player.player_shield_rect.w=self.game.player.player_max_len_shield_rect
                    # On recupere le temps auquel le joueur a touche le bonus de blindage et on reajuste le
                    # temps permettant de controler la variation  de la barre de blindage du joueur en fonction de celui-ci.
                    self.game.game_start_time4=time()//2 
                    self.game.game_start_time5=self.game.game_start_time4
                    self.game.shield_bonus.play()
                self.game.game_all_bonus.remove(bonus) # Suppression du bonus courant
                self.game.bliting_bonus=False
            # Si 10 secondes s'ecoulent sans que le joueur ne touche un bonus, celui-ci disparait
            elif (self.game.game_actual_time-self.game.game_start_time3)!=0 \
            and (self.game.game_actual_time-self.game.game_start_time3)%5==0 and self.game.bliting_bonus==True:
                self.game.game_all_bonus.remove(bonus) # Suppression du bonus courant
                self.game.bliting_bonus=False
                self.game.game_start_time3=self.game.game_actual_time # On redefinit le point de controle du temps 3 au temps actuel
                

class Health_Bonus(Bonus):
    def __init__(self,game):
        super().__init__('health_bonus', game)

class Shield_Bonus(Bonus):
    def __init__(self,game):
        super().__init__('shield_bonus', game)