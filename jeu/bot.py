from tour import Tours
from joueur import Joueur
from cartes.pile_cartes import Pioche, Defausse
from cartes.carte import Carte
import random


class Bot(Joueur):
    def __init__(self, id: int, name: str):
        super().__init__(id, name)

    def play_turn(self, tour: Tours, pioche: Pioche, defausse: Defausse):
        """
        BOT qui joue un tour
        :param tour: le tour actuel
        :param pioche: pioche du jeu en cours
        :param defausse: defausse du jeu en cours
        :return: None
        """
        choisir_couleur = False
        top_carte = defausse.carte_dessus()

        cartes_compatible = [carte for carte in self.get_liste_cartes() if
                             carte.carte_compatible(top_carte, tour, None, pioche, defausse)]

        if cartes_compatible:

            carte_a_effet = [carte for carte in cartes_compatible if carte.get_carte_effet() is not None]

            if carte_a_effet:
                if len(carte_a_effet) > 1:
                    carte_jouer = carte_a_effet[0]
                    for carte in carte_a_effet:
                        if carte.get_carte_effet().get_nom() == "Interdiction":
                            carte_jouer = carte

                else:
                    carte_jouer = random.choice(carte_a_effet)

                    if carte_jouer.get_carte_effet().get_nom() == "Changer de couleur":
                        choisir_couleur = True

            else:
                carte_jouer = max(cartes_compatible, key=lambda carte: carte.get_valeur())

            defausse.ajouter_carte(carte_jouer)
            self.supprimer_carte(carte_jouer)
            print(f"Bot {self.get_pseudo()} a jouer : {carte_jouer}")

            if choisir_couleur:
                couleur = random.choice(Carte.get_couleur())
                print(f"Bot {self.get_pseudo()} a choisi la couleur : {couleur}")
                defausse.carte_dessus().set_couleur(couleur) # marche pas pour le moment

        else:

            carte_piocher = self.piocher_carte(pioche)
            print(f"Bot {self.get_pseudo()} a piocher : {carte_piocher} ")
