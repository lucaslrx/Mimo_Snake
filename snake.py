import pygame
import random
import requests

global ressources

# Initialisation de Pygame
pygame.init()
pygame.mixer.init()

# Définition des dimensions de l'écran
largeur_ecran = 640
hauteur_ecran = 480

# Création de la fenêtre de jeu
ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
pygame.display.set_caption("Snake Game")

jeu_termine = False
high_score = 0
jeu_en_pause = False


class Fruit:
    global ressources

    def __init__(self, image_path, sound_path):
        taille_cellule = ressources['taille_cellule']
        self.x = round(random.randrange(0, largeur_ecran - taille_cellule) / taille_cellule) * taille_cellule
        self.y = round(random.randrange(0, hauteur_ecran - taille_cellule) / taille_cellule) * taille_cellule
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, ((int(taille_cellule * 1.3)), (int(taille_cellule * 1.3))))
        self.sound = pygame.mixer.Sound(sound_path)

    def afficher(self):
        ecran.blit(self.image, (self.x, self.y))

    def manger(self):
        taille_cellule = ressources['taille_cellule']
        self.sound.play()
        self.x = round(random.randrange(0, largeur_ecran - taille_cellule) / taille_cellule) * taille_cellule
        self.y = round(random.randrange(0, hauteur_ecran - taille_cellule) / taille_cellule) * taille_cellule


# Classe pour la boule de feu
class BouleFeu:
    global ressources

    def __init__(self, x, y, direction, vitesse=3, image_path='pic/fireball.png'):
        taille_cellule = ressources['taille_cellule']
        self.x = x
        self.y = y
        self.direction = direction
        self.vitesse = vitesse
        self.images = [pygame.transform.scale(pygame.image.load(image_path),
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
    global ressources

    def __init__(self, x, y):
        image_autruche = ressources['image_autruche']
        self.vitesse = 5
        self.boule_feu = None
        self.direction_x = 1
        self.direction_y = 1
        self.changement_direction_probabilite = 0.05
        self.image = image_autruche

        marge_exclusion = 3 * ressources['taille_cellule']
        centre_x = largeur_ecran // 2
        centre_y = hauteur_ecran // 2

        while True:
            self.x = round(
                random.randrange(0, largeur_ecran - ressources['taille_cellule']) / ressources['taille_cellule']) * \
                     ressources['taille_cellule']
            self.y = round(
                random.randrange(0, hauteur_ecran - ressources['taille_cellule']) / ressources['taille_cellule']) * \
                ressources['taille_cellule']

            if not (centre_x - marge_exclusion <= self.x <= centre_x + marge_exclusion and
                    centre_y - marge_exclusion <= self.y <= centre_y + marge_exclusion):
                break

    def deplacer(self):
        taille_cellule = ressources['taille_cellule']
        image_autruche = ressources['image_autruche']
        image_autruche_gauche = ressources['image_autruche_gauche']
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
        son_autruche = ressources['son_autruche']
        taille_cellule = ressources['taille_cellule']
        if self.boule_feu is None:
            direction = random.choice(["gauche", "droite"])
            self.boule_feu = BouleFeu(self.x, self.y + taille_cellule, direction)
            son_autruche.play()


# Classe pour Florian
class Florian(Autruche):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.vitesse = 10  # Vitesse augmentée pour l'ennemi rapide
        image_florian = ressources['image_florian']
        self.image = image_florian
        self.image_droite = image_florian
        self.image_florian_gauche = ressources['image_florian_gauche']

    def lancer_boule_feu(self):
        son_florian = pygame.mixer.Sound("sound/florian.wav")
        taille_cellule = ressources['taille_cellule']
        if self.boule_feu is None:
            direction = random.choice(["gauche", "droite"])
            self.boule_feu = BouleFeu(self.x, self.y + taille_cellule, direction, vitesse=5,
                                      image_path='pic/pull.png')
            son_florian.play()

    def deplacer(self):
        super().deplacer()  # Appel de la méthode deplacer() de la classe parente Autruche
        # changer l'image de Florian selon la direction
        if self.direction_x > 0:
            self.image = self.image_florian_gauche
        else:
            self.image = self.image_droite


class Serpent:
    def __init__(self, x, y, longueur, vitesse):
        self.x = x
        self.y = y
        self.longueur = longueur
        self.vitesse = vitesse
        self.direction_x = 0
        self.direction_y = 0
        self.corps = [[self.x, self.y]]
        self.tue_autruche = False
        self.clignotement = False

    def maj_position(self):
        self.x += self.direction_x
        self.y += self.direction_y
        self.corps.append([self.x, self.y])
        if len(self.corps) > self.longueur:
            del self.corps[0]

    def change_direction(self, direction_x, direction_y):
        self.direction_x = direction_x
        self.direction_y = direction_y

    def collision_mur(self, largeur_limite, hauteur_limite):
        return self.x >= largeur_limite or self.x < 0 or self.y >= hauteur_limite or self.y < 0

    def collision_soi_meme(self):
        return [self.x, self.y] in self.corps[:-1]

    def manger_pomelos(self):
        self.longueur += 1

    def dessiner(self, ecran_dessiner, taille_cellule, couleur_snake, image_tete):
        for index, segment in enumerate(self.corps):
            if self.clignotement and pygame.time.get_ticks() % 250 < 125:  # le serpent clignote en jaune
                pygame.draw.rect(ecran_dessiner, ressources['couleur_clignotement'],
                                 [segment[0], segment[1], taille_cellule, taille_cellule])
                continue

            if index == len(self.corps) - 1:  # Si le segment est la tête
                if self.direction_y == -taille_cellule:  # Aller vers le haut
                    image_tete_rotated = pygame.transform.rotate(image_tete, 180)
                elif self.direction_y == taille_cellule:  # Aller vers le bas
                    image_tete_rotated = pygame.transform.rotate(image_tete, 0)
                elif self.direction_x == -taille_cellule:  # Aller vers la gauche
                    image_tete_rotated = pygame.transform.rotate(image_tete, 270)
                else:  # Aller vers la droite
                    image_tete_rotated = pygame.transform.rotate(image_tete, 90)

                ecran_dessiner.blit(image_tete_rotated, (segment[0] - taille_cellule * 0.25, segment[1]
                                                         - taille_cellule * 0.25))
            else:  # Sinon c'est le corps
                pygame.draw.rect(ecran_dessiner, couleur_snake,
                                 [segment[0], segment[1], taille_cellule, taille_cellule])

    def clignoter(self, etat):
        self.clignotement = etat


# Fonction principale du jeu


def charger_ressources():
    taille_cellule = 20

    # Chargement des images
    image_tete = pygame.image.load("pic/serpent_tete.png")
    image_tete = pygame.transform.scale(image_tete, (taille_cellule * 1.5, taille_cellule * 1.5))

    image_fireball = pygame.image.load("pic/fireball.png")
    image_fireball = pygame.transform.scale(image_fireball, ((int(taille_cellule * 1.1)), (int(taille_cellule * 1.3))))

    image_autruche = pygame.image.load("pic/autruche.png")
    image_autruche = pygame.transform.scale(image_autruche, (taille_cellule, taille_cellule * 2))
    image_autruche_gauche = pygame.transform.flip(image_autruche, True, False)

    image_florian = pygame.image.load("pic/autruche_florian.png")
    image_florian = pygame.transform.scale(image_florian, (taille_cellule, taille_cellule * 2))
    image_florian_gauche = pygame.transform.flip(image_florian, True, False)

    image_pomelo = pygame.image.load("pic/pomelos1.png")  # Chemin vers l'image du pomelo
    image_pomelo = pygame.transform.scale(image_pomelo, (35, 35))  # Ajustez la taille du pomelo

    image_fond = pygame.image.load("pic/background.png")
    image_fond = pygame.transform.scale(image_fond, (largeur_ecran, hauteur_ecran))

    couleur_snake = (0, 255, 0)
    couleur_fond = (0, 0, 0)
    couleur_clignotement = (255, 255, 0)

    # Chargement des sons
    son_pomelos = pygame.mixer.Sound("sound/pomelos.wav")
    son_autruche = pygame.mixer.Sound("sound/autruche.wav")
    son_boule_de_feu = pygame.mixer.Sound("sound/boule_de_feu.wav")
    son_perdu = pygame.mixer.Sound("sound/perdu.wav")

    # Chargement de la police
    police = pygame.font.Font("tools/Arial.ttf", 24)

    return {
        'taille_cellule': taille_cellule,
        'image_tete': image_tete,
        'image_fireball': image_fireball,
        'image_autruche': image_autruche,
        'image_autruche_gauche': image_autruche_gauche,
        'image_fond': image_fond,
        'image_pomelo': image_pomelo,
        'son_pomelos': son_pomelos,
        'son_autruche': son_autruche,
        'son_boule_de_feu': son_boule_de_feu,
        'son_perdu': son_perdu,
        'police': police,
        'couleur_snake': couleur_snake,
        'couleur_fond': couleur_fond,
        'couleur_clignotement': couleur_clignotement,
        'image_florian': image_florian,
        'image_florian_gauche': image_florian_gauche
    }


def afficher_score(longueur, police):
    texte = police.render("Pomelos: " + str(longueur), True, (255, 255, 255))
    ecran.blit(texte, (10, 10))


def enregistrer_highscore(score):
    payload = {"new_content": str(score)}
    requests.post("http://127.0.0.1:5000/api/update_content", json=payload)


def charger_highscore():
    reponse = requests.get("http://127.0.0.1:5000/api/get_content")
    data = reponse.json()
    contenu = data.get('content')
    if contenu:
        return int(contenu)
    else:
        return 0


def compte_a_rebours(ecran_compte, ressources_compte):
    police = ressources_compte['police']
    for i in range(3, 0, -1):
        ecran_compte.fill(ressources_compte['couleur_fond'])
        texte_compte_a_rebours = police.render(str(i), True, (255, 255, 255))
        rect_compte_a_rebours = texte_compte_a_rebours.get_rect(center=(largeur_ecran // 2, hauteur_ecran // 2))
        ecran_compte.blit(texte_compte_a_rebours, rect_compte_a_rebours)

        # Ajouter le texte sous le compteur
        texte_astuce = police.render("Astuce : Prépare tes touches (bas, haut, gauche, droite)", True, (255, 255, 255))
        rect_astuce = texte_astuce.get_rect(center=(largeur_ecran // 2, hauteur_ecran // 2 + 50))
        ecran_compte.blit(texte_astuce, rect_astuce)

        pygame.display.update()
        pygame.time.wait(1000)


def afficher_bouton(ecran_bouton, texte, position, survol):
    police = ressources['police']
    couleur_texte = (255, 255, 255)
    couleur_survol = (200, 200, 200)

    if survol:
        couleur_texte = couleur_survol

    texte_bouton = police.render(texte, True, couleur_texte)
    rect_bouton = texte_bouton.get_rect(center=position)
    ecran_bouton.blit(texte_bouton, rect_bouton)
    return rect_bouton


def afficher_menu_principal(ecran_menu, ressources_menu):
    largeur_ecran_menu = ecran_menu.get_width()
    hauteur_ecran_menu = ecran_menu.get_height()

    bouton_jouer_survol = False
    bouton_quitter_survol = False

    autruche_x, autruche_y = largeur_ecran_menu // 2 + 40, hauteur_ecran_menu // 2 - 25
    image_autruche = pygame.transform.scale(ressources_menu['image_autruche'], (35, 35))  # Ajustez la taille
    pomelo_x, pomelo_y = largeur_ecran_menu // 2 - 80, hauteur_ecran_menu // 2 - 25
    image_pomelo = pygame.transform.scale(ressources_menu['image_pomelo'], (35, 35))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                rect_bouton_jouer = afficher_bouton(ecran_menu, "Jouer",
                                                    (largeur_ecran_menu // 2, hauteur_ecran_menu // 2),
                                                    bouton_jouer_survol)
                rect_bouton_quitter = afficher_bouton(ecran_menu, "Quitter",
                                                      (largeur_ecran_menu // 2, hauteur_ecran_menu // 2 + 40),
                                                      bouton_quitter_survol)

                if rect_bouton_jouer.collidepoint(mouse_x, mouse_y):
                    compte_a_rebours(ecran_menu, ressources_menu)  # Appel de la fonction de compte à rebours
                    return True  # Démarrer la partie
                elif rect_bouton_quitter.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    quit()

            else:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                rect_bouton_jouer = afficher_bouton(ecran_menu, "Jouer", (largeur_ecran_menu // 2,
                                                                          hauteur_ecran_menu // 2),
                                                    bouton_jouer_survol)
                rect_bouton_quitter = afficher_bouton(ecran_menu, "Quitter", (largeur_ecran_menu // 2,
                                                                              hauteur_ecran_menu // 2 + 40),
                                                      bouton_quitter_survol)

                bouton_jouer_survol = rect_bouton_jouer.collidepoint(mouse_x, mouse_y)
                bouton_quitter_survol = rect_bouton_quitter.collidepoint(mouse_x, mouse_y)

                ecran_menu.fill((0, 0, 0))  # Efface l'écran
                afficher_bouton(ecran_menu, "Jouer", (largeur_ecran_menu // 2, hauteur_ecran_menu // 2),
                                bouton_jouer_survol)
                afficher_bouton(ecran_menu, "Quitter", (largeur_ecran_menu // 2, hauteur_ecran_menu // 2 + 40),
                                bouton_quitter_survol)

                # Affiche l'image de l'autruche à côté du bouton sélectionné
                if bouton_jouer_survol:
                    ecran_menu.blit(image_autruche, (autruche_x, autruche_y))
                    ecran_menu.blit(image_pomelo, (pomelo_x, pomelo_y))
                elif bouton_quitter_survol:
                    ecran_menu.blit(image_autruche, (autruche_x, autruche_y + 40))  # Ajustez la position
                    ecran_menu.blit(image_pomelo, (pomelo_x, pomelo_y + 40))
                pygame.display.update()  # Met à jour l'écran


def afficher_menu_pause():
    global jeu_en_pause
    largeur_ecran_menu_pause = ecran.get_width()
    hauteur_ecran_menu_pause = ecran.get_height()

    bouton_reprendre_survol = False
    bouton_quitter_survol = False

    autruche_x, autruche_y = largeur_ecran_menu_pause // 2 + 40, hauteur_ecran_menu_pause // 2 + 5
    image_autruche = pygame.transform.scale(ressources['image_autruche'], (35, 35))
    pomelo_x, pomelo_y = largeur_ecran_menu_pause // 2 - 80, hauteur_ecran_menu_pause // 2 + 5
    image_pomelo = pygame.transform.scale(ressources['image_pomelo'], (35, 35))

    while jeu_en_pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                rect_bouton_reprendre = afficher_bouton(ecran, "Reprendre",
                                                        (largeur_ecran_menu_pause // 2,
                                                         hauteur_ecran_menu_pause // 2 + 20),
                                                        bouton_reprendre_survol)
                rect_bouton_quitter = afficher_bouton(ecran, "Quitter", (largeur_ecran_menu_pause // 2,
                                                                         hauteur_ecran_menu_pause // 2 + 60),
                                                      bouton_quitter_survol)

                if rect_bouton_reprendre.collidepoint(mouse_x, mouse_y):
                    jeu_en_pause = False
                elif rect_bouton_quitter.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    quit()
            else:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                rect_bouton_reprendre = afficher_bouton(ecran, "Reprendre",
                                                        (largeur_ecran_menu_pause // 2,
                                                         hauteur_ecran_menu_pause // 2 + 20),
                                                        bouton_reprendre_survol)
                rect_bouton_quitter = afficher_bouton(ecran, "Quitter", (largeur_ecran_menu_pause // 2,
                                                                         hauteur_ecran_menu_pause // 2 + 60),
                                                      bouton_quitter_survol)

                bouton_reprendre_survol = rect_bouton_reprendre.collidepoint(mouse_x, mouse_y)
                bouton_quitter_survol = rect_bouton_quitter.collidepoint(mouse_x, mouse_y)

                ecran.fill((0, 0, 0))
                afficher_bouton(ecran, "Reprendre", (largeur_ecran_menu_pause // 2, hauteur_ecran_menu_pause // 2 + 30),
                                bouton_reprendre_survol)
                afficher_bouton(ecran, "Quitter", (largeur_ecran_menu_pause // 2,
                                                   hauteur_ecran_menu_pause // 2 + 60), bouton_quitter_survol)

                if bouton_reprendre_survol:
                    ecran.blit(image_autruche, (autruche_x + 20, autruche_y))
                    ecran.blit(image_pomelo, (pomelo_x - 20, pomelo_y))
                elif bouton_quitter_survol:
                    ecran.blit(image_autruche, (autruche_x, autruche_y + 40))
                    ecran.blit(image_pomelo, (pomelo_x, pomelo_y + 40))
                pygame.display.update()


def check_collision(obj1_x, obj1_y, obj1_size, obj2_x, obj2_y, obj2_size):
    if (obj2_x - obj1_size) < obj1_x < (obj2_x + obj2_size) and (obj2_y - obj1_size) < obj1_y < (obj2_y + obj2_size):
        return True
    return False


def perdu(serpent_corps, serpent):
    global jeu_termine
    global ressources
    global high_score
    taille_cellule = ressources['taille_cellule']

    # Mise à jour du jeu pour indiquer qu'il est terminé
    jeu_termine = True

    # Jouer le son de la défaite
    ressources['son_perdu'].play()
    if (serpent.longueur - 1) > high_score:
        high_score = serpent.longueur - 1
        enregistrer_highscore(high_score)

    # Faire disparaître le serpent
    for _ in range(10):
        for segment in serpent_corps:
            pygame.draw.rect(ecran, ressources['couleur_fond'],
                             [segment[0], segment[1], taille_cellule, taille_cellule])
        pygame.display.update()
        pygame.time.wait(100)
        for segment in serpent_corps:
            pygame.draw.rect(ecran, ressources['couleur_snake'],
                             [segment[0], segment[1], taille_cellule, taille_cellule])
        pygame.display.update()
        pygame.time.wait(100)


def jeu_snake():
    # Initialisation de la position et de la direction du serpent
    serpent = Serpent(largeur_ecran // 2, hauteur_ecran // 2, 1, 15)
    global jeu_termine
    global ressources
    global jeu_en_pause
    global high_score

    ressources = charger_ressources()

    # initialisation du high score
    high_score = charger_highscore()

    # variables temps pour fruit spécial
    temps_fruit_special = pygame.time.get_ticks()
    fruit_special = None
    duree_fruit_special = 5000  # en ms
    fruit_special_temps_effet = 0
    temps_apparition_fruit_special = None
    afficher_menu_principal(ecran, ressources)

    # Initialisation de l'autruche
    taille_cellule = ressources['taille_cellule']

    autruche = Autruche(random.randint(0, largeur_ecran - taille_cellule),
                        random.randint(0, hauteur_ecran - taille_cellule * 2))
    autruche_vivant = True
    autruche_disparition_temps = None


    pomelos = Fruit("pic/pomelos1.png", "sound/pomelos.wav")

    # Variables de contrôle du jeu
    jeu_termine = False
    jeu_en_pause = False
    clock = pygame.time.Clock()
    autruche_mange = False
    serpent_a_bouge = False
    florian_est_arrive = False

    # Boucle principale du jeu
    while not jeu_termine:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jeu_termine = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and serpent.direction_x != taille_cellule:
                    serpent.change_direction(-taille_cellule, 0)
                    serpent_a_bouge = True
                elif event.key == pygame.K_RIGHT and serpent.direction_x != -taille_cellule:
                    serpent.change_direction(taille_cellule, 0)
                    serpent_a_bouge = True
                elif event.key == pygame.K_UP and serpent.direction_y != taille_cellule:
                    serpent.change_direction(0, -taille_cellule)
                    serpent_a_bouge = True
                elif event.key == pygame.K_DOWN and serpent.direction_y != -taille_cellule:
                    serpent.change_direction(0, taille_cellule)
                    serpent_a_bouge = True
                elif event.key == pygame.K_ESCAPE:
                    jeu_en_pause = not jeu_en_pause
                    if jeu_en_pause:
                        pygame.mixer.pause()
                    else:
                        pygame.mixer.unpause()

        if jeu_en_pause:
            afficher_menu_pause()
            continue
        if pygame.time.get_ticks() - temps_fruit_special >= 5000 and not fruit_special:
            temps_fruit_special = pygame.time.get_ticks()

            if random.randint(1, 5) == 1:
                fruit_special = Fruit("pic/pomelos.png", "sound/pomelos.wav")
                temps_apparition_fruit_special = pygame.time.get_ticks()
            else:
                fruit_special = None

        # Make special fruit disappear after 5 seconds
        if fruit_special and pygame.time.get_ticks() - temps_apparition_fruit_special >= 5000:
            fruit_special = None

        # Mise à jour de la position du serpent
        serpent.maj_position()

        # Dessin du serpent
        # Si autruche_mange est True, faire clignoter le serpent
        if autruche_mange:
            if pygame.time.get_ticks() % 250 < 125:  # Clignote toutes les 250 millisecondes
                serpent.clignoter(True)
            else:
                serpent.clignoter(False)
        else:
            serpent.clignoter(False)

        # Vérification des collisions avec les bords de l'écran
        if serpent.collision_mur(largeur_ecran, hauteur_ecran):
            perdu(serpent.corps, serpent)

        # Affichage de l'image de fond
        image_fond = ressources['image_fond']
        ecran.blit(image_fond, (0, 0))

        # Affichage de la pomelos
        pomelos.afficher()

        # Déplacement et affichage de l'autruche
        if autruche_vivant and serpent_a_bouge:
            autruche.deplacer()
            autruche.afficher()

        # Déplacement et affichage du Florian
        if serpent.longueur > 10 and florian_est_arrive == False:
            # Initialisation du Florian
            florian = Florian(random.randint(0, largeur_ecran - taille_cellule),
                              random.randint(0, hauteur_ecran - taille_cellule * 2))
            florian_est_arrive = True

        if florian_est_arrive == True :
            florian.deplacer()
            florian.afficher()
            florian.lancer_boule_feu()

        # Vérification de la collision entre la boule de feu et le serpent
        if autruche.boule_feu is not None:
            autruche.boule_feu.deplacer()
            autruche.boule_feu.afficher()
            if check_collision(serpent.x, serpent.y, taille_cellule, autruche.boule_feu.x, autruche.boule_feu.y,
                               taille_cellule):
                ressources['son_boule_de_feu'].play()
                perdu(serpent.corps, serpent)
            if autruche.boule_feu.x < 0 or autruche.boule_feu.x >= largeur_ecran:
                autruche.boule_feu = None

        # collision serpent fruit spécial
        if fruit_special is not None and check_collision(serpent.x, serpent.y, taille_cellule, fruit_special.x,
                                                         fruit_special.y, taille_cellule):
            fruit_special.manger()
            autruche_mange = True
            fruit_special = None
            fruit_special_temps_effet = pygame.time.get_ticks() + duree_fruit_special

            # If effect of special fruit should end
        if pygame.time.get_ticks() >= fruit_special_temps_effet:
            autruche_mange = False

        # Vérification de la collision entre l'autruche et le serpent
        if autruche_vivant and check_collision(serpent.x, serpent.y, taille_cellule, autruche.x, autruche.y,
                                               taille_cellule):
            if autruche_mange:
                ressources['son_autruche'].play()
                autruche_disparition_temps = pygame.time.get_ticks()  # temps de disparition de l'autruche
                autruche.x = -100  # déplace l'autruche hors de l'écran
                serpent.longueur += 2
                autruche_mange = False
                autruche_vivant = False
                serpent.clignotement = False
            else:
                perdu(serpent.corps, serpent)

        # Faire réapparaître l'autruche après quelques secondes
        if not autruche_vivant and pygame.time.get_ticks() - autruche_disparition_temps >= 5000:
            autruche_vivant = True
            autruche = Autruche(random.randint(0, largeur_ecran - taille_cellule),
                                random.randint(0, hauteur_ecran - taille_cellule * 2))
            autruche_mange = False

        # Vérification de la collision avec le pomelos
        if check_collision(serpent.x, serpent.y, taille_cellule, pomelos.x, pomelos.y, taille_cellule):
            pomelos.manger()
            serpent.manger_pomelos()

        # Vérification des collisions avec le corps du serpent
        if serpent.collision_soi_meme():
            perdu(serpent.corps, serpent)

        # collision avec le Florian
        if florian_est_arrive == True :
            if check_collision(serpent.x, serpent.y, taille_cellule, florian.x, florian.y,
                               taille_cellule):
                ressources['son_boule_de_feu'].play()
                perdu(serpent.corps, serpent)

        # collision des boules de feues de Florian et du serpent
        if florian_est_arrive and florian.boule_feu:
            florian.boule_feu.deplacer()
            florian.boule_feu.afficher()
            if check_collision(serpent.x, serpent.y, taille_cellule, florian.boule_feu.x, florian.boule_feu.y,
                               taille_cellule):
                ressources['son_boule_de_feu'].play()
                perdu(serpent.corps, serpent)
            if florian.boule_feu.x < 0 or florian.boule_feu.x >= largeur_ecran:
                florian.boule_feu = None

        # Dessin du serpent
        serpent.dessiner(ecran, taille_cellule, ressources['couleur_snake'], ressources['image_tete'])

        # Déterminer le score à afficher
        if high_score > serpent.longueur - 1:
            score_affiche = high_score
        else:
            score_affiche = serpent.longueur - 1

        # Générer le texte du score
        texte_highscore = ressources['police'].render("High Score: " + str(score_affiche), True, (255, 255, 255))

        # Définir l'emplacement du score
        rect_highscore = texte_highscore.get_rect()
        rect_highscore.topright = (largeur_ecran - 10, 10)

        # Afficher le score
        ecran.blit(texte_highscore, rect_highscore)

        # affichage du score
        afficher_score(serpent.longueur - 1, ressources['police'])

        # Mise à jour de l'écran
        pygame.display.update()

        # Lancer une nouvelle boule de feu
        autruche.lancer_boule_feu()

        # Limite de vitesse du serpent
        clock.tick(serpent.vitesse)
    # Fermeture de la fenêtre Pygame
    pygame.quit()


# Lancement du jeu
jeu_snake()
