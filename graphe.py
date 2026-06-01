"""
graphe.py

Generation et verification de la connexité d'un graphe aleatoire G(n, p).
"""

import random
import math


def generer_graphe(n, p):
    # Initialisation
    graphe = {}
    for noeud in range(n):
        graphe[noeud] = []

    # Parcours de toutes les paires (i, j) avec i < j
    for i in range(n):
        for j in range(i + 1, n):
            tirage = random.random()       
            if tirage < p:
                graphe[i].append(j)        
                graphe[j].append(i)      

    return graphe


def est_connexe(graphe, n):
    if n <= 1:
        return True

    visites  = set()
    file_bfs = []

    # Depart depuis le noeud 0
    visites.add(0)
    file_bfs.append(0)

    while len(file_bfs) > 0:
        noeud_courant = file_bfs.pop(0)
        for voisin in graphe[noeud_courant]:
            if voisin not in visites:
                visites.add(voisin)
                file_bfs.append(voisin)

    return len(visites) == n


def compter_composantes(graphe, n):
    tous_visites   = set()
    nb_composantes = 0

    for depart in range(n):
        if depart in tous_visites:
            continue

        nb_composantes = nb_composantes + 1
        file_bfs = [depart]
        tous_visites.add(depart)

        while len(file_bfs) > 0:
            courant = file_bfs.pop(0)
            for voisin in graphe[courant]:
                if voisin not in tous_visites:
                    tous_visites.add(voisin)
                    file_bfs.append(voisin)

    return nb_composantes


def generer_graphe_connexe(n, p, max_tentatives=2000):
    for tentative in range(1, max_tentatives + 1):
        graphe = generer_graphe(n, p)

        if est_connexe(graphe, n):
            print("  Graphe connexe trouve en " + str(tentative) + " tentative(s).")
            return graphe

        if tentative % 100 == 0:
            print("  ... " + str(tentative) + " tentatives, recherche en cours...")

    seuil = math.log(n) / n
    raise RuntimeError(
        "Impossible de trouver un graphe connexe en " + str(max_tentatives) +
        " tentatives (n=" + str(n) + ", p=" + str(round(p, 4)) + ").\n"
        "  Conseil : utilisez p > ln(n)/n environ " + str(round(seuil, 4)) +
        " pour n=" + str(n) + "."
    )
