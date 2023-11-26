import time
from joueur import Joueur


class Effet:
    # noinspection PyMethodMayBeStatic
    def appliquer(self, tour, participants, pioche, defausse):
        """
        Applique l'effet de la carte
        :param defausse: défausse du jeu (Defausse) (pas utilisé)
        :param pioche: pioche du jeu (Pioche)
        :param participants: liste des participants de la partie (Participants)
        :param tour: tour en cours
        """
        while True:  # quelqu'un pioche
            joueur_suivant = tour.joueur_suivant(participants)
            cartes_joueur_suivant = joueur_suivant.get_liste_cartes()
            nb_cartes_a_piocher = 2

            possede_carte_plus = False
            for carte in cartes_joueur_suivant:

                carte_effet = carte.get_carte_effet()
                if carte_effet is None:
                    continue
                else:
                    for effet in carte_effet.get_effets():
                        if type(effet) is not type(PlusCarte):
                            continue
                        else:
                            possede_carte_plus = True
                            break

            if not possede_carte_plus:
                # le joueur suivant ne peut pas ajouter de cartes +
                print(f"Tu ne peux pas ajouter de cartes +, tu dois piocher {nb_cartes_a_piocher}.")
                time.sleep(2)
                joueur_suivant.piocher_carte_depart(nb_cartes_a_piocher, pioche)
                break

            else:
                choix = int(input(f"Veux-tu piocher {nb_cartes_a_piocher}, veux-tu mettre poser une carte + (0) ou piocher (1) : "))
                if choix == 1:
                    joueur_suivant.piocher_carte_depart(nb_cartes_a_piocher, pioche)
                    break
                else:
                    cartes_plus = []
                    for i in range(len(cartes_joueur_suivant)):
                        carte_joueur_suivant = cartes_joueur_suivant[i]

                        carte_effets = carte_joueur_suivant.get_carte_effet()
                        if carte_effets is None:
                            continue
                        else :
                            for effet in carte_effets.get_effets():
                                if type(effet) is not type(PlusCarte):
                                    continue
                            cartes_plus.append(carte_joueur_suivant)
                            print(f"{i} : {carte_joueur_suivant}")

                    choix_carte = int(input("Quelle carte + veux-tu poser ? "))
                    carte_a_poser = cartes_plus[choix_carte]
                    joueur_suivant.supprimer_carte(carte_a_poser)
                    defausse.ajouter_carte(carte_a_poser)
                    tour.passer_joueurs(1, participants)
                    nb_cartes_a_piocher += 2 # faut mettre en fonction du plus 2 ou plus 4

        pass

    def carte_posable(self, carte, tour, participants, pioche, defausse):
        pass # un peu plus bas, on l'utilise dans la classe EffetCarte, mais on ne l'a pas codée


class EffetCarte:
    """
    Classe qui permet de créer un effet de carte
    """

    def __init__(self, nom: str, points: int, effets: list[Effet]) -> None:
        """
        :param nom: nom de l'effet
        :param points: le nombre de points que l'effet rapporte à la fin de la partie
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
        :return: les points que l'effet rapporte à la fin de la partie
        """
        return self.__points

    def get_effets(self) -> list[Effet]:
        """
        :return: les effets de la carte
        """
        return self.__effets

    def appliquer_effet(self, tour, participants, pioche, defausse) -> None:
        """
        Applique l'effet de la carte
        """
        for effet in self.__effets:
            effet.appliquer(tour, participants, pioche, defausse)

    def carte_posable(self, carte, tour, participants, pioche, defausse) -> bool:
        """
        :param defausse: défausse du jeu
        :param pioche: pioche du jeu
        :param participants: liste des participants de la partie
        :param tour: tour en cours
        :param carte: carte à comparer
        :return: renvoie un boolean si la carte est posable sur celle-ci (pour des conditions spéciales)
        """
        for effet in self.__effets:
            if not effet.carte_posable(carte, tour, participants, pioche,
                                       defausse):  # il n'y a pas de fonction carte_posable dans la classe Effet
                return False
        return True

    def __str__(self) -> str:
        """
        :return: description de l'effet
        """
        return f"Effet {self.get_nom()} de valeur {self.__points}"


class ChoisirCouleur(Effet):
    def appliquer(self, tour, participants, pioche, defausse) -> int:
        """
        Applique l'effet de la carte
        """
        couleur = int(input("Choisissez une couleur: "))
        print(f'Vous avez choisi la couleur : {couleur}')
        return couleur


class PlusCarte(Effet):
    def __init__(self, nb_cartes_a_piocher: int) -> None:
        self.__nb_cartes_a_piocher = nb_cartes_a_piocher

    def get_nb_cartes_a_piocher(self) -> int:
        return self.__nb_cartes_a_piocher

    def appliquer(self, tour, participants, pioche, defausse) -> None:
        """
        Applique l'effet de la carte
        """
        cartes_a_piocher = self.__nb_cartes_a_piocher
        while True:  # quelqu'un pioche
            joueur_suivant = tour.joueur_suivant(participants)
            cartes_joueur_suivant = joueur_suivant.get_liste_cartes()

            possede_carte_plus = False
            for carte in cartes_joueur_suivant:

                carte_effet = carte.get_carte_effet()
                if carte_effet is None:
                    continue

                for effet in carte_effet.get_effets():
                    if type(effet) is not type(PlusCarte):
                        continue

                    possede_carte_plus = True
                    break

            if not possede_carte_plus:
                # le joueur suivant ne peut pas ajouter de cartes +
                print(f"Tu ne peux pas ajouter de cartes +, tu dois piocher {cartes_a_piocher}")
                time.sleep(2)
                self.piocher_cartes_joueur(joueur_suivant, cartes_a_piocher, pioche)
                break

            else:
                choix = int(input(f"Veux-tu piocher {cartes_a_piocher}, veux-tu mettre poser (0) ou piocher (1) : "))
                if choix == 1:  # Pioche
                    self.piocher_cartes_joueur(joueur_suivant, cartes_a_piocher, pioche)
                    break
                else:  # Pose
                    cartes_plus = []
                    for i in range(len(cartes_joueur_suivant)):
                        carte_joueur_suivant = cartes_joueur_suivant[i]

                        carte_effets = carte_joueur_suivant.get_carte_effet()
                        if carte_effets is None:
                            continue
                        for effet in carte_effets.get_effets():
                            if type(effet) is not type(PlusCarte):
                                continue
                        cartes_plus.append(carte_joueur_suivant)
                        print(f"{i} : {carte_joueur_suivant}")

                    choix_carte = int(input("Quelle carte + veux-tu poser ? "))
                    carte_a_poser = cartes_plus[choix_carte]
                    joueur_suivant.supprimer_carte(carte_a_poser)
                    defausse.ajouter_carte(carte_a_poser)
                    tour.passer_joueurs(1, participants)

            tour.passer_joueurs(1, participants)

    def piocher_cartes_joueur(self, joueur, nombre, pioche):
        cartes_prises = pioche.prendre_cartes(nombre)

        for carte in cartes_prises:
            joueur.ajouter_carte(carte)

        print(f"Le joueur a pioché {len(cartes_prises)} cartes")


class Interdiction(Effet):
    def __init__(self, nb_interdictions: int) -> None:
        self.nb_interdictions = nb_interdictions

    def appliquer(self, tour, participants, pioche, defausse) -> None:
        """
        Applique l'effet de la carte
        """
        tour.passer_joueurs(1, participants)
        print("Ta mère la gentille")


class ChangerSens(Effet):
    def appliquer(self, tour, participants, pioche, defausse) -> None:
        """
        Applique l'effet de la carte
        """
        tour.changer_sens()
        print("Le sens du jeu a été changé")
