import json as j

nom_deck = input('nom du deck : ')
couleurs = input('couleurs présentes (écrire séparé par des espaces) : ').split(' ')
nb_max_carte = int(input('valeur maximale des cartes : '))
effets = input('cartes a effets (plus2,plus4,interdiction,changer_couleur) avec leurs nombre (ex: plus2:4 plus4:2) : ').split(' ')
effets_tuple = []
for effet in effets:
    valeurs = effet.split(':')
    effets_tuple.append((valeurs[0],int(valeurs[1])))

deck_options = {
    'nom_deck':nom_deck,
    'couleurs':couleurs,
    'nb_max_carte':nb_max_carte,
    'effets_cartes':effets_tuple
}

objet_json = j.dumps(deck_options,indent=4)

open(f"{nom_deck}.json", "w").write(objet_json)