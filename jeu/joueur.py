from jeu.cartes.pile_cartes import Pioche
from jeu.cartes.carte import Carte
from jeu.cartes.effet_carte import EffetCarte, PlusCarte, ChoisirCouleur, Interdiction, ChangerSens


def generer_deck_test() -> list[Carte]:
    """
    :return: renvoie une liste de cartes pour tester le jeu
    """
    plus_2 = PlusCarte(2)
    plus_4 = PlusCarte(4)
    choisir_couleur = ChoisirCouleur()
    interdiction = Interdiction(1)
    changer_sens = ChangerSens()

    effets_test = [EffetCarte('Plus 2', 20, [plus_2]),
                   EffetCarte('Plus 4', 50, [plus_4]),
                   EffetCarte('Changer de sens', 20, [choisir_couleur]),
                   EffetCarte('Passer son tour', 20, [interdiction]),
                   EffetCarte('Changer de couleur', 20, [changer_sens])
                   ]
    return [
        # Carte(0, 0, None),
        # Carte(1, 1, None),
        # Carte(2, 2, None),
        # Carte(3, 3, None),
        Carte(0, None, effets_test[0]),
        Carte(0, None, effets_test[0]),
        # Carte(0, None, effets_test[1]),
        # Carte(0, 0, effets_test[2]),
        # Carte(0, 0, effets_test[3]),
        # Carte(0, 0, effets_test[4]),
    ]


class Joueur:
    """
    Classe qui crée un joueur avec un id, un pseudo et une liste de cartes
    """

    def __init__(self, id: int, pseudo: str) -> None:
        """
        :param id (int), pseudo (str)
        :param pseudo: pseudo du joueur
        """
        self.__id: int = id
        self.__pseudo: str = pseudo
        self.__liste_cartes: list[Carte] = []

    def get_id(self) -> int:
        """
        :return: envoie l'id du joueur
        """
        return self.__id

    def get_pseudo(self) -> str:
        """
        :return: envoie le pseudo du joueur
        """
        return self.__pseudo

    def get_liste_cartes(self) -> list[Carte]:
        """
        :return: envoie la liste de carte du joueur (liste de Carte(s))
        """
        return self.__liste_cartes

    def cartes_compatibles(self, carte: Carte, tour, participants, pioche, defausse) -> list[tuple[Carte, bool]]:
        """
        :return: renvoie la liste des cartes compatibles avec la carte du dessus de la défausse
        """
        liste_cartes_compatibles = []
        for carte_joueur in self.get_liste_cartes():
            liste_cartes_compatibles.append(
                (carte_joueur, carte_joueur.carte_compatible(carte, tour, participants, pioche, defausse)))
        return liste_cartes_compatibles

    def ajouter_carte(self, carte) -> None:
        """
        :param carte: La carte piochée par le joueur (Carte)
        :return: rajoute la carte à la liste de cartes du joueur
        """
        self.__liste_cartes.append(carte)

    def uno(self) -> bool:
        """
        :return: bool si il reste une carte au joueur
        """
        if len(self.get_liste_cartes()) == 1:
            return True
        return False

    def supprimer_carte(self, carte) -> bool:
        """
        :param carte: carte choisie par le joueur (Carte)
        :return: renvoie un boolean si la carte a été supprimée ou nou de la liste de carte du joueur
        """
        liste_cartes = self.get_liste_cartes()

        for i in range(len(liste_cartes)):
            if liste_cartes[i] == carte:
                liste_cartes.pop(i)
                return True
        return False

    def supprimer_carte_indice(self, carte_indice: int) -> Carte:
        """
        :param carte_indice: l'indice de la carte choisie par le joueur (int)
        :return: la carte supprimée de la liste de carte du joueur (Carte)
        """
        return self.get_liste_cartes().pop(carte_indice)

    def piocher_cartes_depart(self, pioche: Pioche, nb_cartes: int) -> None:
        """
        :param pioche: la pioche du jeu (Pioche)
        :param nb_cartes: le nombre de carte(s) que le joueur doit piocher (int)
        """
        # self.__liste_cartes = pioche.prendre_cartes(nb_cartes)
        self.__liste_cartes = generer_deck_test()

    def piocher_carte(self, pioche: Pioche) -> Carte:
        """
        :param pioche: la pioche du jeu (Pioche)
        :return: la carte piochée par le joueur (Carte)
        """
        carte = pioche.prendre_cartes(1)[0]
        self.ajouter_carte(carte)
        return carte

    def points_joueur(self) -> int:
        """
        :return: Le nombre de points de la main du joueur (int)
        """
        points = 0
        for carte in self.get_liste_cartes():
            points += carte.get_points()
        return points

    def trier_cartes_joueur(self) -> None:
        """
        Tri les cartes du joueur par couleur
        """
        self.__liste_cartes = self.trier_cartes(self.get_liste_cartes())

    def trier_cartes(self, cartes: list[Carte]) -> list[Carte]:
        """
        Tri les cartes par couleur puis par nombre
        """
        cartes_separees = []
        # (0,[Carte(0,0,None)])

        for carte in cartes:
            for carte_separee in cartes_separees:
                if carte.get_couleur() == carte_separee[0] or (
                        carte.get_couleur() is None and carte_separee[0] == -1):
                    carte_separee[1].append(carte)
                    break
            else:
                tmp = carte.get_couleur()
                if tmp is None:
                    tmp = -1
                cartes_separees.append([tmp, [carte]])

        cartes_separees.sort(key=lambda carte: carte[0])

        for carte_separee in cartes_separees:
            carte_separee[1].sort(key=lambda carte: carte.get_nombre())

        cartes_triees = []
        for carte_separee in cartes_separees:
            cartes_triees.extend(carte_separee[1])

        return cartes_triees

    def plus_de_carte(self) -> bool:
        """
        :return: renvoie un booléen si le joueur n'a plus de carte
        """
        return len(self.get_liste_cartes()) == 0

    def __str__(self) -> str:
        """
        :return: le pseudo du joueur et son id (str) avec ces cartes dans sa main
        """
        res = f'Joueur {self.get_pseudo()} avec id {self.get_id()} possède ces cartes:\n'
        for carte in self.get_liste_cartes():
            res += carte.__str__() + '\n'
        return res


class Participants:
    """
    Classe qui crée une liste de joueurs
    """

    def __init__(self) -> None:
        """
        Initialise la liste de joueurs
        """
        self.__liste_joueurs = []

    def get_liste_joueurs(self) -> list[Joueur]:
        """
        :return: donne la liste de joueurs
        """
        return self.__liste_joueurs

    def get_joueur_par_id(self, id: str) -> Joueur | None:
        """
        :param id: id du joueur
        :return: le joueur qui a l'id donné
        """
        for joueur in self.get_liste_joueurs():
            if joueur.get_id() == id:
                return joueur
        return None

    def creer_joueurs(self, nb_joueurs) -> None:
        """
        :param nb_joueurs: nombre de joueurs dans la partie
        :return: crée la liste de joueurs
        """
        for i in range(nb_joueurs):
            self.ajouter_joueur(Joueur(i, f"Joueur {i + 1}"))

    def ajouter_joueur(self, joueur) -> None:
        """
        :param joueur: instance de la classe joueur
        :return: ajoute le joueur à la liste de joueurs
        """
        self.__liste_joueurs.append(joueur)

    def supprimer_joueur(self, joueur) -> bool:
        """
        :param joueur: instance de la classe joueur
        :return: boolean si le joueur est bien dans la liste de joueurs puis le supprimer
        """
        liste_joueurs = self.get_liste_joueurs()

        for i in range(len(liste_joueurs)):
            if liste_joueurs[i] == joueur:
                liste_joueurs.pop(i)
                return True
        return False

    def distribuer_cartes(self, pioche: Pioche, nb_cartes: int) -> None:
        """
        :param pioche: la pioche du jeu (Pioche)
        :param nb_cartes: le nombre de carte(s) que le joueur doit piocher (int)
        """
        for joueur in self.get_liste_joueurs():
            joueur.piocher_cartes_depart(pioche, nb_cartes)

    def classement_joueurs(self) -> list[Joueur]:
        """
        :return: renvoie la liste des joueurs triés par ordre croissant de points
        """
        liste_joueurs = self.get_liste_joueurs().copy()
        liste_joueurs.sort(key=lambda joueur: joueur.points_joueur(), reverse=True)
        return liste_joueurs

    def __str__(self) -> str:
        """
        :return: la liste des joueurs avec leurs cartes
        """
        res = 'Participants qui contient:\n'
        for joueur in self.get_liste_joueurs():
            res += joueur.__str__() + '\n'
        return res
