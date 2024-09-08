import pygame
from players import Player2
from decor import Decor
from monsters import Monsters
import game_play
import media_and_screen as ms
import sys
import os
import string
import pickle
from random import randint


pygame.init()


fps = pygame.time.Clock()

screen = pygame.display.set_mode(ms.screen_size)
pygame.display.set_caption("Aliens_Killer_Game")


game=game_play.Game(screen)
game_configuration=True
game_launched=True

# Configuration du joueur
while game_configuration:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Sauvegarde des donnees du joueur s'il decide de quitter le jeu
            #ms.saving_player_data(game.player_data_save_dico,game.player_name,game.player.player_victory_marks,
            #                    game.game_level,'player_data_save_file.txt')
            game_configuration = False
            game_launched = False
            pygame.time.wait(1000)
        if event.type == pygame.KEYDOWN:
            if game.player_name_rect_is_activated[0] == True:
                if event.key == pygame.K_BACKSPACE:
                    game.player_name = game.player_name[:-1]
                else:
                    if len(game.player_name)<12:
                        game.player_name += event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Verification du clic sur la zone du nom
            if game.player_name_rect.collidepoint(event.pos):
                game.player_name_rect_is_activated = [True,(0,0,255)]
            else:
                game.player_name_rect_is_activated = [False,(0,255,0)]
            # Verification du clic sur un avatar
            for i in range(len(game.player_avatars_rects)):
                if game.player_avatars_rects[i].collidepoint(event.pos):
                    game.player_avatars_rects_is_activated[i] = [True,(0,0,255)]
                    game.selected_avatar = 'player' + str(i+1)
                    for j in range(len(game.player_avatars_rects)):
                        if j != i:
                            game.player_avatars_rects_is_activated[j] = [False,(0,255,0)]
                    break
            # Verification du clic sur un des choix commencer ou continuer le jeu
                if game.player_remenber_rects[0].collidepoint(event.pos):
                    game.player_remenber_rects_is_activated[0] = [True,(0,0,255)]
                    game.player_remenber_rects_is_activated[1] = [False,(0,255,0)]
                elif game.player_remenber_rects[1].collidepoint(event.pos):
                    game.player_remenber_rects_is_activated[1] = [True,(0,0,255)]
                    game.player_remenber_rects_is_activated[0] = [False,(0,255,0)]
            # Verification du clic sur la zone de lancement du jeu
            if game.launch_game_rect.collidepoint(event.pos):
                if len(game.player_name)>=3:
                        for letter in game.player_name:
                            if letter not in string.ascii_letters:
                                game.player_name_rect_is_activated[1] = (255,0,0)
                                game.configuration_error = True
                                break
                        if game.player_name_rect_is_activated[1] in [(0,0,255),(0,255,0)]:
                            game.player_name_rect_is_activated = [False,(0,255,0)]
                            game.configuration_error = False
                else:
                    game.player_name_rect_is_activated[1] = (255,0,0)
                    game.configuration_error = True
                # Recuperation des donnees des joueurs depuis la derniere partie
                if os.path.exists('player_data_save_file.txt'):
                    with open(os.path.join('player_data_save_file.txt'),'rb') as player_data_save_file:
                        data_recovering = pickle.Unpickler(player_data_save_file)
                        game.player_data_save_dico = data_recovering.load()
                    if game.player_name.lower() in game.player_data_save_dico.keys():
                        if game.player_remenber_rects_is_activated[0][0] == True \
                        or game.player_remenber_rects_is_activated[1][0] == False:   
                            game.player_name_rect_is_activated[1] = (255,0,0)
                            game.configuration_error = True
                        elif game.player_remenber_rects_is_activated[1][0] == True:
                            game.game_level = game.player_data_save_dico[game.player_name][1]
                if game.configuration_error == False:
                    if game.selected_avatar == 'player2':
                        game.player = Player2(game.player_name,game)
                    # On reinstancie certaines objets du jeu et on ajuste les degats que le joueur 
                    # peut causer au monstre en fonction du niveau de jeu
                    game.player.player_attack_marks=ms.cell_width/game.game_level
                    game.decor = Decor(game)
                    game.monster = Monsters('simple_monster',game)
                    # Lorsque le joueur lance le jeu, on change la couleur du rectangle de lancement
                    pygame.draw.rect(screen,(255,255,255),game.launch_game_rect,1)
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    game_configuration = False
                    pygame.mixer.music.play(loops=-1)
    
    screen.fill((0,0,0))
    # Affichage concernant le nom du joueur
    game_play.bliting_text(screen,"Avant de commencer, entrer un nom d'utilisateur(Min: 3 lettres; Max: 12 lettres)",
                    (10*ms.cell_width,3*ms.cell_height,130*ms.cell_width,5*ms.cell_height),'Times New Roman',
                    4*ms.cell_width,(255,255,255))
    pygame.draw.rect(screen,game.player_name_rect_is_activated[1],game.player_name_rect,1)
    game_play.bliting_text(screen,game.player_name,
                        (51*ms.cell_width,10*ms.cell_height,50*ms.cell_width,5*ms.cell_height),
                        'arial',4*ms.cell_width,(255,255,0))
    # Affichage concernant les avatars possibles du joueur
    game_play.bliting_text(screen,"Selectionner un avatar",
                (57*ms.cell_width,20*ms.cell_height,100*ms.cell_width,5*ms.cell_height),'Times New Roman',
                4*ms.cell_width,(255,255,255))
    for i in range(len(game.player_avatars_rects)):
        game.player_avatars[i] = pygame.transform.scale(game.player_avatars[i],
                                                (game.player_avatars_rects[i].w,game.player_avatars_rects[i].h))
        screen.blit(game.player_avatars[i],game.player_avatars_rects[i])
        pygame.draw.rect(screen,game.player_avatars_rects_is_activated[i][1],game.player_avatars_rects[i],2)
    # Affichage concernant le choix de commencer ou continuer le jeu
    game_play.bliting_text(screen,"Commnencer",
                        (15*ms.cell_width,85*ms.cell_height,45*ms.cell_width,5*ms.cell_height),
                        'Times New Roman',4*ms.cell_width,(255,255,255))
    pygame.draw.rect(screen,game.player_remenber_rects_is_activated[0][1],game.player_remenber_rects[0],1)
    game_play.bliting_text(screen,"Continuer",
                        (67*ms.cell_width,85*ms.cell_height,30*ms.cell_width,5*ms.cell_height),
                        'Times New Roman',4*ms.cell_width,(255,255,255))
    pygame.draw.rect(screen,game.player_remenber_rects_is_activated[1][1],game.player_remenber_rects[1],1)
    # Affichage concernant le lancement de la partie
    game_play.bliting_text(screen,"Lancer le jeu",
                        (126*ms.cell_width,85*ms.cell_height,20*ms.cell_width,5*ms.cell_height),
                        'Times New Roman',4*ms.cell_width,(255,0,255))
    pygame.draw.rect(screen,(0,255,0),game.launch_game_rect,1)
    # Affichage en cas d'erreur dans le nom du joueur
    if game.configuration_error == True:
        game_play.bliting_text(screen,"Le nom saisi est déjà pris ou rencontre un problème",
                            (5*ms.cell_width,92*ms.cell_height,140*ms.cell_width,8*ms.cell_height),
                            'narrow',8*ms.cell_width,(255,0,0))
    pygame.display.flip()
    pygame.display.update()
    fps.tick(60)

# Lancement du jeu
while game_launched:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Sauvegarde des donnees du joueur s'il decide de quitter le jeu
            ms.saving_player_data(game.player_data_save_dico,game.player_name,game.player.player_victory_marks,
                                game.game_level,'player_data_save_file.txt')
            game_launched = False
            pygame.time.wait(1000)
        if event.type == pygame.KEYDOWN:
            game.player.pressed_button[event.key]=True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                game.player.player_direction[0] = 1
                game.player.player_state = 'running'
                game.player.player_direction[1] = 'right'
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                game.player.player_direction[0] = -1
                game.player.player_state = 'running'
                game.player.player_direction[1] = 'left'
            if event.key == pygame.K_SPACE:
                game.player.player_state = 'attack'
            # Lorsque le joueur saute
            if (event.key == pygame.K_UP or event.key == pygame.K_w):
                if game.player.player_jump_down_continious == False:
                    game.player.player_jump = True
        if event.type == pygame.KEYUP:
            game.player.pressed_button[event.key]=False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                game.player.player_direction[0] = 0
                game.player.player_state = 'stand_up'
                game.player.player_direction[1] = 'right'
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                game.player.player_direction[0] = 0
                game.player.player_state = 'stand_up'
                game.player.player_direction[1] = 'left'
            if event.key == pygame.K_SPACE:
                game.player.player_direction[0] = 0
                game.player.player_state = 'stand_up'
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game.paused_rect.collidepoint(event.pos):
                game.click_on_paused_rect = True

    # Instructions a executer au cas ou le joueur a cliquer sur le boutton 'PAUSE'
    if game.click_on_paused_rect:
        if os.path.exists('Sounds/game_sound.mp3'):
            game.sound_position=pygame.mixer.music.get_pos()
            pygame.mixer.music.stop()
    while game.click_on_paused_rect:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                # Sauvegarde des donnees du joueur s'il decide de quitter le jeu
                ms.saving_player_data(game.player_data_save_dico,game.player_name,game.player.player_victory_marks,
                                game.game_level,'player_data_save_file.txt')
                game_is_actif = False
                game_launched = False
                game.click_on_paused_rect=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:
                    # Sauvegarde des donnees du joueur s'il decide de quitter le jeu
                    ms.saving_player_data(game.player_data_save_dico,game.player_name,
                                        game.player.player_victory_marks,game.game_level,
                                        'player_data_save_file.txt')
                    game_is_actif = False
                    game_launched = False
                    game.click_on_paused_rect=False
                elif event.key==pygame.K_r:
                    # On reinitialise la position des cometes
                    for i in range(len(game.comets_rain.comet_rects)):
                        game.comets_rain.comet_rects[i].x=randint(20*i,23*(i+1))*ms.cell_width
                        game.comets_rain.comet_rects[i].y=randint(-30,-10)*ms.cell_height
                    # On reinitialise la position des oiseaux kamikases
                    for i in range(len(game.kamikase_birds.bird_rects)):
                        game.kamikase_birds.bird_rects[i].x=randint(-50,-25)*ms.cell_width
                    # On reinitialise d'autres parametres
                    game.player.player_health_marks_rect.w=game.player.player_max_health_marks_rect.w
                    game.player.player_victory_marks=0
                    game.player.player_remaining_shots=0
                    game.player.player_direction=[0,'right']
                    game.player.player_state='stand_up'
                    game.player.rect.x=ms.cell_width
                    game.player.rect.bottom=87*ms.cell_height
                    game.actual_monsters_nbr=1
                    game.game_all_monsters.clear()
                    game.player.player_all_bullets.clear()
                    game.player.player_bullet_launched=False
                    game.player.player_alive=True
                    game.player.player_shielded=False
                    game.game_all_bonus.clear()
                    game.bliting_bonus=False
                    game.comets_rain.allow_comets_rain=False
                    game.kamikase_birds.allow_kamikase_birds=False
                    game.player.player_shield_rect.w=0
                    if os.path.exists('Sounds/game_sound.mp3'):
                        pygame.mixer.music.play(loops=-1)
                    game.click_on_paused_rect=False
                elif event.key==pygame.K_c:
                    game.click_on_paused_rect=False
                    if os.path.exists('Sounds/game_sound.mp3'):
                        pygame.mixer.music.play(loops=-1,start=game.sound_position/1000)
        screen.fill((192,192,192))
        game_play.bliting_text(screen,"PAUSE",(55*ms.cell_width,5*ms.cell_height,50*ms.cell_width,15*ms.cell_height),
                        'Algerian',20*ms.cell_width,(255,0,255))
        game_play.bliting_text(screen,"Appuiyez sur 'C' pour continuer la partie.",
                        (5*ms.cell_width,30*ms.cell_height,140*ms.cell_width,8*ms.cell_height),
                        'narrow',10*ms.cell_width,(0,0,255))
        game_play.bliting_text(screen,"Appuiyez sur 'R' pour recommncer.",
                        (15*ms.cell_width,45*ms.cell_height,130*ms.cell_width,10*ms.cell_height),
                        'narrow',10*ms.cell_width,(0,0,255))
        game_play.bliting_text(screen,"Appuiyez sur 'Q' pour quitter.",
                        (25*ms.cell_width,60*ms.cell_height,125*ms.cell_width,10*ms.cell_height),
                        'narrow',10*ms.cell_width,(0,0,255))
        pygame.display.flip()
        pygame.display.update()
        fps.tick(60)
    # Fin des instructions consernant la 'PAUSE'

    screen.fill((0,0,0))
    game.bliting_all()
    game.moving_all()
    pygame.display.flip()
    pygame.display.update()
    fps.tick(60)

pygame.quit()
sys.exit()