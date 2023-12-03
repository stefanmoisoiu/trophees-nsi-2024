from jeu.cartes.effet_carte import EffetCarte


class Carte:
    def __init__(self, nombre: int, couleur: int | None, effet: EffetCarte | None) -> None:
        """
        Entree : nombre (int), couleur (int), effet (EffetCarte)
        Initialise une carte avec un nombre, couleur et/ou effet.
        """
        self.__nombre = nombre

        if effet is None:
            self.__points = nombre
        else:
            self.__points = effet.get_points()

        self.__couleur = couleur
        self.__effet = effet

    def get_nombre(self) -> int:
        """
        : return le nombre de la carte
        """
        return self.__nombre

    def get_couleur(self) -> int:
        """
        :return: la couleur de la carte
        """
        return self.__couleur

    def get_carte_effet(self) -> EffetCarte:
        """
        :return: l'effet de la carte
        """
        return self.__effet

    def appliquer_effet_carte(self, tour, participants, pioche, defausse) -> None:
        """ Applique l'effet de la carte """
        if self.__effet is None:
            return
        self.__effet.appliquer_effet(tour, participants, pioche, defausse)

    def get_points(self) -> int:
        """
        :return: le nombre de points de la carte
        """
        return self.__points

    def carte_compatible(self, autre_carte, tour, participants, pioche,
                         defausse) -> bool:  # tour, participants, pioche et defausse ne sont pas utilisés.
        """
        :param autre_carte: carte à comparer
        :param tour: tour en cours
        :param participants: liste des participants de la partie
        :param pioche: pioche du jeu
        :param defausse: défausse du jeu
        :return: renvoie un boolean si les cartes proposées sont compatibles
        """
        autre_effet = autre_carte.get_carte_effet()
        notre_effet = self.get_carte_effet()

        if self.get_couleur() is None:
            return True
        if notre_effet is not None and autre_effet is not None and autre_effet == notre_effet:
            return True
        if notre_effet is None and autre_effet is None and autre_carte.get_nombre() == self.get_nombre():
            return True
        if autre_carte.get_couleur() == self.get_couleur():
            return True

        return False

    def __str__(self) -> str:
        """
        :return: description de la carte
        """
        return f'Carte de nombre: {self.get_nombre()}, couleur: {self.get_couleur()} et effet {str(self.get_carte_effet())}'


class Deck:
    """
    Classe permettant de créer un deck de cartes
    """

    def __init__(self, couleurs: list[str], numero_max_carte: int, effets: list[tuple[EffetCarte, int, bool]]) -> None:
        """
        :param couleurs: liste des couleurs du deck
        :param numero_max_carte: le numéro max que les cartes peuvent
        avoir (ex : 9 pour le UNO classique)
        :param effets: liste des effets du deck sous la forme (effet, nombre d'apparitions par couleur, la carte est multi-couleur)
        """
        self.__couleurs = couleurs
        self.__nombre_max = numero_max_carte
        self.__effets = effets

    def get_couleurs(self) -> list[str]:
        """
        :return: renvoie les couleurs du decks
        """
        return self.__couleurs

    def get_nombre_max(self) -> int:
        """
        :return le numéro max que les cartes peuvent avoir (ex: 9 pour le UNO classique)
        """
        return self.__nombre_max

    def get_effets(self) -> list[tuple[EffetCarte, int, bool]]:
        """
        :return: l'effet de la carte
        """
        return self.__effets

    def creer_deck(self) -> list[Carte]:
        """
        :return: renvoie le deck de cartes complet avec les effets et les couleurs
        """
        deck = []

        for nombre in range(self.get_nombre_max() + 1):
            for i_couleur in range(len(self.get_couleurs())):
                deck.append(Carte(nombre, i_couleur, None))

        for effet in self.get_effets():
            for i in range(effet[1]):
                if effet[2] is True:
                    deck.append(Carte(0, None, effet[0]))
                else:
                    for i_couleur in range(len(self.get_couleurs())):
                        deck.append(Carte(0, i_couleur, effet[0]))
        return deck

    def __str__(self) -> str:
        """
        :return: description du deck
        """
        return f'Deck de couleurs: {self.get_couleurs()}, nombre max: {self.get_nombre_max()} et effets {self.get_effets()}'
