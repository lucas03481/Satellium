import pygame
import sys
import random
import time

#on initialise pygame (logique t'es con)
pygame.init()

#Taille de la fenetre
largeur_fenetre = 1024
hauteur_fenetre = 768
fps = 144
blanc = (255, 255, 255)
noir = (0, 0, 0)
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Avions vs Aliens")



fond_image = pygame.image.load("fond.png")  
avion_image = pygame.image.load("avion.png")  
alien_image = pygame.image.load("alien.png") 
missile_image = pygame.image.load("missile.png") 
explosion_image = pygame.image.load("explosion.png")  

pygame.mixer.init()
son_monstre = pygame.mixer.Sound("monstre.mp3")
son_double_monstre = pygame.mixer.Sound("double_monstre.mp3")
son_triple_monstre = pygame.mixer.Sound("triple_monstre.mp3")
son_monstre_hurt = pygame.mixer.Sound("monstre_hurt.mp3")
son_blaster = pygame.mixer.Sound("blaster.mp3")
son_powerup = pygame.mixer.Sound("powerup.mp3")
son_powerup.play()
son_powerup.set_volume(0.5) 



# Redimensionnement des images(merci chatgpt tu gère bg)
fond_image = pygame.transform.scale(fond_image, (largeur_fenetre, hauteur_fenetre))
avion_image = pygame.transform.scale(avion_image, (50, 50))
alien_image = pygame.transform.scale(alien_image, (50, 50))
missile_image = pygame.transform.scale(missile_image, (20, 20))
explosion_image = pygame.transform.scale(explosion_image, (50, 50))

#affiche l'avion,alien,score
def afficher_avion(x, y):
    fenetre.blit(avion_image, (x, y))

#affiche un 
def afficher_alien(x, y):
    fenetre.blit(alien_image, (x, y))
#affiche un missile
def afficher_missile(x, y):
    fenetre.blit(missile_image, (x, y))

#affiche une explosion
def afficher_explosion(x, y):
    fenetre.blit(explosion_image, (x, y))

#affiche le 
def afficher_score(score):
    police = pygame.font.Font(None, 36)
    texte_score = police.render(f"Score: {score}", True, blanc)
    fenetre.blit(texte_score, (largeur_fenetre - 150, 10))

#boucle du jeu (truc qui permet de mettre invisible l'alien et la disparition du sang.)
def jeu():
    clock = pygame.time.Clock()

    avion_x = largeur_fenetre // 2 - 25
    avion_y = hauteur_fenetre - 100
    avion_vitesse = 4

    alien_x = random.randint(0, largeur_fenetre - 50)
    alien_y = 50
    alien_vitesse = 1 

    missile_x = 0
    missile_y = 0
    missile_vitesse = 7
    missile_etat = "pret"  
    explosion_etat = "invisible"  

    temps_explosion = 0
    temps_pause = 0
    temps_reapparition = 0
    temps_invisibilite = 0  
    duree_invisibilite = 1  
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        touches = pygame.key.get_pressed()
        if touches[pygame.K_LEFT] and avion_x > 0:
            avion_x -= avion_vitesse
        if touches[pygame.K_RIGHT] and avion_x < largeur_fenetre - 50:
            avion_x += avion_vitesse
        if touches[pygame.K_UP] and avion_y > 0:
            avion_y -= avion_vitesse
        if touches[pygame.K_DOWN] and avion_y < hauteur_fenetre - 100:
            avion_y += avion_vitesse
        if touches[pygame.K_SPACE] and missile_etat == "pret":
            missile_x = avion_x + 15  # Ajustez les coordonnées pour placer le missile au centre de l'avion
            missile_y = avion_y - 20  # Ajustez les coordonnées pour placer le missile juste au-dessus de l'avion
            missile_etat = "en_vol"
            explosion_etat = "invisible"
            son_blaster.play() 

        # Déplacement de l'alien
        if time.time() - temps_pause >= 1:
            alien_y += alien_vitesse
        if alien_y > hauteur_fenetre:
            alien_y = 0
            alien_x = random.randint(0, largeur_fenetre - 50)
            temps_reapparition = time.time()
            temps_invisibilite = time.time()  # Mettre à jour le temps d'invisibilité lors de la réapparition

        # Rendre l'alien invisible pendant la durée spécifiée
        if (
            temps_invisibilite > 0
            and time.time() - temps_invisibilite <= duree_invisibilite
        ):
            afficher_alien(-100, -100)  # Coordonnées hors de l'écran

        # Déplacement du missile
        if missile_etat == "en_vol":
            missile_y -= missile_vitesse
            if missile_y < 0:
                missile_etat = "pret"

        # Gestion des collisions
        if (
            alien_x < missile_x < alien_x + 50
            and alien_y < missile_y < alien_y + 50
            and missile_etat == "en_vol"
        ):
            explosion_etat = "visible"
            missile_etat = "pret"
            alien_y = 0
            alien_x = random.randint(0, largeur_fenetre - 50)
            temps_explosion = time.time()
            temps_pause = time.time()
            temps_invisibilite = time.time()  
            score += 1
        
         # Jouer le son en fonction du score
        
        if score == 1 and not pygame.mixer.get_busy():
            son_monstre.play()
        elif score == 5 and not pygame.mixer.get_busy():
            son_double_monstre.play()
        elif score == 10 and not pygame.mixer.get_busy():
            son_triple_monstre.play()

        # Affichage de l'explosion pendant 1 seconde
        if explosion_etat == "visible" and time.time() - temps_explosion >= 1:
            explosion_etat = "invisible"

        # Affichage du fond
        fenetre.blit(fond_image, (0, 0))

    

        # Affichage des éléments du jeu
        afficher_avion(avion_x, avion_y)
        afficher_alien(alien_x, alien_y)
        if missile_etat == "en_vol":
            afficher_missile(missile_x, missile_y)
        if explosion_etat == "visible":
            afficher_explosion(alien_x, alien_y)

        # Affichage du score
        afficher_score(score)

        pygame.display.flip()
        clock.tick(fps)

if __name__ == "__main__":
    jeu()
