"""
main.py

Point d'entree du programme -- Generateur de graphe G(n, p).
"""

import sys

from graphe        import generer_graphe_connexe
from statistiques  import (calculer_statistiques,
                            afficher_statistiques,
                            afficher_distribution_degres)
from visualisation import classifier_sous_graphes, visualiser

P = 0.5


def afficher_en_tete():
    largeur = 58
    titre   = "Graphe aleatoire G(n, p)"
    marge   = (largeur - len(titre)) // 2
    print("=" * largeur)
    print(" " * marge + titre)
    print("=" * largeur)


def saisir_n():
    while True:
        saisie = input("\nNombre de noeuds n (entier >= 2) : ").strip()
        try:
            n = int(saisie)
        except ValueError:
            print("  Erreur : '" + saisie + "' n'est pas un entier valide.")
            continue
        if n < 2:
            print("  Erreur : n doit etre >= 2  (recu : " + str(n) + ").")
            continue
        return n


def afficher_graphe(graphe):
    print("\n Liste d'adjacence ")
    for noeud in sorted(graphe.keys()):
        voisins = sorted(graphe[noeud])
        if len(voisins) == 0:
            chaine = "(aucun voisin)"
        else:
            parties = []
            for v in voisins:
                parties.append(str(v))
            chaine = "[" + ", ".join(parties) + "]"
        print("  Noeud " + str(noeud) + "  ->  " + chaine)


def afficher_resume(n, stats, classification):
    nb_aretes = stats["nb_aretes"]
    nb_max    = stats["nb_aretes_max"]
    densite   = stats["densite"]
    d_moy     = stats["degre_moyen"]
    cliques   = classification["cliques"]
    hubs      = classification["hubs"]
    cycle     = classification["cycle"]

    print("\n Resume final ")
    print("  Modele    : Erdos-Renyi G(n=" + str(n) +
          ", p=" + str(P) + ")")
    print("  Type      : non oriente - sans boucle - connexe garanti")
    print("  Aretes    : " + str(nb_aretes) + " / " + str(nb_max) +
          "  (" + str(round(densite * 100, 1)) + " %)")
    print("  Deg. moy. : " + str(round(d_moy, 4)))
    print("  Connexe   : Oui")
    print("  Cliques   : " + str(len(cliques)))
    print("  Hubs      : " + str(len(hubs)))
    if len(cycle) > 0:
        print("  Cycle     : oui")
    else:
        print("  Cycle     : non")
    print("\nProgramme termine avec succes.")


def main():
    afficher_en_tete()

    n = saisir_n()

    print("\n  Probabilite fixee : p = " + str(P))

    print("\nGeneration d'un graphe G(n=" + str(n) +
          ", p=" + str(P) + ") connexe")
    try:
        graphe = generer_graphe_connexe(n, P, max_tentatives=2000)
    except RuntimeError as erreur:
        print("\n  Echec : " + str(erreur))
        sys.exit(1)

    afficher_graphe(graphe)

    stats = calculer_statistiques(graphe, n)
    afficher_statistiques(stats)
    afficher_distribution_degres(stats)

    print("\n Classification des sous-graphes ")
    classification = classifier_sous_graphes(graphe, n)

    print("\nOuverture de la visualisation")
    titre = "Graphe aleatoire G(n=" + str(n) + ", p=" + str(P) + ")"
    visualiser(graphe, n, classification, titre=titre)

    afficher_resume(n, stats, classification)


if __name__ == "__main__":
    main()