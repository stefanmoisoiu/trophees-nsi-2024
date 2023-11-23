from carte import Deck
from effet_carte import *
import json

plus_2 = PlusCarte(2)
plus_4 = PlusCarte(4)
choisir_couleur = ChoisirCouleur()
interdiction = Interdiction(1)
changer_sens = ChangerSens()

effet_plus_4 = EffetCarte('plus 4', 50, [plus_4])
effet_changement_sens = EffetCarte('changement de sens', 20, [changer_sens])
effet_interdiction = EffetCarte('interdiction', 20, [interdiction])
effet_joker = EffetCarte('Joker', 50, [plus_4, choisir_couleur])
effet_changement_couleur = EffetCarte('Changemet de couleur', 20, [choisir_couleur])

ficher_a_charger = 'Test JSON/deck.json'
deck_charge = json.load(open(ficher_a_charger,'r'))
print(deck_charge)
effets = []
for effet in deck_charge['effets_cartes']:
    type_effet = effet[0]
    if type_effet == 'plus2':
        effets.append((EffetCarte('plus 2', 20, [plus_2]), effet[1], False))
    if type_effet == 'plus4':
        effets.append((EffetCarte('plus 4', 20, [plus_4]), effet[1], False))
    if type_effet == 'interdiction':
        effets.append((EffetCarte('interdiction', 20, [interdiction]), effet[1], False))
    if type_effet == 'changer_couleur':
        effets.append((EffetCarte('changer de couleur', 20, [choisir_couleur]), effet[1], True))



deck_final = Deck(deck_charge['couleurs'],deck_charge['nb_max_carte'],effets)
        
