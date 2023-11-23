import random
from carte import Carte


class Pioche:
    """
    Classe qui représente la pioche du jeu. Elle contient une liste de cartes.
    """

    def __init__(self) -> None:
        self.__liste_cartes = []

    def get_liste_cartes(self) -> list[Carte]:
        """
        :return: la liste des cartes de la pioche
        """
        return self.__liste_cartes

    def ajouter_carte(self, carte: Carte) -> None:
        """
        Ajoute une carte à la pioche
        :param carte: la carte à ajouter
        """
        self.__liste_cartes.append(carte)

    def ajouter_cartes(self, cartes: list[Carte]) -> None:
        """
        Ajoute des cartes à la pioche
        :param cartes: les cartes à ajouter
        """
        for carte in cartes:
            self.ajouter_carte(carte)

    def supprimer_carte(self, carte: list[Carte]) -> None:
        """
        Enlève une carte à la pioche
        :param carte: la carte enlèver
        """
        self.__liste_cartes.remove(carte)

    def melanger_pioche(self) -> None:
        """
        Mélange la pioche
        """
        random.shuffle(self.__liste_cartes)

    def pioche_vide(self) -> bool:
        """
        :return: Un booléen indiquant si la pioche est vide ou non (True si vide, False sinon)
        """
        return len(self.get_liste_cartes()) <= 0

    def cartes_restantes(self) -> int:
        """
        :return: Le nombre de cartes restantes dans la pioche
        """
        return len(self.get_liste_cartes())

    def prendre_cartes(self, nombre: int) -> list[Carte]:
        """
        Prendre un nombre de cartes dans la pioche
        :param nombre: le nombre de cartes à prendre
        :return: la liste des cartes prises
        """
        cartes_prises = []
        for i in range(nombre):
            cartes_prises.append(self.__liste_cartes.pop())

        return cartes_prises

    def __str__(self) -> str:
        """
        :return: une représentation de la pioche sous forme de chaîne de caractères
        """
        res = 'Pioche qui contient:\n'
        for carte in self.get_liste_cartes():
            res += carte.__str__() + '\n'
        return res


class Defausse:
    """
    Classe qui représente la défausse du jeu. Elle contient une liste de cartes.
    """

    def __init__(self) -> None:
        """
        Constructeur de la classe. Initialise une liste vide de cartes.
        """
        self.__liste_cartes = []

    def get_liste_cartes(self) -> list[Carte]:
        """
        :return: la liste des cartes de la défausse
        """
        return self.__liste_cartes

    def ajouter_carte(self, carte: Carte) -> None:
        """
        Ajoute une carte à la défausse
        :param carte: la carte à ajouter
        """
        self.__liste_cartes.append(carte)

    def carte_dessus(self) -> Carte | None:
        """
        :return: la carte du dessus de la défausse ou None si la défausse est vide
        """
        if not self.__liste_cartes:
            return None
        return self.__liste_cartes[-1]

    def pioche_vide(self) -> list[Carte]:
        """
        :return: Toutes les cartes de la défausse sont mélangées sauf la dernière.
        """
        carte_restante = self.__liste_cartes.pop()

        cartes_melangees = []
        for carte in self.__liste_cartes:
            cartes_melangees.append(carte)

        self.__liste_cartes = [carte_restante]

        random.shuffle(cartes_melangees)

        return cartes_melangees

    def defausse_vide(self) -> bool:
        """
        :return: Un booléen indiquant si la défausse est vide ou non (True si vide, False sinon)
        """
        return len(self.get_liste_cartes()) <= 1

    def __str__(self) -> str:
        """
        :return: une représentation de la défausse sous forme de chaîne de caractères
        """
        res = 'La défausse contient : \n'
        for carte in self.get_liste_cartes():
            res += carte.__str__() + '\n'
        return res
