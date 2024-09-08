import pygame
import media_and_screen as ms
from bullet import Bullets


pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self,player_image,player_name,game):
        super().__init__()
        self.game=game
        self.rect=pygame.Rect(ms.cell_width,72*ms.cell_height,10*ms.cell_width,15*ms.cell_height)
        self.player_name=player_name
        self.player_on_some_support=True
        self.player_jump_nbr=20
        self.player_jump=False
        self.player_jump_down_continious=False
        self.player_jump_index=0
        self.player_jump_up_index=0
        self.player_jump_down_index=self.player_jump_nbr
        self.player_image=player_image
        self.player_all_bullets=[]
        self.player_bullet_launched=False
        self.player_remaining_shots=0
        self.pressed_button={}
        self.player_direction=[0,'right']
        self.player_state='stand_up'
        self.player_alive=True
        self.player_shielded=False
        self.player_speed=[ms.cell_width,ms.cell_height]
        self.player_victory_marks=0
        self.player_health_marks_rect=pygame.Rect(12*ms.cell_width,3*ms.cell_height,115*ms.cell_width,4*ms.cell_height)
        self.player_max_health_marks_rect=pygame.Rect(12*ms.cell_width,3*ms.cell_height,115*ms.cell_width,4*ms.cell_height)
        self.player_max_len_shield_rect=100*ms.cell_width
        self.player_shield_rect=pygame.Rect(27*ms.cell_width,0,0,3*ms.cell_height)
        self.decrease_nbr_for_end_player_shield_rect=5
        self.player_attack_marks=ms.cell_width

    def bliting_player(self,image,rect,player_logo,player_logo_rect):
        image = pygame.transform.scale(image,(rect.w,rect.h))
        # Affichage du joueur
        self.game.screen.blit(image,rect)
        player_logo = pygame.transform.scale(player_logo,(player_logo_rect.w,player_logo_rect.h))
        # Affichage du logo du joueur
        self.game.screen.blit(player_logo,player_logo_rect)
        # Dessin de la barre de vie du joueur
        pygame.draw.rect(self.game.screen,(255,0,0),self.player_max_health_marks_rect)
        pygame.draw.rect(self.game.screen,(0,255,0),self.player_health_marks_rect)
        # Si le joueur est actuellement blindé; on dessine sa barre de blindage (son rectangle de blindage n'est pas vide)
        if self.player_shield_rect.w>0:
            if (self.game.game_actual_time-self.game.game_start_time5)!=0 \
            and (self.game.game_actual_time-self.game.game_start_time5)%1==0:
                self.player_shield_rect.w-=self.player_max_len_shield_rect/self.decrease_nbr_for_end_player_shield_rect
                self.game.game_start_time5=self.game.game_actual_time
            pygame.draw.rect(self.game.screen,(192,192,192),self.player_shield_rect)

        return image, player_logo

    def moving_player(self,rect):
        # Lorsque le joueur tire
        if self.pressed_button.get(pygame.K_SPACE) and self.pressed_button.get(pygame.K_x):
            if self.player_remaining_shots>0:
                self.player_state='attack'
                self.game.player_has_shot.play() # On joue l'audio correspondant a un tir du joueur
                new_bullet=Bullets(self.player_direction[1],self.game) 
                if len(self.player_all_bullets)<=1:
                    self.player_all_bullets.append(new_bullet)
                self.player_bullet_launched = True
                if new_bullet.bullet_direction=='right':
                    new_bullet.image=new_bullet.normal_image
                elif new_bullet.bullet_direction=='left':
                    new_bullet.image=new_bullet.reverse_image
                # Reassignation de la position du projectile en fonction de celle du joueur
                new_bullet.rect.x=rect.centerx
                new_bullet.rect.y=rect.y+3*ms.cell_height
        # Lorsque le joueur se deplace horizontalement
        # On vérifie s'il est autorisé à se déplacer(Gestion de ce paramètre dans monsters.py: moving_monster) 
        if self.game.player_moving_autorised==True:
            rect.x+=self.player_direction[0]*self.player_speed[0]
        # Lorsque le joueur saute
        if self.player_jump==True:
            if self.player_jump_up_index<=self.player_jump_nbr:
                self.player_jump_up_index+=1
                self.player_jump_index=self.player_jump_up_index
                rect.y-=2*self.player_speed[1]
            else:
                rect.y+=self.player_speed[1]
                self.player_jump_down_index-=1
                self.player_jump_index=self.player_jump_down_index
        elif self.player_jump_down_continious==True:
            rect.y+=self.player_speed[1]
            self.player_jump_down_index-=1
            self.player_jump_index=self.player_jump_down_index
            
        return rect


class Player1(Player):
    def __init__(self,player_name,game):
        self.image=ms.loading_image("player1.png")
        self.player_stand_up=[
                            [self.image.subsurface((210,0,52,60))],
                            [pygame.transform.flip(self.image.subsurface((210,0,52,60)),True,False)]
                        ]
        self.player_running=[
                    [
                        self.image.subsurface((263,0,72,60)),self.image.subsurface((335,0,68,60)),
                        self.image.subsurface((404,0,69,60)),self.image.subsurface((472,0,69,60)),
                        self.image.subsurface((541,0,69,60)),self.image.subsurface((611,2,69,55)),
                        self.image.subsurface((682,2,69,55)),self.image.subsurface((751,2,69,55))
                    ],
                    [
                        pygame.transform.flip(self.image.subsurface((263,0,72,60)),True,False),
                        pygame.transform.flip(self.image.subsurface((335,0,68,60)),True,False),
                        pygame.transform.flip(self.image.subsurface((404,0,69,60)),True,False),
                        pygame.transform.flip(self.image.subsurface((472,0,69,60)),True,False),
                        pygame.transform.flip(self.image.subsurface((541,0,69,60)),True,False),
                        pygame.transform.flip(self.image.subsurface((611,2,69,55)),True,False),
                        pygame.transform.flip(self.image.subsurface((682,2,69,55)),True,False),
                        pygame.transform.flip(self.image.subsurface((751,2,69,55)),True,False)
                    ]
                ]
        self.player_attack=[
                    [
                        self.image.subsurface((357,59,107,57)),self.image.subsurface((465,59,76,57)),
                        self.image.subsurface((541,59,49,64)),self.image.subsurface((593,59,51,64)),
                        self.image.subsurface((645,57,76,55)),self.image.subsurface((720,59,53,54))
                    ],
                    [
                        pygame.transform.flip(self.image.subsurface((357,59,107,57)),True,False),
                        pygame.transform.flip(self.image.subsurface((465,59,76,57)),True,False),
                        pygame.transform.flip(self.image.subsurface((541,59,49,64)),True,False),
                        pygame.transform.flip(self.image.subsurface((593,59,51,64)),True,False),
                        pygame.transform.flip(self.image.subsurface((645,57,76,55)),True,False),
                        pygame.transform.flip(self.image.subsurface((720,59,53,54)),True,False)
                    ],

                ]
        self.player_all_states={
                            'stand_up':self.player_stand_up,
                            'running':self.player_running,
                            'attack':self.player_attack
                        }
        self.image_index=0
        self.player_logo_rect=pygame.Rect(0,1.5*ms.cell_height,9*ms.cell_width,7*ms.cell_height)
        self.player_logo=self.image.subsurface((295,312,165,98))
        Player.__init__(self,self.player_stand_up[0][0],player_name,game)

    def bliting_player(self):
        self.image_index+=1
        if self.image_index>=len(self.player_all_states[self.player_state][0]):
            self.image_index=0
        if self.player_direction[1]=='right':
            self.player_image=self.player_all_states[self.player_state][0][self.image_index]
        elif self.player_direction[1]=='left':
            self.player_image=self.player_all_states[self.player_state][1][self.image_index]

        self.player_image, self.player_logo = super().bliting_player(self.player_image,
                                            self.rect,self.player_logo,self.player_logo_rect)
        if self.player_state=='attack':
            pygame.time.wait(10)

    def moving_player(self):
        self.rect = super().moving_player(self.rect)

    def __str__(self):
        return f"Player Name: {self.player_name}\nPlayer Avatar: Blade Queen"


class Player2(Player):
    def __init__(self,player_name,game):
        self.image=ms.loading_image("player2.png")
        self.player_stand_up=[
                            [self.image.subsurface((46,5,56,39))],
                            [pygame.transform.flip(self.image.subsurface((46,5,56,39)),True,False)]
                        ]
        self.player_attack=[
                [
                    self.image.subsurface((35,56,38,40)),self.image.subsurface((0,126,45,46)),
                    self.image.subsurface((50,135,40,41)),self.image.subsurface((91,101,63,71)),
                    self.image.subsurface((160,101,63,71)),self.image.subsurface((229,101,63,71))
                ],
                [
                    pygame.transform.flip(self.image.subsurface((35,56,38,40)),True,False),
                    pygame.transform.flip(self.image.subsurface((0,126,45,46)),True,False),
                    pygame.transform.flip(self.image.subsurface((50,135,40,41)),True,False),
                    pygame.transform.flip(self.image.subsurface((91,101,63,71)),True,False),
                    pygame.transform.flip(self.image.subsurface((160,101,63,71)),True,False),
                    pygame.transform.flip(self.image.subsurface((229,101,63,71)),True,False)
                ],
            ]
        self.player_all_states={
                            'stand_up':self.player_stand_up,
                            'running':self.player_stand_up,
                            'attack':self.player_attack
                        }
        self.image_index=0
        self.player_logo_rect=pygame.Rect(0,ms.cell_height,11*ms.cell_width,8*ms.cell_height)
        self.player_logo=self.image.subsurface((0,4,34,39))
        Player.__init__(self,self.player_stand_up[0][0],player_name,game)

    def bliting_player(self):
        self.image_index+=1
        if self.image_index>=len(self.player_all_states[self.player_state][0]):
            self.image_index=0
        if self.player_direction[1]=='right':
            self.player_image=self.player_all_states[self.player_state][0][self.image_index]
        elif self.player_direction[1]=='left':
            self.player_image=self.player_all_states[self.player_state][1][self.image_index]

        self.player_image, self.player_logo = super().bliting_player(self.player_image,
                                            self.rect,self.player_logo,self.player_logo_rect)
        if self.player_state=='attack':
            pygame.time.wait(10)

    def moving_player(self):
        self.rect = super().moving_player(self.rect)

    def __str__(self):
        return f"Player Name: {self.player_name}\nPlayer Avatar: Demon Hunter"
