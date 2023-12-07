import json as j
import os
from chargeur_deck import chargement_deck


def createur_deck() -> None:
    """Créer un deck et l'enregistre dans un fichier json"""

    nom_deck = input('nom du deck : ')
    couleurs = input('couleurs présentes (écrire séparé par des espaces) : ').split(' ')
    nb_max_carte = int(input('valeur maximale des cartes : '))
    
    effets_texte = []
    while True:
        creer_carte_effet = input('Créer une carte à effet ? (O/N)')
        if creer_carte_effet == 'N':
            break
        
        effets_dispos = ['plus','interdiction','changer_couleur','changer_sens']
        
        while len(effets_dispos) > 0:
            
            ajouter_effet = input('Ajouter un effet ? (O/N)')
            if ajouter_effet == 'N':
                break
            
            for i in range(len(effets_dispos)):
                print(f'{i} {effets_dispos[i]}')
            
            choix = int(input('quel effet à ajouter? (indice)'))
            
            effet_choisi = effets_dispos[i]
            effets_dispos.pop(i)
            
            match effet_choisi:
                case 'plus':
                    valeur_plus = int(input('Combien de cartes doit le plus donner ?'))
                    print('flop')
                case 'interdiction':
                    nb_interdictions = int(input("Combien de joueurs l'interdiction faire passer"))
                    print('ok')
                case 'changer_couleur':
                    print('')
        
    effets = input('cartes a effets (plus2,plus4,interdiction,changer_couleur,changer_sens) avec leurs nombre (ex: plus2:4 plus4:2) : ').split(' ')

    effets_tuple = []

    for effet in effets:
        valeurs = effet.split(':')
        effets_tuple.append((valeurs[0], int(valeurs[1])))

    deck_options = {
        'nom_deck': nom_deck,
        'couleurs': couleurs,
        'nb_max_carte': nb_max_carte,
        'effets_cartes': effets_tuple
    }

    objet_json = j.dumps(deck_options, indent=4)

    open(f"{nom_deck}.json", "w").write(objet_json)


def choisir_deck():
    # Prendre les decks dans le dossier deck_precharges
    liste_decks_noms = os.listdir('deck_precharges')
    liste_decks = []
    for nom in liste_decks_noms:
        liste_decks.append(chargement_deck(f'deck_precharges/{nom}'))

    # Afficher les decks
    for i in range(len(liste_decks)):
        print(f"deck {i} : {liste_decks_noms[i].split('.')[0]}")
        print(f"    - Nombre de cartes par couleurs : {liste_decks[i].get_nombre_max()}")
        print("    - couleurs :")
        for couleur in liste_decks[i].get_couleurs():
            print(f"        - {couleur}")
        print("    - effets :")
        for tuple_effet in liste_decks[i].get_effets():
            texte = f"        - {tuple_effet[0]} apparaissant {tuple_effet[1]} fois "
            if tuple_effet[2]:
                texte += "dans tout le deck qui est multicolore"
            else:
                texte += "par couleur de carte"
            print(texte)

        print(f"({liste_decks[i].get_nombre_cartes()} cartes au total)")
        print("------------------")

    # Demander le choix du deck
    choix = int(input('Choisissez un deck : (chiffre)'))

    return liste_decks[choix]


def choix_deck_host():
    """Permet de choisir un deck prégénèrer ou d'en créer un nouveau"""
    if input('Tu veux créer un deck ? (oui/non)') == 'oui':
        createur_deck()
    return choisir_deck()


#choisir_deck()
createur_deck()
