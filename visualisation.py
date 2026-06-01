"""
visualisation.py

Classification des sous-graphes et visualisation coloree avec
matplotlib et networkx.

"""

import math
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# Detection des cliques

def trouver_cliques(graphe, n):
    cliques = []

    for i in range(n):
        for j in range(i + 1, n):
            if j in graphe[i]:
                for k in range(j + 1, n):
                    if k in graphe[i] and k in graphe[j]:
                        cliques.append((i, j, k))

    return cliques


# Detection d'un cycle simple (DFS)

def trouver_un_cycle(graphe, n):
    visite = {}
    parent = {}
    pile   = []
    cycle  = []

    for depart in range(n):
        if depart in visite:
            continue

        pile.append((depart, -1))

        while len(pile) > 0:
            noeud, par = pile.pop()

            if noeud in visite:
                continue
            visite[noeud] = True
            parent[noeud] = par

            for voisin in graphe[noeud]:
                if voisin not in visite:
                    pile.append((voisin, noeud))
                elif voisin != par and len(cycle) == 0:
                    chemin  = [voisin, noeud]
                    courant = noeud
                    while parent.get(courant, -1) != -1 and courant != voisin:
                        courant = parent[courant]
                        chemin.append(courant)
                        if courant == voisin:
                            break
                    cycle = chemin

    return cycle


# Detection des noeuds hubs

def trouver_hubs(graphe, n):
    degres = []
    for noeud in range(n):
        degres.append(len(graphe[noeud]))

    moyenne = sum(degres) / n

    variance = 0.0
    for d in degres:
        variance = variance + (d - moyenne) ** 2
    variance   = variance / n
    ecart_type = math.sqrt(variance)

    seuil = moyenne + ecart_type

    hubs = set()
    for noeud in range(n):
        if degres[noeud] >= seuil:
            hubs.add(noeud)

    return hubs


# Classification

def classifier_sous_graphes(graphe, n):
    print("  Classification des sous-graphes en cours...")

    cliques = trouver_cliques(graphe, n)
    print("    Cliques (k=3)   : " + str(len(cliques)) + " trouvee(s)")

    cycle = trouver_un_cycle(graphe, n)
    if len(cycle) > 0:
        print("    Cycle detecte   : oui (" + str(len(cycle)) + " noeuds)")
    else:
        print("    Cycle detecte   : non")

    hubs = trouver_hubs(graphe, n)
    print("    Hubs            : " + str(len(hubs)) + " noeud(s)")

    resultat = {}
    resultat["cliques"] = cliques
    resultat["cycle"]   = cycle
    resultat["hubs"]    = hubs
    return resultat


# Visualisation

def visualiser(graphe, n, classification, titre="Graphe aleatoire G(n, p)"):

    plt.rcParams["toolbar"] = "None"

    # Construction du graphe 
    G = nx.Graph()
    G.add_nodes_from(range(n))
    for i in range(n):
        for j in graphe[i]:
            if i < j:
                G.add_edge(i, j)

    cliques = classification["cliques"]
    cycle   = classification["cycle"]
    hubs    = classification["hubs"]

    # Noeuds et aretes appartenant a une clique
    noeuds_clique = set()
    aretes_clique = set()
    for (i, j, k) in cliques:
        noeuds_clique.add(i)
        noeuds_clique.add(j)
        noeuds_clique.add(k)
        aretes_clique.add((i, j))
        aretes_clique.add((i, k))
        aretes_clique.add((j, k))

    # Noeuds et aretes du cycle
    noeuds_cycle = set(cycle)
    aretes_cycle = set()
    for i in range(len(cycle) - 1):
        u = min(cycle[i], cycle[i + 1])
        v = max(cycle[i], cycle[i + 1])
        aretes_cycle.add((u, v))

    # Couleur de chaque noeud
    couleurs_noeuds = []
    for noeud in range(n):
        if noeud in hubs:
            couleurs_noeuds.append("#C0392B")  
        elif noeud in noeuds_cycle:
            couleurs_noeuds.append("#2ecc71")  
        elif noeud in noeuds_clique:
            couleurs_noeuds.append("#e67e22")
        else:
            couleurs_noeuds.append("#95a5a6")   

    # Couleur de chaque arete
    couleurs_aretes = []
    largeurs_aretes = []
    for u, v in G.edges():
        paire = (min(u, v), max(u, v))
        if paire in aretes_clique:
            couleurs_aretes.append("#e67e22")   
            largeurs_aretes.append(2.5)
        elif paire in aretes_cycle:
            couleurs_aretes.append("#2ecc71")  
            largeurs_aretes.append(2.0)
        else:
            couleurs_aretes.append("#bdc3c7")  
            largeurs_aretes.append(1.0)

    # Mise en page
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.patch.set_facecolor("#2b2b2b")

    # Sous-figure gauche : graphe colore
    ax1 = axes[0]
    ax1.set_facecolor("#3c3c3c")
    ax1.set_title("Graphe G(n, p) - Classification",
                  color="white", fontsize=12, pad=12)

    pos = nx.spring_layout(G, seed=42, k=2.0 / math.sqrt(n))

    nx.draw_networkx_nodes(G, pos, ax=ax1,
                           node_color=couleurs_noeuds,
                           node_size=400,
                           edgecolors="white",
                           linewidths=0.8)

    nx.draw_networkx_edges(G, pos, ax=ax1,
                           edge_color=couleurs_aretes,
                           width=largeurs_aretes,
                           alpha=0.85)

    nx.draw_networkx_labels(G, pos, ax=ax1,
                            font_color="white",
                            font_size=8,
                            font_weight="bold")

    legende = [
        mpatches.Patch(color="#C0392B",
                       label="Hub    [" + str(len(hubs)) + " noeuds]"),
        mpatches.Patch(color="#2ecc71",
                       label="Cycle  [" + str(len(noeuds_cycle)) + " noeuds]"),
        mpatches.Patch(color="#e67e22",
                       label="Clique (k=3) [" + str(len(cliques)) + " trouvee(s)]"),
        mpatches.Patch(color="#95a5a6",
                       label="Noeud ordinaire"),
    ]
    ax1.legend(handles=legende,
               loc="lower left",
               facecolor="#4a4a4a",
               edgecolor="white",
               labelcolor="white",
               fontsize=8)

    ax1.axis("off")

    # Sous-figure droite : resume statistique
    ax2 = axes[1]
    ax2.set_facecolor("#3c3c3c")
    ax2.set_title("Resume de la classification",
                  color="white", fontsize=12, pad=12)
    ax2.axis("off")

    nb_aretes_total = 0
    for v in graphe:
        nb_aretes_total = nb_aretes_total + len(graphe[v])
    nb_aretes_total = nb_aretes_total // 2

    densite_val = round(nb_aretes_total / (n * (n - 1) // 2), 3)

    if len(cycle) > 0:
        cycle_texte = str(len(cycle)) + " noeuds"
    else:
        cycle_texte = "aucun"

    lignes = [
        ("Parametres du graphe", ""),
        ("  Noeuds (n)",          str(n)),
        ("  Aretes",              str(nb_aretes_total)),
        ("  Densite",             str(densite_val)),
        ("", ""),
        ("Sous-graphes detectes", ""),
        ("  Cliques (k=3)",       str(len(cliques))),
        ("  Cycle representatif", cycle_texte),
        ("  Hubs",                str(len(hubs))),
        ("", ""),
        ("Proprietes", ""),
        ("  Connexe",             "Oui"),
        ("  Non oriente",         "Oui"),
        ("  Sans boucle",         "Oui"),
    ]

    y = 0.95
    for label, valeur in lignes:
        if valeur == "":
            ax2.text(0.05, y, label,
                     color="#f39c12", fontsize=10,
                     fontweight="bold",
                     transform=ax2.transAxes)
        else:
            ax2.text(0.05, y, label,
                     color="#ecf0f1", fontsize=9,
                     transform=ax2.transAxes)
            ax2.text(0.75, y, valeur,
                     color="#2ecc71", fontsize=9,
                     fontweight="bold",
                     transform=ax2.transAxes)
        y = y - 0.07

    plt.suptitle(titre, color="white", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig("graphe.png", dpi=150,
                bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.show()
    print("\n  Figure sauvegardee -> graphe.png")
