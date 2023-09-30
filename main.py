#!/usr/bin/env python3

from email.errors import NoBoundaryInMultipartDefect
from sys import argv
from geo.point import Point




### Rapide Paire

def distance(point1, point2):
    """
    Calcule la distance au carré
    """
    return (point1.x-point2.x)**2+(point1.y-point2.y)**2

def coor_x(point):
    """
    Renvoie la coordonné en x du point, utilisé pour comme key pour sort
    """
    return point.x

def coor_y(point):
    """
    Renvoie la coordonné en y du point, utilisé pour comme key pour sort
    """
    return point.y

def paire_rapide(liste_x, liste_y):
    """
    Algo Paire Rapide, voir explication avec le pseudo code dans le rapport
    """
    dmin = float('inf')
    couple = (None, None)
    for rayon in range(1, len(liste_x)):
        dx_min, dy_min = float('inf'), float('inf')
        for centre in range(0, len(liste_x)-rayon):
            dist_x = distance(liste_x[centre], liste_x[rayon+centre])
            dist_y = distance(liste_y[centre], liste_y[rayon+centre])
            delta_x = (liste_x[centre].x - liste_x[rayon+centre].x)**2
            if dx_min >= delta_x:
                dx_min = delta_x
            delta_y = (liste_y[centre].y - liste_y[rayon+centre].y)**2
            if dy_min >= delta_y:
                dy_min = delta_y
            if dmin > dist_x:
                couple = (liste_x[centre], liste_x[rayon+centre])
                dmin = dist_x
            if dmin > dist_y:
                couple = (liste_y[centre], liste_y[rayon+centre])
                dmin = dist_y
        if dmin <= dx_min + dy_min:
            return couple, dmin
    return couple, dmin



### Diviser pour régner


def cle(paire):
    """
    Sert de key pour renvoyer dmin
    """
    return paire[1]

def intersection_x(liste, moitier, dmin):
    """
    Renvoie la liste des points inclue dans l'intersection à retester
    """
    a, b = 0, 0
    xm = liste[moitier].x
    for i, j in enumerate(liste[moitier:]):
        if j.x - xm < dmin:
            b = i
        else:
            break
    for i, j in enumerate(reversed(liste[:moitier])):
        if xm - j.x < dmin:
            a = i
        else:
            break
    return liste[moitier-a-1: moitier+b+1]


def min_intersection(points, dmin):
    """
    Renvoie le couple le plus proche dans l'intersection.
    """
    nombre_point = len(points)
    for i in range(min(6, nombre_point - 1), nombre_point):
        for j in range(max(0, i-6), i):
            dist = distance(points[i], points[j])
            if dist < dmin:
                dmin = dist
    dmin = dmin**0.5
    return dmin, (points[i], points[j])

def diviser_pour_regner(liste_x, ite):
    """
    Algo diviser_pour_regner, voir explication avec le pseudo code dans le rapport
    """
    if len(liste_x) <= ite:
        liste_y = sorted(liste_x, key=coor_y)
        return paire_rapide(liste_x, liste_y)
    moitier = len(liste_x)//2
    (quadrant_hg, dmin_hg) = diviser_pour_regner(liste_x[:moitier], ite)
    (quadrant_hd, dmin_hd) = diviser_pour_regner(liste_x[moitier:], ite)
    (couple, dmin) = min((quadrant_hg, dmin_hg), (quadrant_hd, dmin_hd), key=cle)
    inter_x = intersection_x(liste_x, moitier, dmin)
    paire_int_x = min_intersection(inter_x, dmin)
    if dmin > paire_int_x[0]:
        dmin, couple = paire_int_x
    return couple, dmin



##### Table de Hashage

###Algo_Crible
def codage_cle(x, y, r):
    """
    Sert de clé pour les table de hashage
    """
    return (int(x/r)<<20)+int(y/r)

def crea_grille(points, rayon):
    """
    Créer une table de hashage qui joue le role de grille pour algo_crible
    et insère les points dans la table
    """
    grille = dict()
    for i in points:
        grille[codage_cle(i.x, i.y, rayon)] = i
    return grille


def calcul_dmin(point, rayon, grille):
    """
    Renvoie le dmin entre le point 'point' et les points issues des cases adjacentes
    """
    dmin = float("inf")
    couple = None
    for i in range(int(point.x/rayon)-1, int(point.x/rayon)+2):
        for j in range(int(point.y/rayon)-1, int(point.y/rayon)+2):
            if (i<<20)+j in grille:
                point2 = grille[(i<<20)+j]
                dist = distance(point, point2)
                if dmin > dist:
                    dmin = dist
                    couple = (point, point2)
    return dmin, couple


def algo_crible(points, debut, dmin, couple):
    """
    Algo_Crible voir explication et pseudo code dans le rapport
    """
    compteur = 0
    rayon = dmin**0.5
    grille = crea_grille(points[:debut], rayon)
    for i in range(debut, len(points)):
        dmin2, couple1 = calcul_dmin(points[i], rayon, grille)
        if dmin2 > dmin:
            grille[codage_cle(points[i].x, points[i].y, rayon)] = points[i]
        else:
            rayon = dmin2**0.5
            dmin = dmin2
            couple = couple1
            compteur += 1
            grille = crea_grille(points[:i+1], rayon)
    return couple



###Algo_Grille

def algo_grille(points, dmin, couple):
    """
    Algo_Grille voir explication et pseudo code dans le rapport
    """
    rayon = dmin**0.5
    grille = crea_grille2(points, rayon)
    for i in grille.keys():
        cpl, d = recherche_case(i, grille)
        if not cpl:
            pass
        elif d < dmin:
            dmin = d
            couple = cpl
    return couple


def crea_grille2(points, rayon):
    """
    Créer une table de hashage qui joue le role de grille pour algo_grille
    et insère les points dans la table
    """
    grille = dict()
    for i in points:
        key = codage_cle(i.x, i.y, rayon)
        #print(f"clé:{key} est {i}")
        if grille.get(key) is None:
            grille[key] = [i]
        else:
            grille[key].append(i)
    return grille


def recherche_case(key, grille):
    """
    Retourne le couple le plus proche dans les 4 listes concatené adjacente
    """
    L = grille[key] + grille.get(key+1, []) + grille.get(key+(1<<20), []) + grille.get(key+1+(1<<20), [])
    if len(L) == 1:
        return (False, False)
    if len(L) == 2:
        return ((L[0], L[1]), distance(L[0], L[1]))
    liste_x = sorted(L, key=coor_x)
    liste_y = sorted(L, key=coor_y)
    return paire_rapide(liste_x, liste_y)

#####Affichage

def print_dpr(points, nb):
    """
    Affiche le couple de distance minimale avec Diviser pour regner
    """
    liste_x = sorted(points, key=coor_x)        #Liste trié suivant x croissant
    couple, _ = diviser_pour_regner(liste_x, nb)
    print(f"{float(couple[0].x)}, {float(couple[0].y)}; {float(couple[1].x)}, {float(couple[1].y)}")

def print_crible_hybride(points, nb):
    """
    Affiche le couple de distance minimale avec algo_crible si len(points)>nb et Paire Rapide sinon
    """
    if len(points) < nb:
        print_paire_rapide(points)
    else:
        liste_x = sorted(points[:nb], key=coor_x)        #Liste trié suivant x croissant
        liste_y = sorted(points[:nb], key=coor_y)
        couple, dmin = paire_rapide(liste_x, liste_y)
        couple = algo_crible(points, nb-1, dmin, couple)
        print(f"{float(couple[0].x)}, {float(couple[0].y)}; {float(couple[1].x)}, {float(couple[1].y)}")


def print_grille_hybride(points, nb):
    """
    Affiche le couple de distance minimale avec algo_grille si len(points)>nb et Paire Rapide sinon
    """
    if len(points) < nb:
        print_paire_rapide(points)
    else:
        liste_x = sorted(points[:nb], key=coor_x)        #Liste trié suivant x croissant
        liste_y = sorted(points[:nb], key=coor_y)
        couple, dmin = paire_rapide(liste_x, liste_y)
        couple = algo_grille(points, dmin, couple)
        print(f"{float(couple[0].x)}, {float(couple[0].y)}; {float(couple[1].x)}, {float(couple[1].y)}")


def print_paire_rapide(points):
    """
    Affiche le couple de distance minimale avec Paire Rapide
    """
    liste_x = sorted(points, key=coor_x)        #Liste trié suivant x croissant
    liste_y = sorted(points, key=coor_y)
    couple, _ = paire_rapide(liste_x, liste_y)
    print(f"{float(couple[0].x)}, {float(couple[0].y)}; {float(couple[1].x)}, {float(couple[1].y)}")


def load_instance(filename):
    """
    loads .mnt file.
    returns list of points.
    """
    with open(filename, "r") as instance_file:
        points = [Point((float(p[0]), float(p[1]))) for p in (l.split(',') for l in instance_file)]

    return points

def print_solution(points):
    """
    calcul et affichage de la solution (a faire)
    """
    print_crible_hybride(points, 20000)
    #print_grille_hybride(points, 20000)
    #print_dpr(points, 10000)
    #print_paire_rapide(points)

def main():
    """
    ne pas modifier: on charge des instances donnees et affiches les solutions
    """
    for instance in argv[1:]:
        points = load_instance(instance)
        print_solution(points)


main()
