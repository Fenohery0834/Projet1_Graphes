"""
statistiques.py

Calcul et affichage des metriques d'un graphe non oriente.
"""


def calculer_statistiques(graphe, n):
    liste_degres = {}
    somme_degres = 0
    degre_min    = None
    degre_max    = None

    for noeud in range(n):
        degre = len(graphe[noeud])
        liste_degres[noeud] = degre
        somme_degres = somme_degres + degre

        if degre_min is None:
            degre_min = degre
            degre_max = degre
        else:
            if degre < degre_min:
                degre_min = degre
            if degre > degre_max:
                degre_max = degre

    nb_aretes     = somme_degres // 2
    nb_aretes_max = n * (n - 1) // 2

    if nb_aretes_max > 0:
        densite = nb_aretes / nb_aretes_max
    else:
        densite = 0.0

    if n > 0:
        degre_moyen = somme_degres / n
    else:
        degre_moyen = 0.0

    stats = {}
    stats["nb_noeuds"]     = n
    stats["nb_aretes"]     = nb_aretes
    stats["nb_aretes_max"] = nb_aretes_max
    stats["densite"]       = densite
    stats["degre_moyen"]   = degre_moyen
    stats["degre_min"]     = degre_min if degre_min is not None else 0
    stats["degre_max"]     = degre_max if degre_max is not None else 0
    stats["liste_degres"]  = liste_degres

    return stats


def afficher_statistiques(stats):
    n             = stats["nb_noeuds"]
    nb_aretes     = stats["nb_aretes"]
    nb_aretes_max = stats["nb_aretes_max"]
    densite       = stats["densite"]
    degre_moyen   = stats["degre_moyen"]
    degre_min     = stats["degre_min"]
    degre_max     = stats["degre_max"]

    print("\n Statistiques ")
    print("  Nombre de noeuds   : " + str(n))
    print("  Nombre d'aretes    : " + str(nb_aretes) +
          "  (max possible : " + str(nb_aretes_max) + ")")
    print("  Densite            : " + str(round(densite, 4)) +
          "  (" + str(round(densite * 100, 1)) + " %)")
    print("  Degre moyen        : " + str(round(degre_moyen, 4)))
    print("  Degre minimum      : " + str(degre_min))
    print("  Degre maximum      : " + str(degre_max))


def afficher_distribution_degres(stats):
    liste_degres = stats["liste_degres"]

    comptage = {}
    for noeud in liste_degres:
        d = liste_degres[noeud]
        if d not in comptage:
            comptage[d] = 0
        comptage[d] = comptage[d] + 1

    max_count = 0
    for valeur in comptage.values():
        if valeur > max_count:
            max_count = valeur

    LARGEUR_MAX = 24

    print("\n Distribution des degres ")
    print("  Degre   Noeuds  Histogramme")
    print("  ------  ------  " + "-" * LARGEUR_MAX)

    for degre in sorted(comptage.keys()):
        nb = comptage[degre]
        if max_count > 0:
            longueur = int((nb / max_count) * LARGEUR_MAX)
        else:
            longueur = 0
        barre = "#" * longueur
        print("  " + str(degre).rjust(6) + "  " + str(nb).rjust(6) +
              "  " + barre + "  (" + str(nb) + ")")