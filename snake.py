import pygame
import random

# Initialisation de Pygame
pygame.init()
pygame.mixer.init()

# Définition des dimensions de l'écran
largeur_ecran = 640
hauteur_ecran = 480

police = pygame.font.Font("tools/Arial.ttf", 24)

# Création de la fenêtre de jeu
ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
pygame.display.set_caption("Snake Game")

# Chargement de l'image de la pomelos
taille_cellule = 20

image_tete = pygame.image.load("pic/serpent_tete.png")
image_tete = pygame.transform.scale(image_tete, (taille_cellule * 1.5, taille_cellule * 1.5))

# Chargement de l'image de la boule de feu
image_fireball = pygame.image.load("pic/fireball.png")
image_fireball = pygame.transform.scale(image_fireball, ((int(taille_cellule * 1.1)), (int(taille_cellule * 1.3))))

# Chargement de l'image de l'autruche
image_autruche = pygame.image.load("pic/autruche.png")
image_autruche = pygame.transform.scale(image_autruche, (taille_cellule, taille_cellule * 2))
image_autruche_gauche = pygame.transform.flip(image_autruche, True, False)

# Définition des couleurs
couleur_fond = (0, 0, 0)
couleur_snake = (0, 255, 0)

# Chargement de l'image de fond d'écran
image_fond = pygame.image.load("pic/background.png")
image_fond = pygame.transform.scale(image_fond, (largeur_ecran, hauteur_ecran))

# son
son_pomelos = pygame.mixer.Sound("sound/pomelos.wav")
son_autruche = pygame.mixer.Sound("sound/autruche.wav")
son_boule_de_feu = pygame.mixer.Sound("sound/boule_de_feu.wav")
son_perdu = pygame.mixer.Sound("sound/perdu.wav")
jeu_termine = False


class Fruit:
    def __init__(self, image_path, sound_path):
        self.x = round(random.randrange(0, largeur_ecran - taille_cellule) / taille_cellule) * taille_cellule
        self.y = round(random.randrange(0, hauteur_ecran - taille_cellule) / taille_cellule) * taille_cellule
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, ((int(taille_cellule * 1.3)), (int(taille_cellule * 1.3))))
        self.sound = pygame.mixer.Sound(sound_path)

    def afficher(self):
        ecran.blit(self.image, (self.x, self.y))

    def manger(self):
        self.sound.play()
        self.x = round(random.randrange(0, largeur_ecran - taille_cellule) / taille_cellule) * taille_cellule
        self.y = round(random.randrange(0, hauteur_ecran - taille_cellule) / taille_cellule) * taille_cellule



# Classe pour la boule de feu
class BouleFeu:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.vitesse = 3
        self.images = [pygame.transform.scale(pygame.image.load('pic/fireball.png'),
                                              (int(taille_cellule * 1.1), int(taille_cellule * 1.3))),
                       pygame.transform.scale(pygame.image.load('pic/fireball2.png'),
                                              (int(taille_cellule * 1.1), int(taille_cellule * 1.3))),
                       pygame.transform.scale(pygame.image.load('pic/fireball3.png'),
                                              (int(taille_cellule * 1.1), int(taille_cellule * 1.3)))]
        self.current_image = 0
        self.image_counter = 0  # Initialise un compteur d'images à 0
        self.image_counter_limit = 5  # Nombre d'images avant de passer à la suivante

    def deplacer(self):
        if self.direction == "gauche":
            self.x -= self.vitesse
        elif self.direction == "droite":
            self.x += self.vitesse

    def afficher(self):
        ecran.blit(self.images[self.current_image], (self.x, self.y))
        # On incrémente le compteur d'images à chaque appel de la fonction
        self.image_counter += 1
        # Si le compteur d'images atteint la limite, on passe à l'image suivante et on remet le compteur à zéro
        if self.image_counter >= self.image_counter_limit:
            self.current_image = (self.current_image + 1) % len(self.images)
            self.image_counter = 0



# Classe pour l'autruche
class Autruche:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vitesse = 5
        self.boule_feu = None
        self.direction_x = 1
        self.direction_y = 1
        self.changement_direction_probabilite = 0.05
        self.image = image_autruche

    def deplacer(self):
        self.y += self.vitesse * self.direction_y
        if self.y <= 0 or self.y >= hauteur_ecran - taille_cellule * 2:
            self.direction_y *= -1

        self.x += self.vitesse * self.direction_x
        if self.x <= 0 or self.x >= largeur_ecran - taille_cellule:
            self.direction_x *= -1

        # Ajouter une composante aléatoire aux déplacements avec une probabilité plus faible
        if random.random() < self.changement_direction_probabilite:
            self.direction_x = random.choice([-1, 1])
            self.direction_y = random.choice([-1, 1])

        # changer l'image de l'autruche selon la direction
        if self.direction_x > 0:
            self.image = image_autruche_gauche
        else:
            self.image = image_autruche

    def afficher(self):
        ecran.blit(self.image, (self.x, self.y))

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


pomelos = Fruit("pic/pomelos1.png", "sound/pomelos.wav")


def afficher_menu_pause():
    ecran.fill((0, 0, 0))
    texte_pause = police.render("Pause", True, (255, 255, 255))
    texte_reprendre = police.render("Reprendre", True, (255, 255, 255))
    texte_quitter = police.render("Quitter", True, (255, 255, 255))

    ecran.blit(texte_pause,
               (largeur_ecran // 2 - texte_pause.get_width() // 2, hauteur_ecran // 2 - texte_pause.get_height() // 2))
    ecran.blit(texte_reprendre, (largeur_ecran // 2 - texte_reprendre.get_width() // 2, hauteur_ecran // 2 + 20))
    ecran.blit(texte_quitter, (largeur_ecran // 2 - texte_quitter.get_width() // 2, hauteur_ecran // 2 + 60))
    pygame.display.update()

def check_collision(obj1_x, obj1_y, obj1_size, obj2_x, obj2_y, obj2_size):
    if (obj2_x - obj1_size) < obj1_x < (obj2_x + obj2_size) and (obj2_y - obj1_size) < obj1_y < (obj2_y + obj2_size):
        return True
    return False

def perdu(serpent_corps):
    global jeu_termine

    # Mise à jour du jeu pour indiquer qu'il est terminé
    jeu_termine = True

    # Jouer le son de la défaite
    son_perdu.play()

    # Faire disparaître le serpent
    for _ in range(10):
        for segment in serpent_corps:
            pygame.draw.rect(ecran, couleur_fond, [segment[0], segment[1], taille_cellule, taille_cellule])
        pygame.display.update()
        pygame.time.wait(100)
        for segment in serpent_corps:
            pygame.draw.rect(ecran, couleur_snake, [segment[0], segment[1], taille_cellule, taille_cellule])
        pygame.display.update()
        pygame.time.wait(100)

def jeu_snake():
    # Initialisation de la position et de la direction du serpent
    serpent_x = largeur_ecran // 2
    serpent_y = hauteur_ecran // 2
    direction_x = 0
    direction_y = 0
    global image_tete
    global jeu_termine

    # initialisation du high score

    high_score = charger_highscore()

    # Initialisation de la longueur du serpent
    serpent_longueur = 1
    serpent_corps = []
    serpent_vitesse = 15

    # Initialisation de l'autruche
    autruche = Autruche(random.randint(0, largeur_ecran - taille_cellule),
                        random.randint(0, hauteur_ecran - taille_cellule * 2))

    # Variables de contrôle du jeu
    jeu_termine = False
    jeu_en_pause = False
    clock = pygame.time.Clock()

    # Boucle principale du jeu
    while not jeu_termine:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jeu_termine = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction_x != taille_cellule:  # prevent going right when moving left
                    direction_x = -taille_cellule
                    direction_y = 0
                elif event.key == pygame.K_RIGHT and direction_x != -taille_cellule:  # prevent going left when moving right
                    direction_x = taille_cellule
                    direction_y = 0
                elif event.key == pygame.K_UP and direction_y != taille_cellule:  # prevent going down when moving up
                    direction_x = 0
                    direction_y = -taille_cellule
                elif event.key == pygame.K_DOWN and direction_y != -taille_cellule:  # prevent going up when moving down
                    direction_x = 0
                    direction_y = taille_cellule
                elif event.key == pygame.K_ESCAPE:
                    jeu_en_pause = not jeu_en_pause
                    if jeu_en_pause:
                        pygame.mixer.pause()
                    else:
                        pygame.mixer.unpause()

        if jeu_en_pause:
            afficher_menu_pause()
            continue

        # Mise à jour de la position du serpent
        serpent_x += direction_x
        serpent_y += direction_y

        # Vérification des collisions avec les bords de l'écran
        if serpent_x >= largeur_ecran or serpent_x < 0 or serpent_y >= hauteur_ecran or serpent_y < 0:
            perdu(serpent_corps)

        # Affichage de l'image de fond
        ecran.blit(image_fond, (0, 0))

        # Affichage de la pomelos
        pomelos.afficher()

        # Déplacement et affichage de l'autruche
        autruche.deplacer()
        autruche.afficher()

        # Vérification de la collision entre la boule de feu et le serpent
        if autruche.boule_feu is not None:
            autruche.boule_feu.deplacer()
            autruche.boule_feu.afficher()
            # if int(serpent_x) == int(autruche.boule_feu.x) and int(serpent_y) == int(autruche.boule_feu.y)
            if check_collision(serpent_x, serpent_y, taille_cellule, autruche.boule_feu.x, autruche.boule_feu.y,
                               taille_cellule):
                son_boule_de_feu.play()
                perdu(serpent_corps)
            if autruche.boule_feu.x < 0 or autruche.boule_feu.x >= largeur_ecran:
                autruche.boule_feu = None

        # Vérification de la collision entre l'autruche et le serpent
        if check_collision(serpent_x, serpent_y, taille_cellule, autruche.x, autruche.y, taille_cellule):
            son_autruche.play()
            perdu(serpent_corps)

        # Vérification de la collision avec le pomelos
        if check_collision(serpent_x, serpent_y, taille_cellule, pomelos.x, pomelos.y, taille_cellule):
            pomelos.manger()
            serpent_longueur += 1

            if (serpent_longueur - 1) > high_score:
                enregistrer_highscore(serpent_longueur - 1)

        # Mise à jour du corps du serpent
        serpent_tete = [serpent_x, serpent_y]
        serpent_corps.append(serpent_tete)
        if len(serpent_corps) > serpent_longueur:
            del serpent_corps[0]

        # Vérification des collisions avec le corps du serpent
        for segment in serpent_corps[:-1]:
            if segment == serpent_tete:
                perdu(serpent_corps)

        # Dessin du serpent
        for index, segment in enumerate(serpent_corps):
            if index == len(serpent_corps) - 1:  # Si le segment est la tête
                if direction_y == -taille_cellule:  # Aller vers le haut
                    image_tete_rotated = pygame.transform.rotate(image_tete, 180)
                elif direction_y == taille_cellule:  # Aller vers le bas
                    image_tete_rotated = pygame.transform.rotate(image_tete, 0)
                elif direction_x == -taille_cellule:  # Aller vers la gauche
                    image_tete_rotated = pygame.transform.rotate(image_tete, 270)
                else:  # Aller vers la droite
                    image_tete_rotated = pygame.transform.rotate(image_tete, 90)

                ecran.blit(image_tete_rotated, (segment[0] - taille_cellule * 0.25, segment[1] - taille_cellule * 0.25))
            else:  # Sinon c'est le corps
                pygame.draw.rect(ecran, couleur_snake, [segment[0], segment[1], taille_cellule, taille_cellule])

        # affichage du high score
        texte_highscore = police.render("High Score: " + str(high_score), True, (255, 255, 255))
        rect_highscore = texte_highscore.get_rect()
        rect_highscore.topright = (largeur_ecran - 10, 10)
        ecran.blit(texte_highscore, rect_highscore)

        # affichage du high score
        texte_highscore = police.render("High Score: " + str(high_score), True, (255, 255, 255))
        rect_highscore = texte_highscore.get_rect()
        rect_highscore.topright = (largeur_ecran - 10, 10)
        ecran.blit(texte_highscore, rect_highscore)

        # affichage du score
        afficher_score(serpent_longueur - 1)

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
