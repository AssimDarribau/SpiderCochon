import pygame
import random
from pygame import *

largeur_ecran = 800
hauteur_ecran = 1150


class Bouton:
    def __init__(self, x, y, largeur, hauteur, texte, couleur, couleur_texte):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.couleur = couleur
        self.couleur_texte = couleur_texte

    def dessiner(self, screen, font):
        pygame.draw.rect(screen, self.couleur, self.rect)
        texte_surf = font.render(self.texte, True, self.couleur_texte)
        texte_rect = texte_surf.get_rect(center=self.rect.center)
        screen.blit(texte_surf, texte_rect)

    def est_clique(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False


def enregistrer_score(nom, score):
    """
    Enregistre un score dans le fichier texte.
    """
    with open("scores.txt", "a") as fichier:
        fichier.write(f"{nom} : {score}\n")


def afficher_classement(screen):
    """
    Affiche le classement trié par score décroissant.
    """
    font = pygame.font.Font(r"Super Shiny.ttf", 50)

    background_image = pygame.image.load("ressources/classement.png")
    background_image = pygame.transform.scale(background_image, (largeur_ecran, hauteur_ecran))

    try:
        with open("scores.txt", "r") as fichier:
            scores = fichier.readlines()
    except FileNotFoundError:
        scores = []

# trier les scores
    scores_propres = []
    for ligne in scores:
        try:
            nom, score = ligne.strip().split(" : ")
            scores_propres.append((nom, int(score)))  # Convertir le score en entier
        except ValueError:
            continue  # Ignore les erreurs

# Trier les scores par ordre décroissant
    scores_triees = sorted(scores_propres, key=extraire_score, reverse=True)

    en_attente = True
    while en_attente:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return  # Retour à l'écran précédent avec ESC

# Dessiner le fond d'écran
        screen.blit(background_image, (0, 0))

# Afficher le texte "Classement"
        titre = font.render("Classement", True, (255, 255, 255))
        screen.blit(titre, (largeur_ecran // 2 - titre.get_width() // 2, 50))

# Afficher les scores
        for i, (nom, score) in enumerate(scores_triees[:22]):  # Limiter à 22 scores affichés
            texte_score = font.render(f"{nom} : {score}", True, (255, 255, 255))
            screen.blit(texte_score, (50, 150 + i * 40))

        pygame.display.flip()

def extraire_score(x):
    return x[1]


def demander_nom(screen):
    font = pygame.font.Font(r"Super Shiny.ttf", 50)
    nom = ""
    en_attente = True
    while en_attente:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return None
            if event.type == KEYDOWN:
                if event.key == K_RETURN:  # Valider le nom
                    en_attente = False
                elif event.key == K_BACKSPACE:  # Supprimer un caractère
                    nom = nom[:-1]
                else:
                    nom += event.unicode

        screen.fill((0, 0, 0))
        texte = font.render("Entrez votre nom: " + nom, True, (255, 255, 255))
        screen.blit(texte, (50, hauteur_ecran // 2))
        pygame.display.flip()

    return nom


def ecran_accueil(screen):
    """
    Affiche l'écran d'accueil avec un arrière-plan et un bouton "Jouer".

    Args:
        screen (pygame.Surface): Surface principale où dessiner les éléments.

    Returns:
        bool: Retourne True si le joueur clique sur "Jouer", sinon False.
    """

    font = pygame.font.Font(r"Super Shiny.ttf", 50)
    background_image = pygame.image.load("ressources/accueil.png")
    background_image = pygame.transform.scale(background_image, (largeur_ecran, hauteur_ecran))

    bouton_start = Bouton(largeur_ecran // 2 - 100, hauteur_ecran // 2 + 50, 200, 50, "Jouer", (200, 25, 75), (255, 255, 255))
    bouton_classement = Bouton(largeur_ecran // 2 - 120, hauteur_ecran // 2 + 120, 250, 50, "Classement", (25, 75, 200), (255, 255, 255))

    en_attente = True
    while en_attente:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return None
            if bouton_start.est_clique(event):
                nom_joueur = demander_nom(screen)
                return nom_joueur  # Retourner le nom pour l'utiliser plus tard (Important)
            if bouton_classement.est_clique(event):
                afficher_classement(screen)

        screen.blit(background_image, (0, 0))
        bouton_start.dessiner(screen, font)
        bouton_classement.dessiner(screen, font)
        pygame.display.flip()


class Araigner(pygame.sprite.Sprite):
    def __init__(self):
        super(Araigner, self).__init__()
        self.image_up1 = pygame.image.load("ressources/araigner_up1.png")
        self.image_up2 = pygame.image.load("ressources/araigner_up2.png")

        self.image_down1 = pygame.image.load("ressources/araigner_down1.png")
        self.image_down2 = pygame.image.load("ressources/araigner_down2.png")

        self.image_left1 = pygame.image.load("ressources/araigner_left1.png")
        self.image_left2 = pygame.image.load("ressources/araigner_left2.png")

        self.image_right1 = pygame.image.load("ressources/araigner_right1.png")
        self.image_right2 = pygame.image.load("ressources/araigner_right2.png")
#image Par Defaut
        self.surf = self.image_up1
        self.rect = self.surf.get_rect(center=(largeur_ecran // 2, hauteur_ecran - 50))


        self.animation_counter = 0

    def update(self, pressed_keys):
        self.animation_counter += 1

        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            if self.animation_counter % 10 < 5:
                self.surf = self.image_up1
            else:
                self.surf = self.image_up2

        elif pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 10)
            if self.animation_counter % 10 < 5:
                self.surf = self.image_down1
            else:
                self.surf = self.image_down2

        elif pressed_keys[K_LEFT]:
            self.rect.move_ip(-7, 1)
            if self.animation_counter % 10 < 5:
                self.surf = self.image_left1
            else:
                self.surf = self.image_left2

        elif pressed_keys[K_RIGHT]:
            self.rect.move_ip(7, 1)
            if self.animation_counter % 10 < 5:
                self.surf = self.image_right1
            else:
                self.surf = self.image_right2

        else:
# Par défaut
            self.animation_counter = 0
            self.surf = self.image_up1

        if pressed_keys[K_SPACE]:
            if len(la_toile.sprites()) < 1 :
                toile = Toile(self.rect.center)
                tous_sprites.add(toile)
                la_toile.add(toile)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > largeur_ecran:
            self.rect.right = largeur_ecran
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= hauteur_ecran:
            self.rect.bottom = hauteur_ecran


class Toile(pygame.sprite.Sprite):
    def __init__(self, center_toile):
        super(Toile, self).__init__()
        self.surf = pygame.image.load("ressources/toile.png")
        self.rect = self.surf.get_rect(
            center=center_toile
        )
        son_toile.play()

    def update(self):
        self.rect.move_ip(0, -15)  #toile haut
        if self.rect.bottom < 0:  # la supprimer
            self.kill()



class Enemmi(pygame.sprite.Sprite):
    def __init__(self, vitesse_fond):
        super(Enemmi, self).__init__()
        self.surf = pygame.image.load("ressources/ennemi.png")
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, largeur_ecran),
                -50  # Par défaut
            )
        )
        self.speed = random.randint(5, 10) + vitesse_fond  # Ajouter la vitesse de fond

    def update(self):
        self.rect.move_ip(0, self.speed)  # bas
        if self.rect.top > hauteur_ecran:  # Supprimer
            self.kill()

    def ajuster_vitesse(self, vitesse_fond):
        self.speed += vitesse_fond // 10  # Ajustement de la vitesse avec une proportion de la vitesse de fond



class Explosion(pygame.sprite.Sprite):
    def __init__(self, center_position):
        super(Explosion, self).__init__()

        self._compteur = 10
        self.surf = pygame.image.load("ressources/explosionn.png")
        self.rect = self.surf.get_rect(center=center_position)
        son_explosion.play()

    def update(self):
        self._compteur -= 1
        if self._compteur == 0:
            self.kill()


class Fond:
    def __init__(self):
        # Charger l'image de fond
        self.image = pygame.image.load("ressources/building.png").convert()
        self.image = pygame.transform.scale(self.image, (largeur_ecran, hauteur_ecran))
        # Positions de départ
        self.y1 = 0
        self.y2 = -hauteur_ecran

    def update(self, vitesse_fond):
        self.y1 += vitesse_fond
        self.y2 += vitesse_fond

        # Boucler l'arrière-plan
        if self.y1 >= hauteur_ecran:
            self.y1 = -hauteur_ecran
        if self.y2 >= hauteur_ecran:
            self.y2 = -hauteur_ecran

    def draw(self, screen):
        screen.blit(self.image, (0, self.y1))
        screen.blit(self.image, (0, self.y2))


class Score(pygame.sprite.Sprite):
    def __init__(self):
        super(Score, self).__init__()
        self._score_courant = 0
        self._multiplicateur = 1
        self._set_text()

    def _set_text(self):
        self.surf = police_score.render(
            f'Score : {self._score_courant}', False, (255, 255, 255)
        )
        self.rect = self.surf.get_rect(topleft=(10, 10))

        # Texte pour le multiplicateur
        self.multiplicateur_surf = police_score.render(
            f'Multiplicateur : x{self._multiplicateur}', False, (255, 255, 255)
        )
        self.multiplicateur_rect = self.multiplicateur_surf.get_rect(topleft=(10, 50))

    def update(self):
        self._set_text()

    def incrementer(self, valeur):
        self._score_courant += valeur

    def set_multiplicateur(self, valeur):
        self._multiplicateur = valeur


class Bonus(pygame.sprite.Sprite):
    def __init__(self, vitesse_fond):
        super(Bonus, self).__init__()
        self.surf = pygame.image.load("ressources/bonus.png")
        self.surf = pygame.transform.scale(self.surf, (50, 50))  # Ajustez la taille du bonus
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, largeur_ecran),
                -50  # Commence hors de l'écran
            )
        )
        self.speed = vitesse_fond + 5  # Les bonus tombent légèrement plus vite que l'arrière-plan

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > hauteur_ecran:  # Supprimer si le bonus sort de l'écran
            self.kill()




pygame.font.init()

police_score= pygame.font.Font(r"Super Shiny.ttf", 40)

pygame.mixer.init()

son_toile = pygame.mixer.Sound("ressources/bruit_toile.ogg")
son_explosion = pygame.mixer.Sound("ressources/explosion.ogg")


clock = pygame.time.Clock()

pygame.init()

pygame.display.set_caption("Spider Cochon")

Ajout_ennemi = pygame.USEREVENT + 1
pygame.time.set_timer(Ajout_ennemi, 500)

ecran = pygame.display.set_mode([largeur_ecran, hauteur_ecran])

clock = pygame.time.Clock()

tous_sprites = pygame.sprite.Group()

araigner = Araigner()
tous_sprites.add(araigner)
la_toile = pygame.sprite.Group()
les_ennemies = pygame.sprite.Group()
les_explosions = pygame.sprite.Group()
score = Score()
tous_sprites.add(score)

fond = Fond()
continuer = True


def lancer_jeu(screen, tous_sprites, la_toile, les_ennemies, les_explosions, nom_joueur):
    araigner = Araigner()
    tous_sprites.add(araigner)

    fond = Fond()
    score = Score()
    tous_sprites.add(score)

    bonus_group = pygame.sprite.Group()  # Groupe pour les bonus

    # Variables pour gérer la difficulté et les bonus
    frequence_ennemis = 500
    vitesse_fond = 5
    compteur_temps = 0
    multiplicateur_score = 1
    BONUS_EVENT = pygame.USEREVENT + 2
    pygame.time.set_timer(BONUS_EVENT, 10000)

    pygame.time.set_timer(Ajout_ennemi, frequence_ennemis)

    continuer = True
    clock = pygame.time.Clock()

    while continuer:
        delta_time = clock.tick(30)  # Limiter à 30 FPS
        compteur_temps += delta_time

        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = False
            elif event.type == Ajout_ennemi:
                nouvel_ennemi = Enemmi(vitesse_fond)
                les_ennemies.add(nouvel_ennemi)
                tous_sprites.add(nouvel_ennemi)
            elif event.type == BONUS_EVENT:
                bonus = Bonus(vitesse_fond)
                bonus_group.add(bonus)
                tous_sprites.add(bonus)

        # Augmenter la difficulté toutes les 5 secondes
        if compteur_temps >= 5000:
            compteur_temps = 0
            frequence_ennemis = max(200, frequence_ennemis - 50)
            vitesse_fond += 1
            pygame.time.set_timer(Ajout_ennemi, frequence_ennemis)

            for ennemi in les_ennemies:
                ennemi.ajuster_vitesse(vitesse_fond)

        # Gestion des collisions avec les ennemis
        if pygame.sprite.spritecollideany(araigner, les_ennemies):
            araigner.kill()
            explosion = Explosion(araigner.rect.center)
            les_explosions.add(explosion)
            tous_sprites.add(explosion)
            continuer = False

        # Gestion des collisions avec les toiles
        for toile in la_toile:
            ennemis_touches = pygame.sprite.spritecollide(toile, les_ennemies, True)
            if len(ennemis_touches) > 0:
                toile.kill()
                score.incrementer(len(ennemis_touches) * multiplicateur_score)
            for ennemi in ennemis_touches:
                explosion = Explosion(ennemi.rect.center)
                les_explosions.add(explosion)
                tous_sprites.add(explosion)

        # Gestion des collisions avec les bonus
        bonus_touches = pygame.sprite.spritecollide(araigner, bonus_group, True)
        if bonus_touches:
            multiplicateur_score += len(bonus_touches)
            score.set_multiplicateur(multiplicateur_score)  # Mettre à jour l'affichage du multiplicateur

        # Mise à jour des sprites
        touche_appuyee = pygame.key.get_pressed()
        araigner.update(touche_appuyee)
        la_toile.update()
        les_ennemies.update()
        les_explosions.update()
        bonus_group.update()
        score.update()

        # Dessiner l'arrière-plan et tous les sprites
        fond.update(vitesse_fond)
        fond.draw(screen)
        for sprite in tous_sprites:
            screen.blit(sprite.surf, sprite.rect)

# Afficher le multiplicateur sous le score
        screen.blit(score.multiplicateur_surf, score.multiplicateur_rect)

        pygame.display.flip()

    # Jeu terminé, enregistrer le score
    enregistrer_score(nom_joueur, score._score_courant)
    return score._score_courant


def afficher_fin(screen, score):
    """
    Affiche un écran de fin de jeu avec un bouton pour rejouer et une image personnalisée.
    """
    font = pygame.font.Font(r'Super Shiny.ttf', 60)
    bouton_rejouer = Bouton(largeur_ecran // 2 - 100, hauteur_ecran // 2 + 250, 200, 50, "Rejouer", (0, 200, 0), (255, 255, 255))

    # Charger l'image personnalisée
    try:
        image_fin = pygame.image.load("ressources/photo_fin.png")
# Redimensionner en gardant le ratio
        largeur_voulue = 400
        hauteur_voulue = int((largeur_voulue / 1080) * 1094)  # Calculer la hauteur en maintenant le ratio
        image_fin = pygame.transform.smoothscale(image_fin, (largeur_voulue, hauteur_voulue))
    except pygame.error as e:
        print(f"Erreur lors du chargement de l'image : {e}")
        image_fin = None

    continuer = True
    while continuer:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return "quitter"
            if event.type == MOUSEBUTTONDOWN and bouton_rejouer.est_clique(event):
                return "rejouer"

# Dessiner l'arrière-plan
        screen.fill((0, 0, 0))

# Afficher le message de fin
        message = font.render(f"Perdu!!! Score: {score}", True, (255, 255, 255))
        screen.blit(message, (largeur_ecran // 2 - message.get_width() // 2, hauteur_ecran // 2 - 250))

# Afficher l'image si elle est chargée
        if image_fin:
            image_x = largeur_ecran // 2 - largeur_voulue // 2
            image_y = hauteur_ecran // 2 - hauteur_voulue // 2
            screen.blit(image_fin, (image_x, image_y))

# Afficher le bouton "Rejouer"
        bouton_rejouer.dessiner(screen, font)

# Rafraîchir l'écran
        pygame.display.flip()

# Programme principal
if __name__ == "__main__":
    pygame.init()
    ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
    pygame.display.set_caption("Spider Cochon")

    rejouer = True
    while rejouer:
# Réinitialiser les groupes de sprites pour chaque partie
        tous_sprites = pygame.sprite.Group()
        la_toile = pygame.sprite.Group()
        les_ennemies = pygame.sprite.Group()
        les_explosions = pygame.sprite.Group()

# Afficher l'écran d'accueil
        nom_joueur = ecran_accueil(ecran)
        if nom_joueur:
# Lancer une partie
            score_final = lancer_jeu(ecran, tous_sprites, la_toile, les_ennemies, les_explosions, nom_joueur)

# Afficher l'écran de fin
            action_fin = afficher_fin(ecran, score_final)

            if action_fin == "rejouer":
# Relancer une nouvelle partie
                continue
            else:
                rejouer = False
    pygame.quit()

