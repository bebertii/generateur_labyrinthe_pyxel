import pyxel
from random import random, randrange, randint
"""
Le script génère un labyrinthe aléatoire parfait (il n'existe qu'un et un seul chemin possible entre 2 cases données)
par la méthode des fusions :
    - chaque case est initialement fermée sur ses 4 côtés et se voit attribuer un identifiant unique, chaque case est donc un labyrinthe de 1 case parfait
    - l'algo choisit aléatoirement une case et un côté fermé (droite ou bas, pas la peine de faire les 4)
    - si la case voisine correspondant au côté choisi possède le même identifiant, c'est qu'elle appartient au même labyrinthe : le côté ne sera pas ouvert,
    et l'ont teste l'autre mur possible
    - si la case voisine possède un identifiant différent, c'est qu'elle n'appartient pas au même labyrinthe. Dans ce cas :
        - on mémorise l'identifiant de la case voisine
        - on remplace toutes les cases ayant le même identifiant que celui de la case voisine par celui de la case en cours
    - on recommence jusqu'à ce que toutes les cartes possèdent le même identifiant

Pour visualiser le processus de fusions successive, le script associe à chaque identifiant une des 15 couleurs disponibles en dehors du noir dans la palette
de Pyxel et chaque case est coloriée de cette couleur
"""
largeur, hauteur = 256, 256 # dimensions de la denêtre pyxel
taille_brique = 8   # taille d'une case en pixels (ideal : 8)
nb_briques_l  = largeur // taille_brique # détermination du nombre de cases en largeur
nb_briques_h = hauteur//taille_brique # détermination du nombre de cases en hauteur

pyxel.init(largeur, hauteur,fps = 60) # instanciation de la fenêtre pyxel

carte=dict() # déclaration de la carte qui deviendra le labyrinthe
#fusionnees = [] # déclaration de la liste contenant tous les identifiants disponibles

# peuplement de la carte en utilisant comme clé un tuple correspondant aux coordonnées de la case
# chaque case contient en liste les informations sur l'état de chacun de ses 4 murs : False -> fermé, True -> ouvert
# le dernier item de la liste est l'identifiant de la case
for i in range(nb_briques_l):
    for j in range(nb_briques_h):
        carte[(i,j)] = [False] * 4 + [nb_briques_l*i + j]

# Cette fonction permet d'inverser l'état d'un mur d'une case donnée ainsi que celui de la case voisine correspondante
# ex : si je veux ouvrir le mur de droite de la case (7,10), il faut également ouvrir celui de gauche de la case (8,10)
# l'utilisation de l'opérateur 'not' permet d'ouvrir si le mur est fermé et de fermer si la porte est ouverte
def inverser_mur(i,j,num):
    global nb_briques_l, nb_briques_h
    carte[(i,j)][num] = not carte[(i,j)][num]
    if num == 0 : carte[((i - 1) % nb_briques_l, j)][2] = not carte[((i - 1) % nb_briques_l, j)][2]
    if num == 2 : carte[((i + 1) % nb_briques_l, j)][0] = not carte[((i + 1) % nb_briques_l, j)][0]
    if num == 1 : carte[(i, (j - 1) % nb_briques_h)][3] = not carte[(i, (j - 1) % nb_briques_h)][3]
    if num == 3 : carte[(i, (j + 1) % nb_briques_h)][1] = not carte[(i, (j + 1) % nb_briques_h)][1]
    return None

# fonction chargée du dessin du labyrinthe en appliquant le code couleur correspondant à l'identifiant de chaque case
def dessine():
    global nb_briques_l, nb_briques_h, taille_brique
    pyxel.cls(0)
    for i in range(nb_briques_l):
        for j in range(nb_briques_h):
            coul = carte[(i,j)][-1] % 15 + 1 # détermination de la couleur de la case à partir de son identifiant
            pyxel.rect(taille_brique * i + 1, taille_brique * j + 1, taille_brique - 2, taille_brique - 2, coul)
            if carte[(i,j)][0] : pyxel.line(taille_brique * i, taille_brique * j + 1, taille_brique * i, taille_brique * j + 6, coul)
            if carte[(i,j)][2] : pyxel.line(taille_brique * (i + 1) - 1, taille_brique * j + 1, taille_brique * (i + 1) - 1, taille_brique * (j + 1) - 2, coul)
            if carte[(i,j)][1] : pyxel.line(taille_brique * i + 1, taille_brique * j, taille_brique * (i + 1) - 2, taille_brique * j, coul)
            if carte[(i,j)][3] : pyxel.line(taille_brique * i + 1, taille_brique * (j + 1) - 1, taille_brique * (i + 1) - 2, taille_brique * (j + 1) - 1, coul)
    pyxel.flip()
    return None

def fusion_laby():
    global nb_briques_l, nb_briques_h

    # on génère une liste des identifiants
    cles_dispos = [x for x in range(nb_briques_l * nb_briques_h)]

    while len(cles_dispos) > 1:
        change = False

        # les coordonnées de la case choisie au hasard
        # /!\ par défaut le labyrinthe est comme celui de pacman, ouvrir le bord inférieur de la case tout en bas ouvre le bord supérieur
        # de la case tout en haut, pareil pour la gauche et la droite.
        # si ce n'est pas ce que vous voulez, utilisez plutôt
        # i = randrange(0, nb_briques_l - 1)
        # j = randrange(0, nb_briques_h - 1)
        i = randrange(0, nb_briques_l)
        j = randrange(0, nb_briques_h)

        ordre = sorted([2,3],key=lambda x:random())

        if ordre[0] == 2: # si on cherche à ouvrir le mur de droite
            # on vérifie que ce mur est fermé (sinon, inutile de l'ouvrir !)
            # et que l'identifiant de la case à droite est différent de celui de la case considérée
            if carte[(i,j)][ordre[0]] == False and carte[(i,j)][-1] != carte[((i + 1) % nb_briques_l, j)][-1]:
                # on mémorise l'identifiant de la case voisine afin ensuite de modifier toutes les cases ayant le même identifiant
                a_fusionner = carte[((i+1) % nb_briques_l, j)][-1]
                # on ouvre le mur de droite de la case considérée ainsi que le mur de gauche de la case voisine
                inverser_mur(i,j,ordre[0])
                # on parcourt toutes les cases afin de remplacer l'identifiant des cases qui auraient le même que celui de la case de gauche
                for m in range(nb_briques_l):
                    for n in range(nb_briques_h):
                        if carte[(m,n)][-1] == a_fusionner :
                            carte[(m,n)][-1] = carte[(i,j)][-1]
                # on supprime l'identifiant de la case voisine des identifiants présents dans le labyrinthe
                del(cles_dispos[cles_dispos.index(a_fusionner)])
                # on indique qu'il y a eu un changement
                change = True

            # on fait de même pour le bas si la droite n'était pas possible (déjà ouverte ou case voisine du même groupe)
            elif carte[(i,j)][ordre[1]] == False and carte[(i,j)][-1] != carte[(i,(j+1)%nb_briques_h)][-1]:
                a_fusionner = carte[(i,(j+1)%nb_briques_h)][-1]
                inverser_mur(i,j,ordre[1])
                for m in range(nb_briques_l):
                    for n in range(nb_briques_h):
                        if carte[(m,n)][-1] == a_fusionner :
                            carte[(m,n)][-1] = carte[(i,j)][-1]
                del(cles_dispos[cles_dispos.index(a_fusionner)])
                change = True

        else : # même idée que précédemment mais inversé parce que la première direction était vers le bas
            if carte[(i,j)][ordre[0]] == False and carte[(i,j)][-1] != carte[(i,(j+1)%nb_briques_h)][-1]:
                a_fusionner = carte[(i,(j+1)%nb_briques_h)][-1]
                inverser_mur(i,j,ordre[0])
                for m in range(nb_briques_l):
                    for n in range(nb_briques_h):
                        if carte[(m,n)][-1] == a_fusionner :
                            carte[(m,n)][-1] = carte[(i,j)][-1]
                del(cles_dispos[cles_dispos.index(a_fusionner)])
                change = True

            elif carte[(i,j)][ordre[1]] == False and carte[(i,j)][-1] != carte[((i+1)%nb_briques_l,j)][-1]:
                a_fusionner = carte[((i+1)%nb_briques_l,j)][-1]
                inverser_mur(i,j,ordre[1])
                for m in range(nb_briques_l):
                    for n in range(nb_briques_h):
                        if carte[(m,n)][-1] == a_fusionner :
                            carte[(m,n)][-1] = carte[(i,j)][-1]
                del(cles_dispos[cles_dispos.index(a_fusionner)])
                change = True
        # En fin de labyrinthe, cette méthode va très souvent choisir une case inutilisable, si jamais on choisit de
        # redessiner à chaque tentative, l'animation va être très longue sur de grands labyrinthe
        # on ne redessine donc que si la boucle a abouti à un changement dans le labyrinthe
        if change : dessine()
    return None

fusion_laby()
