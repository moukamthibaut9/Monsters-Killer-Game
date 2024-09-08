import pygame
import players
import monsters
import decor
import bullet
import bonus
import comets_rain
import kamikase_birds
import media_and_screen as ms
import time
import os
from random import randint


pygame.init()

def bliting_text(screen,text,text_rect,police,size,color):
    if os.path.exists('Polices/'+police+'.ttf'):
        font=pygame.font.Font('Polices/'+police+'.ttf',size)
    else:
        try: font=pygame.font.SysFont(police,size,False)
        except: font=pygame.font.SysFont('algerian',size,False)
    text=font.render(text,True,color)
    screen.blit(text,text_rect)

class Game:

    def __init__(self,screen):
        self.screen=screen
        # Chargement de tous les audios qui seront joués pendant le jeu
            # Pour le joueur
        self.player_little_touched=ms.loading_sound('player_little_touched.wav')
        self.player_very_touched=ms.loading_sound('player_very_touched.wav')
        self.player_winner=ms.loading_sound('player_winner.wav')
        self.player_killed=ms.loading_sound('player_killed.wav')
        self.player_has_shot=ms.loading_sound('player_has_shot.wav')

        self.player_very_touched.set_volume(0.2)
            # Pour les monstres
        self.main_monster_little_touched=ms.loading_sound('main_monster_little_touched.wav')
        self.main_monster_very_touched=ms.loading_sound('main_monster_very_touched.wav')
        self.simple_monster_little_touched=ms.loading_sound('simple_monster_little_touched.wav')
        self.simple_monster_very_touched=ms.loading_sound('simple_monster_very_touched.wav')
        self.main_monster_killed=ms.loading_sound('main_monster_killed.wav')
        self.simple_monster_killed=ms.loading_sound('simple_monster_killed.wav')
            # Pour les oiseaux kamikases
        self.bird_killed=ms.loading_sound('bird_killed.wav')
            # Pour les bonus
        self.shield_bonus=ms.loading_sound('shield_bonus.wav')
        self.health_bonus=ms.loading_sound('health_bonus.wav')
            # Pour le jeu
        if os.path.exists('Sounds/game_sound.mp3'):
            pygame.mixer.music.load('Sounds/game_sound.mp3')
            if os.path.exists('Sounds/game_sound2.mp3'):
                pygame.mixer.music.queue('Sounds/game_sound2.mp3')
            pygame.mixer.music.set_volume(0.3)
            self.sound_position=0
        # Definition du temps auquel le jeu est initialisé (en double de secondes)
        self.game_start_time1=time.time()//2 # Permet de controler l'attribution des projectiles au joueur
        self.game_start_time2=time.time()//2 # Permet de controler l'intervalle de temps entre deux generations de monstres
        self.game_start_time3=time.time()//2 # Permet de controler l'intervalle de temps entre deux generations de bonus
        self.game_start_time4=time.time()//2 # Permet de controler la duree pendant laquelle le joueur ne peut subir de degats
        self.game_start_time5=time.time()//2 # Permet de controler la variation  de la barre de blindage du joueur lorsque celui-ci est blindé
        self.game_start_time6=time.time()//2 # Permet de controler l'apparution des oiseaux kamikases lorsque le joueur reste trop lomptemps sur une plateforme
        # Definition du temps actuel (en double de secondes)
        self.game_actual_time=time.time()//2
        # Definition de l'espace dans lequel le joueur peut se deplacer
        self.game__space_rect = pygame.Rect(0, -20*ms.cell_height, ms.screen_size[0], ms.screen_size[1]+20*ms.cell_height)
        # Definition d'un dictionnaire qui contiendra des donnees du joueur: nom, score et niveau
        self.player_data_save_dico={}
        # En rapport avec le nom du joueur
        self.player_name=""
        self.player_name_rect=pygame.Rect(50*ms.cell_width,10*ms.cell_height,50*ms.cell_width,6*ms.cell_height)
        self.player_name_rect_is_activated=[False,(0,255,0)]
        # En rapport avec les avatars du joueurs du joueur
        self.selected_avatar='player'
        self.player_avatars=[ms.loading_image('avatar_player1.png'),ms.loading_image('avatar_player2.png')]
        self.player_avatars_rects=[
                            pygame.Rect(30*ms.cell_width,27*ms.cell_height,30*ms.cell_width,50*ms.cell_height),
                            pygame.Rect(90*ms.cell_width,27*ms.cell_height,30*ms.cell_width,50*ms.cell_height)
                        ]
        self.player_avatars_rects_is_activated=[[False,(0,255,0)],[False,(0,255,0)]]
         # En rapport avec le choix de commencer ou continuer le jeu
        self.player_remenber_rects=[
                            pygame.Rect(10*ms.cell_width,84*ms.cell_height,30*ms.cell_width,7*ms.cell_height),
                            pygame.Rect(60*ms.cell_width,84*ms.cell_height,30*ms.cell_width,7*ms.cell_height)
                        ]
        self.player_remenber_rects_is_activated=[[False,(0,255,0)],[False,(0,255,0)]]
        # En rapport avec le lancement de la partie
        self.launch_game_rect=pygame.Rect(124*ms.cell_width,84*ms.cell_height,25*ms.cell_width,7*ms.cell_height)
        self.configuration_error=False
        # En rapport avec le score, le niveau, et l'option de mise en pause(menu)
        self.score_rect=pygame.Rect(127*ms.cell_width,0,20*ms.cell_width,4*ms.cell_height)
        self.level_rect=pygame.Rect(129*ms.cell_width,4*ms.cell_height,15*ms.cell_width,4*ms.cell_height)
        self.pass_level_rect=pygame.Rect(98*ms.cell_width,84*ms.cell_height,42*ms.cell_width,7*ms.cell_height)
        self.pass_to_next_level=False
        self.game_level=1
        self.paused_rect=pygame.Rect(144*ms.cell_width,0,5.8*ms.cell_width,8*ms.cell_height)
        self.click_on_paused_rect=False
        # Autres
        self.actual_monsters_nbr=1
        self.game_all_monsters=[]
        self.player_collision_with_monster=False
        self.player_moving_autorised=True
        self.game_all_bonus=[]
        self.bliting_bonus=False
        # Initialisation du joueur, du decor,  des projctiles du joueur, des enemies et des bonus
        self.player=players.Player1(self.player_name,self)
        self.decor=decor.Decor(self)
        self.bullet=bullet.Bullets(self.player.player_direction[1],self)
        self.monster=monsters.Monsters('simple_monster',self)
        self.player.player_all_bullets.append(self.bullet)
        self.bonus=bonus.Bonus('health_bonus',self)
        self.comets_rain=comets_rain.Comets_Rain(self)
        self.kamikase_birds=kamikase_birds.Kamikase_Birds(self)


    def bliting_all(self):
        # Affichage de l'arriere plan et des differentes plateformes
        self.decor.bliting_decor(self.screen)
        # Affichage du nombre de tirs restant au joueur (Augmente apres 30 secondes)
        bliting_text(self.screen,"Shots: "+str(self.player.player_remaining_shots),
            (12*ms.cell_width,0,13*ms.cell_width,3*ms.cell_height),'Algerian',4*ms.cell_width,(255,255,255))
        # Affichage du score
        bliting_text(self.screen,"Score:"+str(self.player.player_victory_marks),
            self.score_rect,'Commic Sans s',5*ms.cell_width,(255,255,255))
        # Affichage du niveau de jeu
        bliting_text(self.screen,"Level: "+str(self.game_level),
            self.level_rect,'Commic Sans S',5*ms.cell_width,(255,0,255))
        # Affichage concernant la mise en pause
        pygame.draw.rect(self.screen,(255,255,255),self.paused_rect,5)
        bliting_text(self.screen,"| |",(145*ms.cell_width,0,3*ms.cell_width,5*ms.cell_height),
                     'Roboto-Black',5*ms.cell_width,(0,0,0))
        # Affichage du joueur et rectriction de ses deplacements a l'espace de jeu
        self.player.bliting_player()
        self.player.rect.clamp_ip(self.game__space_rect)
        # Affichage des monstres
        self.monster.bliting_monter()
        # Affichage des projectiles du joueur
        if self.player.player_bullet_launched==True and self.player.player_remaining_shots>0:
            self.bullet.bliting_bullet()
        # Affichage des cometes de feu
        if self.comets_rain.allow_comets_rain==True:
            self.comets_rain.bliting_comets()
        # Affichage des oiseaux kamikases
        if self.kamikase_birds.allow_kamikase_birds==True:
            self.kamikase_birds.bliting_birds()
        # Affichage du bonus
        if self.bliting_bonus==True:
            self.bonus.bliting_bonus()

    def moving_all(self):
        # Redefinition du temps actuel (en vingtaine de secondes)
        self.game_actual_time=time.time()//2
        # On verifie si 12 secondes se sont deja ecoulée afin d'incrémenter le nombre de tirs du joueur
        if (self.game_actual_time-self.game_start_time1)!=0 and (self.game_actual_time-self.game_start_time1)%6==0:
            self.player.player_remaining_shots+=5
            self.game_start_time1=self.game_actual_time # On redefinit le point de controle du temps 1 au temps actuel
        # Si 20 secondes se sont ecoulées et que le joueur est au dessus des plateformes les plus basses du jeu,
        # On permet l'apparution des oiseaux kamikases
        if self.player.rect.bottom<=self.decor.supports_rects[0].y+ms.cell_height \
        and (self.game_actual_time-self.game_start_time6)!=0 \
        and (self.game_actual_time-self.game_start_time6)%10==0:
            self.kamikase_birds.allow_kamikase_birds=True
            self.game_start_time6=self.game_actual_time # On redefinit le point de controle du temps 6 au temps actuel
        elif self.player.rect.bottom>=87*ms.cell_height:
            for rect in self.kamikase_birds.bird_rects:
                if rect.right<=0:
                    self.kamikase_birds.allow_kamikase_birds=False
                    break
        # On verifie si le joueur a tiré et si son nombre de tirs est valide avant de déplacer les projectiles
        if self.player.player_bullet_launched==True and self.player.player_remaining_shots>0:
            self.bullet.moving_bullet()
        # Deplacement controlé des cometes du jeu
        if self.comets_rain.allow_comets_rain==True:
            self.comets_rain.moving_comets()
        # Deplacement controlé des oiseaux kamikases du jeu
        if self.kamikase_birds.allow_kamikase_birds==True:
            self.kamikase_birds.moving_birds()
        # On verififie le niveau actuel du jeu avant d'effectuer une génération de monstre en 
        # fonction de celui-ci ( Cette génération est controlée)
        if self.game_level==1:
            self.monsters_generation_controled(0.5,200,160)# (1,200,160)
        elif self.game_level==2:
            self.monsters_generation_controled(1,175,145)# (1,175,145)
        elif self.game_level==3:
            self.monsters_generation_controled(1,150,120)# (2,150,120)
        elif self.game_level==4:
            self.monsters_generation_controled(1,125,100)# (1,200,175)
        # Gestion de la generation de bonus (Apres toutes les 60 secondes: niveau 1 et 2; 30 secondes: autres niveaux )
        if self.game_level in [1,2,3]:
            self.bonus_generation_controled(30)
        else:
            self.bonus_generation_controled(15)

        # Si 2*X secondes se sont écoulées depuis que je joueur a touché à un blindage, il pert son invincibilité
        # (X ici correspond au parametre 'decrease_nbr_for_end_player_shield_rect')
        if (self.game_actual_time-self.game_start_time4)!=0 \
        and (self.game_actual_time-self.game_start_time4)%self.player.decrease_nbr_for_end_player_shield_rect==0 \
        and self.player.player_shielded==True:
            self.player.player_shielded=False

        # Gestion du passage du joueur au niveau suivant
        if self.pass_to_next_level:
            if os.path.exists('Sounds/game_sound.mp3'):
                self.sound_position=pygame.mixer.music.get_pos()
                pygame.mixer.music.stop()
        while self.pass_to_next_level:
            # Et recupere la position actuelle du son du jeu et on le stoppe
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    if os.path.exists("Images/terrain"+str(self.game_level+1)+".jpg"):
                        self.game_level+=1
                    # Sauvegarde des donnees du joueur s'il decide de quitter le jeu
                    ms.saving_player_data(self.player_data_save_dico,self.player_name,self.player.player_victory_marks,
                                    self.game_level,'player_data_save_file.txt')
                    self.pass_to_next_level=False
                    pygame.quit()
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if self.pass_level_rect.collidepoint(event.pos):
                        if os.path.exists("Images/terrain"+str(self.game_level+1)+".jpg"):
                            # On reinitialise la position des cometes
                            for i in range(len(self.comets_rain.comet_rects)):
                                self.comets_rain.comet_rects[i].x=randint(20*i,23*(i+1))*ms.cell_width
                                self.comets_rain.comet_rects[i].y=randint(-30,-10)*ms.cell_height
                            # On reinitialise la position des oiseaux kamikases
                            for i in range(len(self.kamikase_birds.bird_rects)):
                                self.kamikase_birds.bird_rects[i].x=randint(-50,-25)*ms.cell_width
                            # On reinitialise d'autres parametres
                            self.player.player_health_marks_rect.w=self.player.player_max_health_marks_rect.w
                            self.player.player_victory_marks=0
                            self.player.player_direction=[0,'right']
                            self.player.player_state='stand_up'
                            self.player.rect.x=ms.cell_width
                            self.player.rect.bottom=87*ms.cell_height
                            self.actual_monsters_nbr=1
                            self.game_level+=1
                            self.game_all_monsters.clear()
                            self.decor.bg_img = ms.loading_image("terrain"+str(self.game_level)+".jpg")
                            self.player.player_bullet_launched=False
                            self.player.player_attack_marks=ms.cell_width/self.game_level
                            self.pass_to_next_level=False
                            self.comets_rain.allow_comets_rain=False
                            self.kamikase_birds.allow_kamikase_birds=False
                            self.game_all_bonus.clear()
                            self.bliting_bonus=False
                            self.player.player_shielded=False
                            self.player.player_shield_rect.w=0
                            pygame.time.wait(1000)
                            # On reprend le son du jeu on on s'est arreté
                            if os.path.exists('Sounds/game_sound.mp3'):
                                pygame.mixer.music.play(loops=-1)
                        else:
                            # Sauvegarde des données du joueur s'il a terminé le jeu et qu'il led quitte
                            ms.saving_player_data(self.player_data_save_dico,self.player_name,self.player.player_victory_marks,
                                    self.game_level,'player_data_save_file.txt')
                            self.pass_to_next_level=False
                            pygame.quit()
            self.screen.fill((192,192,192))
            pygame.draw.rect(self.screen,(0,0,255),self.pass_level_rect,3)
            if os.path.exists("Images/terrain"+str(self.game_level+1)+".jpg"):
                bliting_text(self.screen,"WINNER",
                            (50*ms.cell_width,10*ms.cell_height,50*ms.cell_width,15*ms.cell_height),
                            'Algerian',20*ms.cell_width,(0,0,255))
                bliting_text(self.screen,"Passer au niveau suivant",
                            (100*ms.cell_width,85*ms.cell_height,40*ms.cell_width,5*ms.cell_height),
                            'Times New Roman',4*ms.cell_width,(255,0,255))
            else:
                bliting_text(self.screen,"CONGRATULATIONS",
                            (3*ms.cell_width,15*ms.cell_height,125*ms.cell_width,15*ms.cell_height),
                            'Algerian',20*ms.cell_width,(255,255,255))
                bliting_text(self.screen,"Vous avez terminé le jeu",
                            (100*ms.cell_width,85*ms.cell_height,40*ms.cell_width,5*ms.cell_height),
                            'Times New Roman',4*ms.cell_width,(255,0,255))
            pygame.display.flip()
            pygame.display.update()
                
        # Deplacement des enemies
        self.monster.moving_monster()
        # Lorsque le joueur se deplace
        self.player.moving_player()
        # Gestions des collisions avec les differents supports ou le sol du jeu pour le joueur 1
        for i in range(len(self.decor.supports_rects)):
            if (self.player.rect.bottom==self.decor.supports_rects[i].top+ms.cell_height \
            and self.decor.supports_rects[i].left-self.player.rect.w/1.5<self.player.rect.x \
            and self.player.rect.x<self.decor.supports_rects[i].right-self.player.rect.w/3) \
            or self.player.rect.bottom>=87*ms.cell_height:
                self.player.player_jump_down_continious=False
                self.player.player_on_some_support=True
                break
            elif i==len(self.decor.supports_rects)-1:
                self.player.player_jump_down_continious=True
                self.player.player_on_some_support=False
        if self.player.player_on_some_support==True:
            self.player.player_jump=False
            self.player.player_jump_up_index=0
            self.player.player_jump_down_index=self.player.player_jump_nbr
        
        # Gestion de la mort du joueur
        if self.player.player_alive==False:
            # On joue l'audio correspondant a la mort du joueur
            pygame.time.wait(500) # pour laisser le temps a l'audio precedent de se terminer
            self.player_killed.play()
            pygame.time.wait(900)
            if os.path.exists('Sounds/game_sound.mp3'):
                self.sound_position=pygame.mixer.music.get_pos()
                pygame.mixer.music.stop()
            while self.player.player_alive==False:
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        # Sauvegarde des donnees du joueur s'il decide de quitter le jeu
                        ms.saving_player_data(self.player_data_save_dico,self.player_name,self.player.player_victory_marks,
                                        self.game_level,'player_data_save_file.txt')
                        self.player.player_alive=True
                        pygame.quit()
                    if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_q:
                            ms.saving_player_data(self.player_data_save_dico,self.player_name,
                                            self.player.player_victory_marks,
                                            self.game_level,'player_data_save_file.txt')
                            self.player.player_alive=True
                            pygame.quit()
                        if event.key==pygame.K_r:
                            # On reinitialise la position des cometes
                            for i in range(len(self.comets_rain.comet_rects)):
                                self.comets_rain.comet_rects[i].x=randint(20*i,23*(i+1))*ms.cell_width
                                self.comets_rain.comet_rects[i].y=randint(-30,-10)*ms.cell_height
                            # On reinitialise la position des oiseaux kamikases
                            for i in range(len(self.kamikase_birds.bird_rects)):
                                self.kamikase_birds.bird_rects[i].x=randint(-50,-25)*ms.cell_width
                            # On reinitialise d'autres parametres
                            self.player.player_health_marks_rect.w=self.player.player_max_health_marks_rect.w
                            self.player.player_victory_marks=0
                            self.player.player_remaining_shots=0
                            self.player.player_direction=[0,'right']
                            self.player.player_state='stand_up'
                            self.player.rect.x=ms.cell_width
                            self.player.rect.bottom=87*ms.cell_height
                            self.actual_monsters_nbr=1
                            self.game_all_monsters.clear()
                            self.player.player_all_bullets.clear()
                            self.player.player_bullet_launched=False
                            self.player.player_alive=True
                            self.comets_rain.allow_comets_rain=False
                            self.kamikase_birds.allow_kamikase_birds=False
                            self.game_all_bonus.clear()
                            self.bliting_bonus=False
                            self.player.player_shielded=False
                            self.player.player_shield_rect.w=0
                            if os.path.exists('Sounds/game_sound.mp3'):
                                pygame.mixer.music.play(loops=-1)

                self.screen.fill((192,192,192))
                bliting_text(self.screen,"FAILED",
                            (50*ms.cell_width,10*ms.cell_height,50*ms.cell_width,15*ms.cell_height),
                            'Algerian',20*ms.cell_width,(0,0,0))
                bliting_text(self.screen,"Appuiyez sur 'R' pour recommencer.",
                            (15*ms.cell_width,50*ms.cell_height,130*ms.cell_width,10*ms.cell_height),
                            'narrow',10*ms.cell_width,(0,0,255))
                bliting_text(self.screen,"Appuiyez sur 'Q' pour quitter.",
                            (25*ms.cell_width,80*ms.cell_height,125*ms.cell_width,10*ms.cell_height),
                            'narrow',10*ms.cell_width,(0,0,255))
                pygame.display.flip()
                pygame.display.update()

    def monsters_generation_controled(self,time_moduler,max_monsters_autorised,min_monster_before_final):
        """
        Cette fonction permet la génération de montres de facon controlée.
            Les monstres sont générés après un certain temps et la génération est stopée si
        le nombre de monstres déjà généré a atteint un certain seuil.
            Aussi, la génération du monstre principal ne se fait que si un nombre minimal de
        monstres simples a déjà été généré
            Le paramètre 'time_moduler' controle le temps avant génération d'un nouveau monstre,il doit etre
        supérieur à 0 (plus il est grand, plus il faudra du temps avant génération d'un nouveau monstre: 
        il est multiplie par 2)
        """
        if (self.game_actual_time-self.game_start_time2)!=0 \
        and (self.game_actual_time-self.game_start_time2)%time_moduler==0 \
        and self.actual_monsters_nbr<=max_monsters_autorised and self.player.rect.bottom>=87*ms.cell_height:
            new_simple_monster=monsters.Monsters('simple_monster',self)
            self.game_all_monsters.append(new_simple_monster)
            self.actual_monsters_nbr+=1
            if self.actual_monsters_nbr==min_monster_before_final: 
                new_main_monster=monsters.Monsters('main_monster',self)
                self.game_all_monsters.append(new_main_monster)
                # Apres génération du monstre principal, on active une pluie de comètes dans le jeu
                self.comets_rain.allow_comets_rain=True
                self.actual_monsters_nbr+=1
            self.game_start_time2=self.game_actual_time # On redefinit le point de controle du temps 2 au temps actuel


    def bonus_generation_controled(self,time_moduler):
        """
            Cette fonction permet la génération de bonus de facon controlée.
            Les bonus sont générés après un certain temps. Le paramètre 'time_moduler' controle
        le temps avant génération d'un nouveau bonus,il doit etre supérieur à 0 (plus il est grand, 
        plus il faudra du temps avant génération d'un nouveau bonus: il est multiplie par 2)
        """
        if (self.game_actual_time-self.game_start_time3)!=0 \
        and (self.game_actual_time-self.game_start_time3)%time_moduler==0:
            self.game_all_bonus.clear() # On vide d'abord la liste des bonus avant d'ajouter un autre
            selected_bonus=randint(1,2) # Ce parametre va permettre de choisir un bonus a ajouter au hasard
            if selected_bonus==1:
                new_bonus=bonus.Bonus('health_bonus',self)
            elif selected_bonus==2:
                new_bonus=bonus.Bonus('shield_bonus',self)
            self.game_all_bonus.append(new_bonus)
            self.bliting_bonus=True
            self.game_start_time3=self.game_actual_time # On redefinit le point de controle du temps 3 au temps actuel
