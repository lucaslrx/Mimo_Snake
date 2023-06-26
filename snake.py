import pygame
import random

# Initialisation de Pygame
pygame.init()
pygame.mixer.init()

# Définition des dimensions de l'écran
largeur_ecran = 640
hauteur_ecran = 480

police = pygame.font.Font("arial.ttf", 24)

# Création de la fenêtre de jeu
ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
pygame.display.set_caption("Snake Game")

# Chargement de l'image du pomelos
image_pomelos = pygame.image.load("pomelos1.png")
taille_cellule = 20
image_pomelos = pygame.transform.scale(image_pomelos, ((int(taille_cellule * 1.3)), (int(taille_cellule * 1.3))))

# Chargement de l'image de la boule de feu
image_fireball = pygame.image.load("fireball.png")
image_fireball = pygame.transform.scale(image_fireball, ((int(taille_cellule * 1.1)), (int(taille_cellule * 1.3))))

# Chargement de l'image de l'autruche
image_autruche = pygame.image.load("autruche.png")
image_autruche = pygame.transform.scale(image_autruche, (taille_cellule, taille_cellule * 2))

# Définition des couleurs
couleur_fond = (0, 0, 0)
couleur_snake = (0, 255, 0)

# Chargement de l'image de fond d'écran
image_fond = pygame.image.load("background.png")
image_fond = pygame.transform.scale(image_fond, (largeur_ecran, hauteur_ecran))

#son
son_pomelos = pygame.mixer.Sound("pomelos.wav")
son_autruche = pygame.mixer.Sound("autruche.wav")
son_boule_de_feu = pygame.mixer.Sound("boule_de_feu.wav")

# Classe pour la boule de feu
class BouleFeu:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.vitesse = 3

    def deplacer(self):
        if self.direction == "gauche":
            self.x -= self.vitesse
        elif self.direction == "droite":
            self.x += self.vitesse

    def afficher(self):
        ecran.blit(image_fireball, (self.x, self.y))

# Classe pour l'autruche
class Autruche:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vitesse = 5
        self.boule_feu = None

    def deplacer(self):
        self.y += self.vitesse
        if self.y <= 0 or self.y >= hauteur_ecran - taille_cellule * 2:
            self.vitesse *= -1

    def afficher(self):
        ecran.blit(image_autruche, (self.x, self.y))

    def lancer_boule_feu(self):
        if self.boule_feu is None:
            direction = random.choice(["gauche", "droite"])
            self.boule_feu = BouleFeu(self.x, self.y + taille_cellule, direction)
            son_autruche.play()

# Fonction principale du jeu
def afficher_score(longueur):
    texte = police.render("Pomelos: " + str(longueur), True, (255, 255, 255))
    ecran.blit(texte, (10, 10))

def enregistrer_highscore(score):
    with open("highscore.txt", "w") as fichier:
        fichier.write(str(score))

def charger_highscore():
    with open("highscore.txt", "r") as fichier:
        contenu = fichier.read()
        if contenu:
            return int(contenu)
        else:
            return 0


def jeu_snake():
    # Initialisation de la position et de la direction du serpent
    serpent_x = largeur_ecran // 2
    serpent_y = hauteur_ecran // 2
    direction_x = 0
    direction_y = 0

    #initialisation du high score
    high_score = charger_highscore()

    # Initialisation de la position de la pomelos
    pomelos_x = round(random.randrange(0, largeur_ecran - taille_cellule) / taille_cellule) * taille_cellule
    pomelos_y = round(random.randrange(0, hauteur_ecran - taille_cellule) / taille_cellule) * taille_cellule

    # Initialisation de la longueur du serpent
    serpent_longueur = 1
    serpent_corps = []
    serpent_vitesse = 15

    # Initialisation de l'autruche
    autruche = Autruche(random.randint(0, largeur_ecran - taille_cellule), random.randint(0, hauteur_ecran - taille_cellule * 2))

    # Variables de contrôle du jeu
    jeu_termine = False
    clock = pygame.time.Clock()

    # Boucle principale du jeu
    while not jeu_termine:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jeu_termine = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction_x = -taille_cellule
                    direction_y = 0
                elif event.key == pygame.K_RIGHT:
                    direction_x = taille_cellule
                    direction_y = 0
                elif event.key == pygame.K_UP:
                    direction_x = 0
                    direction_y = -taille_cellule
                elif event.key == pygame.K_DOWN:
                    direction_x = 0
                    direction_y = taille_cellule

        # Mise à jour de la position du serpent
        serpent_x += direction_x
        serpent_y += direction_y

        # Vérification des collisions avec les bords de l'écran
        if serpent_x >= largeur_ecran or serpent_x < 0 or serpent_y >= hauteur_ecran or serpent_y < 0:
            jeu_termine = True

        # Affichage de l'image de fond
        ecran.blit(image_fond, (0, 0))

        # Affichage de la pomelos
        ecran.blit(image_pomelos, (pomelos_x, pomelos_y))

        # Déplacement et affichage de l'autruche
        autruche.deplacer()
        autruche.afficher()

        # Vérification de la collision entre la boule de feu et le serpent
        if autruche.boule_feu is not None:
            autruche.boule_feu.deplacer()
            autruche.boule_feu.afficher()
           # if int(serpent_x) == int(autruche.boule_feu.x) and int(serpent_y) == int(autruche.boule_feu.y)
            if int(serpent_x) > int(autruche.boule_feu.x + -15) and int(serpent_x) < int(autruche.boule_feu.x + 15) and int(serpent_y) > int(autruche.boule_feu.y - 15) and int(serpent_y) < int(autruche.boule_feu.y + 15):
                son_boule_de_feu.play()
                jeu_termine = True
            if autruche.boule_feu.x < 0 or autruche.boule_feu.x >= largeur_ecran:
                autruche.boule_feu = None
        
        # Vérification de la collision entre la boule de feu et le serpent
            if int(serpent_x) > int(autruche.x + -15) and int(serpent_x) < int(autruche.x + 15) and int(serpent_y) > int(autruche.y - 15) and int(serpent_y) < int(autruche.y + 15):
                jeu_termine = True

        # Vérification de la collision avec la pomelos
        if serpent_x == pomelos_x and serpent_y == pomelos_y:
            pomelos_x = round(random.randrange(0, largeur_ecran - taille_cellule) / taille_cellule) * taille_cellule
            pomelos_y = round(random.randrange(0, hauteur_ecran - taille_cellule) / taille_cellule) * taille_cellule
            serpent_longueur += 1
            son_pomelos.play()
            enregistrer_highscore(serpent_longueur-1) 


        # Mise à jour du corps du serpent
        serpent_tete = []
        serpent_tete.append(serpent_x)
        serpent_tete.append(serpent_y)
        serpent_corps.append(serpent_tete)
        if len(serpent_corps) > serpent_longueur:
            del serpent_corps[0]

        # Vérification des collisions avec le corps du serpent
        for segment in serpent_corps[:-1]:
            if segment == serpent_tete:
                jeu_termine = True

        # Dessin du serpent
        for segment in serpent_corps:
            pygame.draw.rect(ecran, couleur_snake, [segment[0], segment[1], taille_cellule, taille_cellule])
        
        #affichage du high score
        texte_highscore = police.render("High Score: " + str(high_score), True, (255, 255, 255))
        rect_highscore = texte_highscore.get_rect()
        rect_highscore.topright = (largeur_ecran - 10, 10)
        ecran.blit(texte_highscore, rect_highscore)


        #affichage du score
        afficher_score(serpent_longueur-1)

        # Mise à jour de l'écran
        pygame.display.update()

        # Lancer une nouvelle boule de feu
        autruche.lancer_boule_feu()

        # Limite de vitesse du serpent
        clock.tick(serpent_vitesse)
    
    # Fermeture de la fenêtre Pygame
    pygame.quit()

# Lancement du jeu
jeu_snake()