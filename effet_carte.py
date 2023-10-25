class Effet:
    def appliquer(self, tour, participants, pioche, defausse):
        pass

    def carte_posable(self, carte, tour, participants, pioche, defausse) -> bool:
        """
        :param carte: carte à comparer
        :return: renvoie un boolean si la carte est posable sur celle-ci (pour des conditions spéciales)
        """
        return True
class EffetCarte:
    """
    Classe qui permet de créer un effet de carte
    """

    def __init__(self, nom: str, points: int, effets: list[Effet]) -> None:
        """
        :param nom: nom de l'effet
        :param points: points que l'effet rapporte a la fin de la partie
        """
        self.__nom = nom
        self.__points = points
        self.__effets = effets

    def get_nom(self) -> str:
        """
        :return: le nom de l'effet
        """
        return self.__nom

    def get_points(self) -> int:
        """
        :return: les points que l'effet rapporte a la fin de la partie
        """
        return self.__points

    def appliquer_effet(self, tour, participants, pioche, defausse):
        """
        Applique l'effet de la carte
        """
        for effet in self.__effets:
            effet.appliquer(tour, participants, pioche, defausse)

    def carte_posable(self, carte, tour, participants, pioche, defausse) -> bool:
        """
        :param carte: carte à comparer
        :return: renvoie un boolean si la carte est posable sur celle-ci (pour des conditions spéciales)
        """
        for effet in self.__effets:
            if not effet.carte_posable(carte, tour, participants, pioche, defausse):
                return False
        return True

    def __str__(self) -> str:
        """
        :return: description de l'effet
        """
        return f"Effet {self.get_nom()} de valeur {self.__points}"
class ChoisirCouleur(Effet):
    def appliquer(self, tour, participants, pioche, defausse):
        """
        Applique l'effet de la carte
        """
        couleur = int(input("Choisissez une couleur: "))
        print(f'Vous avez choisi la couleur : {couleur}')
        return couleur
class PlusCarte(Effet):
    def __init__(self, nb_cartes_a_piocher: int):
        self.__nb_cartes_a_piocher = nb_cartes_a_piocher
    def get_nb_cartes_a_piocher(self):
        return self.__nb_cartes_a_piocher
    def appliquer(self, tour, participants, pioche, defausse):
        """
        Applique l'effet de la carte
        """

        joueur_suivant = tour.joueur_suivant(participants)

        cartes_joueur_suivant = joueur_suivant.get_liste_cartes()
        for carte in cartes_joueur_suivant:
            if type(carte) is type(PlusCarte):
                print("Le joueur suivant a déjà une carte +")
                return

        cartes_supplementaires_a_piocher = 0

        cartes_defausse = defausse.get_liste_cartes()
        for i in range(len(cartes_defausse)-1,0, -1):
            if type(cartes_defausse[i]) is type(PlusCarte):
                cartes_supplementaires_a_piocher += cartes_defausse[i].get_nb_cartes_a_piocher()
            else:
                break


        cartes_prises = pioche.prendre_cartes(self.__nb_cartes_a_piocher + cartes_supplementaires_a_piocher)
        for carte in cartes_prises:
            joueur_suivant.ajouter_carte(carte)
        print(f"Le joueur a pioché {len(cartes_prises)} cartes")

        tour.passer_joueurs(1, participants)
class Interdiction(Effet):
    def __init__(self, nb_interdictions: int):
        self.nb_interdictions = nb_interdictions

    def appliquer(self, tour, participants, pioche, defausse):
        """
        Applique l'effet de la carte
        """
        tour.passer_joueurs(1, participants)
        print("Ta mère la gentille")
class ChangerSens(Effet):
    def appliquer(self, tour, participants, pioche, defausse):
        """
        Applique l'effet de la carte
        """
        tour.changer_sens()
        print("Le sens du jeu a été changé")