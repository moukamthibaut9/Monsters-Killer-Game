import pygame
import media_and_screen as ms


pygame.init()

class Bullets(pygame.sprite.Sprite):
    
    def __init__(self,direction,game):
        super().__init__()
        self.game=game
        self.bullet_direction=direction
        self.rect=pygame.Rect(self.game.player.rect.centerx,
                            self.game.player.rect.y+3*ms.cell_height,5*ms.cell_width,10*ms.cell_height)
        self.image=pygame.transform.scale(ms.loading_image('player_bullet.png'),(self.rect.w,self.rect.h))
        self.normal_image=self.image
        self.reverse_image=pygame.transform.flip(self.image,True,False)
        self.bullet_speed=2*ms.cell_width

    def delete_bullet(self):
        self.game.player.player_all_bullets.remove(self)

    def bliting_bullet(self):
        for bullet in self.game.player.player_all_bullets:
            self.game.screen.blit(bullet.image,bullet.rect)

    def moving_bullet(self):
        for bullet in self.game.player.player_all_bullets:
            # L'attribution de la direction des projectiles est gerée dans player.py: moving_player
            # lors de la ceration du nouvel objet Bullets
            if bullet.bullet_direction=='right':
                bullet.rect.x+=bullet.bullet_speed
            elif bullet.bullet_direction=='left':
                bullet.rect.x-=bullet.bullet_speed
            # Lorsqu'un projectile sort de la surface de jeu pendant son mouvement, on le supprime
            # et on décrémente le nombre de tirs du joueur
            if not -bullet.rect.w<=bullet.rect.x<=ms.screen_size[0]:
                bullet.delete_bullet()
                self.bullet_launched=False
                self.game.player.player_remaining_shots-=1
                if self.game.player.player_remaining_shots<0:
                    self.game.player.player_remaining_shots=0
            else:
                # s'il y a apparution des oiseaux kamikases et qu'un projectile du joueur en touche un 
                # Celui-ci explose et on reinitialise sa position
                if self.game.kamikase_birds.allow_kamikase_birds==True:
                    for rect in self.game.kamikase_birds.bird_rects:
                        if bullet.rect.colliderect(rect):
                            self.game.screen.blit(self.game.kamikase_birds.explosion_image,(rect.x,rect.y,
                                self.game.player.rect.w,self.game.player.rect.h))
                            rect.x=-35*ms.cell_width
                            self.game.player.player_victory_marks+=1
                            self.game.bird_killed.play()
                for monster in self.game.game_all_monsters:
                    # Lorsqu'un projectile entre en contact avec un monstre, on le supprime, 
                    # on décrémente le nombre de tirs du joueur et le sang du monstre diminu
                    # de facon adapté à la taille de l'écran
                    if bullet.rect.colliderect(monster.rect):
                        bullet.delete_bullet()
                        self.bullet_launched=False
                        self.game.player.player_remaining_shots-=1
                        if self.game.player.player_remaining_shots<0:
                            self.game.player.player_remaining_shots=0
                        if self.game.player.player_attack_marks>=\
                        (self.game.player.player_attack_marks/monster.monster_attack_marks)*3*0.6:
                            monster.monster_health_rect.w-=3*self.game.player.player_attack_marks
                        else:
                            monster.monster_health_rect.w-=3*3*self.game.player.player_attack_marks
                        if monster.monster_category=='main_monster':
                            # On joue l'audio correspondant au cri du monstre principal losrqu'il est fortement touché
                            self.game.main_monster_very_touched.play()
                        elif monster.monster_category=='simple_monster':
                            # On joue l'audio correspondant au cri d'un simple monstre losrqu'il est fortement touché
                            self.game.simple_monster_very_touched.play()
                        break


        