import random

from jeu.bot import Bot
from jeu.cartes.carte import Deck
from jeu.cartes.effet_carte import *
from jeu.joueur import Participants
from jeu.cartes.pile_cartes import Pioche, Defausse
from jeu.tour import Tours


class Partie:
    """
    Classe qui gère le déroulement du jeu
    """

    def __init__(self, participants: Participants, deck: Deck, nb_cartes_a_distribuer: int = 7) -> None:
        """
        :param participants: liste des participants de la partie
        :param deck: deck utilisé pour la partie
        :param nb_cartes_a_distribuer: nombre de cartes à distribuer à chaque joueur
        """
        self.__participants: Participants = participants
        self.__deck: Deck = deck
        self.__nb_cartes_a_distribuer: int = nb_cartes_a_distribuer

        self.__tour: Tours

        self.__defausse: Defausse
        self.__pioche: Pioche   

    def initialisation_partie(self) -> None:
        """
        Méthode qui initialise une partie
        """
        self.__defausse = Defausse()
        self.__pioche = Pioche()

        self.__tour = Tours()

        # créer la pioche et melange les cartes
        cartes_jeu = self.__deck.creer_deck()
        random.shuffle(cartes_jeu)
        self.__pioche.ajouter_cartes(cartes_jeu)

        # on distribue les cartes aux joueurs
        self.__participants.distribuer_cartes(self.__pioche, self.__nb_cartes_a_distribuer)

        # on met la premiere carte de la pioche dans la défausse
        self.__defausse.ajouter_carte(self.__pioche.prendre_cartes(1)[0])

        partie_finie = False
        while not partie_finie:
            partie_finie = self.jouer_tour()

    def jouer_tour(self) -> bool:
        """
        Sert à jouer un tour
        """
        return self.__tour.tour_suivant(self.__participants, self.__pioche, self.__defausse)


nb_joueurs = int(input("Combien de joueurs ? "))
participants = Participants()
participants.creer_joueurs(nb_joueurs)

nb_bots = int(input("Combien de bots ? "))
for i in range(nb_bots):
    participants.ajouter_joueur(Bot(i, f"Bot {i + 1}"))

couleurs = ['rouge', 'bleu', 'vert', 'jaune']
numero_max_carte = 9

plus_2 = PlusCarte(2)
plus_4 = PlusCarte(4)
choisir_couleur = ChoisirCouleur()
interdiction = Interdiction(1)
changer_sens = ChangerSens()

effets = [(EffetCarte('plus 2', 20, [plus_2]), 2, False),
          (EffetCarte('plus 4', 50, [plus_4]), 2, True),
          (EffetCarte('changement de sens', 20, [changer_sens]), 2, False),
          (EffetCarte('interdiction', 20, [interdiction]), 2, False),
          (EffetCarte('Joker', 50, [plus_4, choisir_couleur]), 4, True)]

deck = Deck(couleurs, numero_max_carte, effets)
partie = Partie(participants, deck)

partie.initialisation_partie()
