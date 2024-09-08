import pygame
import animation
import media_and_screen as ms
from random import randint, choice


pygame.init()

class Monsters(animation.Sprite_Animation):
    
    def __init__(self,monster_category,game):
        super().__init__('monster',monster_category,game)
        self.game=game
        self.monster_category=monster_category
        self.monster_direction=''
        self.monster_actual_state='stand_up'
        self.monster_attack_marks=ms.cell_width/5
        if self.monster_category=='simple_monster':
            self.monster_speed=choice([0.7,0.8,0.9,1,1.1,1.2,1.3])*ms.cell_width/2
            self.rect=pygame.Rect(randint(ms.nbr_cell_x-5,ms.nbr_cell_x+10)*ms.cell_width,
                                72*ms.cell_height,10*ms.cell_width,15*ms.cell_height)
            self.monster_health_rect=pygame.Rect(self.rect.x,71*ms.cell_height,10*ms.cell_width,ms.cell_height)
            self.monster_max_health_rect=pygame.Rect(self.rect.x,71*ms.cell_height,10*ms.cell_width,ms.cell_height)
        elif self.monster_category=='main_monster':
            self.monster_speed=ms.cell_width/3
            self.rect=pygame.Rect(randint(ms.nbr_cell_x-5,ms.nbr_cell_x+10)*ms.cell_width,
                                63*ms.cell_height,20*ms.cell_width,25*ms.cell_height)
            self.monster_health_rect=pygame.Rect(12*ms.cell_width,8*ms.cell_height,137*ms.cell_width,3*ms.cell_height)
            self.monster_max_health_rect=pygame.Rect(12*ms.cell_width,8*ms.cell_height,137*ms.cell_width,3*ms.cell_height)
        
    def delete_monster(self):
        self.game.game_all_monsters.remove(self)

    def bliting_monter(self):
        # Affichage des monstres et de leurs barres de vie a l'ecran
        for monster in self.game.game_all_monsters:
            # On fait appel a la fonction 'bliting_animate_sprite' de la classe mere Sprite_Animation pour 
            # un affichage animé des monstres
            monster.bliting_animate_sprite(monster.monster_actual_state,monster.monster_direction,monster.rect)
            # On dessine la barre de vie du monstre
            pygame.draw.rect(self.game.screen,(255,0,0),monster.monster_max_health_rect)
            if monster.monster_category=='simple_monster':
                pygame.draw.rect(self.game.screen,(255,255,0),monster.monster_health_rect)
            elif monster.monster_category=='main_monster':
                pygame.draw.rect(self.game.screen,(0,0,255),monster.monster_health_rect)


    def moving_monster(self):
        self.game.player_collision_with_monster=False
        self.game.player_moving_autorised=True
        for monster in self.game.game_all_monsters:
            # On verifie la situation de l'enemie par rapport au joueur avant de lui assigner une direction
            if monster.rect.right<self.game.player.rect.centerx \
            and  monster.rect.left<self.game.player.rect.centerx \
            and monster.rect.y-10*ms.cell_width<self.game.player.rect.y:
                monster.monster_direction='right'
            elif monster.rect.right>self.game.player.rect.centerx \
            and  monster.rect.left>self.game.player.rect.centerx \
            and monster.rect.y-10*ms.cell_width<self.game.player.rect.y:
                monster.monster_direction='left'
            else:
                monster.monster_direction=''
            # On deplace les enemies
            if monster.monster_direction=='right':
                monster.monster_actual_state='running'
                monster.rect.x+=monster.monster_speed
            elif monster.monster_direction=='left':
                monster.monster_actual_state='running'
                monster.rect.x-=monster.monster_speed
            else:
                # On verifie si un monstre touche un joueur avant de reduire la barre de vie de celui-ci
                # de facon adapté à la taille de l'écran
                if monster.rect.colliderect(self.game.player.rect):
                    monster.monster_actual_state='attack'
                    self.game.player_collision_with_monster=True
                    # Si le joueur n'est pas blindé, le monstre lui elle lui inflige des dégats, 
                    # sinon rien ne se passe
                    if self.game.player.player_shielded==False:
                        # Le monstre inflige moins de degats au joueur s'il attaque en meme temps que lui
                        if self.game.player.player_state=='attack':
                            if monster.monster_attack_marks>=3*0.6:
                                monster.game.player.player_health_marks_rect.w-=monster.monster_attack_marks/3
                            else:
                                self.game.player.player_health_marks_rect.w-=0.6
                            # On joue l'audio correspondant au cri du joueur lorsqu'il est faiblement touche par l'attaque d'un monstre
                            self.game.player_little_touched.play()
                            if monster.monster_category=='main_monster':
                                # On joue l'audio correspondant au cri du monstre principal losrqu'il est faiblement touché
                                self.game.main_monster_little_touched.play()
                            elif monster.monster_category=='simple_monster':
                                # On joue l'audio correspondant au cri d'un simple monstre losrqu'il est faiblement touché
                                self.game.simple_monster_little_touched.play()
                        # Si seul le monstre attaque, les degats sont infligés normalemet au joueur
                        else:
                            if monster.monster_attack_marks>=3*0.6:
                                self.game.player.player_health_marks_rect.w-=monster.monster_attack_marks-monster.monster_attack_marks%0.6
                                pygame.time.wait(5)
                            else:
                                self.game.player.player_health_marks_rect.w-=3*0.6
                            # On joue l'audio correspondant au cri du joueur lorsqu'il est fortement touche par l'attaque d'un monstre
                            self.game.player_very_touched.play()
                    # Dans le cas d'une collision, le joueur peut uniquement aller du coté opposé au monstre
                    if (self.game.player.player_direction[1]=='right' and monster.rect.x<self.game.player.rect.x) \
                    or (self.game.player.player_direction[1]=='left' and monster.rect.x>self.game.player.rect.x):
                        self.game.player_moving_autorised=True
                    # Si le joueur est tourné vers le monstre et qu'il attaque, il lui inflige des dégats
                    # et le sang de celui-ci diminu de facon adapté à la taille de l'écran
                    elif ((self.game.player.player_direction[1]=='right' and monster.rect.x>self.game.player.rect.x) \
                    or (self.game.player.player_direction[1]=='left' and monster.rect.x<self.game.player.rect.x)):
                        self.game.player_moving_autorised=False
                        if self.game.player.player_state=='attack':
                            if self.game.player.player_attack_marks>=\
                            (self.game.player.player_attack_marks/monster.monster_attack_marks)*3*0.6:
                                monster.monster_health_rect.w-=self.game.player.player_attack_marks
                            else:
                                monster.monster_health_rect.w-=3*self.game.player.player_attack_marks
                            if monster.monster_category=='main_monster':
                                # On joue l'audio correspondant au cri du monstre principal losrqu'il est faiblement touché
                                self.game.main_monster_little_touched.play()
                            elif monster.monster_category=='simple_monster':
                                # On joue l'audio correspondant au cri d'un simple monstre losrqu'il est faiblement touché
                                self.game.simple_monster_little_touched.play()
                else:
                    monster.monster_actual_state='stand_up'
            # Si la barre de vie du joueur est a 0, on passe son parametre 'player_alive' a 'False'
            if self.game.player.player_health_marks_rect.w<=-ms.cell_width:
                self.game.player.player_alive=False
            # On ajuste en temps reel la position de la barre de vie du monstre s'il s'agit d'un simple monstre
            if monster.monster_category=='simple_monster':
                monster.monster_max_health_rect.x=monster.monster_health_rect.x=monster.rect.x
            # On verifie si la barre de vie du monstre est a O avant de supprimmer celui-ci
            if monster.monster_health_rect.w<=0:
                # Si le monstre qui vient de se faire tuer est le principal, le joueur peut passer au le niveau
                if monster.monster_category=='main_monster':
                    self.game.pass_to_next_level=True
                    self.game.commets_rain=False
                    self.game.player.player_victory_marks+=4
                    # On joue l'audio correspondant au cri du monstre principal lorsqu'il meurt
                    pygame.time.wait(500) # pour laisser le temps a l'audio precedent de se terminer
                    self.game.main_monster_killed.play()
                    # On joue l'audio correspondant a la  victoire du joueur
                    self.game.player_winner.play()
                elif monster.monster_category=='simple_monster':
                    # On joue l'audio correspondant au cri d'un simple monstre lorsqu'il meurt
                    self.game.simple_monster_killed.play()
                self.game.game_all_monsters.remove(monster)
                self.game.player.player_victory_marks+=1


class Simple_Monster(Monsters):

    def __init__(self, game):
        super().__init__('simple_monster', game)

class Main_Monster(Monsters):
    def __init__(self, game):
        super().__init__('main_monster', game)