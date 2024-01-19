import time


class Effet:
    def appliquer(self, tour, participants, pioche, defausse) -> None:
        """
        Applique l'effet de la carte
        :param defausse: défausse du jeu (Defausse) (pas utilisé)
        :param pioche: pioche du jeu (Pioche)
        :param participants: liste des participants de la partie (Participants)
        :param tour: tour en cours
        """
        pass


class EffetCarte:
    """
    Classe qui permet de créer un effet de carte
    """

    def __init__(self, nom: str, points: int, effets: list[Effet]) -> None:
        """
        :param nom: nom de l'effet
        :param points: le nombre de points que l'effet rapporte à la fin de la partie
        :param effets: les effets de la carte
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
        :param defausse: défausse du jeu
        :param pioche: pioche du jeu
        :param participants: liste des participants de la partie
        """
        for effet in self.__effets:
            effet.appliquer(tour, participants, pioche, defausse)

    def __str__(self) -> str:
        """
        :return: description de l'effet
        """
        return f"Effet {self.get_nom()} de valeur {self.__points}"


class ChoisirCouleur(Effet):
    def appliquer(self, tour, participants, pioche, defausse) -> int:
        """
        Applique l'effet de la carte
        :param defausse: défausse du jeu
        :param pioche: pioche du jeu
        :param participants: liste des participants de la partie
        """
        couleur = int(input("Choisissez une couleur: "))
        print(f'Vous avez choisi la couleur : {couleur}')
        return couleur


class PlusCarte(Effet):
    def __init__(self, nb_cartes_a_piocher: int) -> None:
        """
        :param nb_cartes_a_piocher: nombre de cartes à piocher
        """
        self.__nb_cartes_a_piocher = nb_cartes_a_piocher

    def get_nb_cartes_a_piocher(self) -> int:
        """
        :return: le nombre de cartes à piocher
        """
        return self.__nb_cartes_a_piocher

    def appliquer(self, tour, participants, pioche, defausse) -> None:
        """
        Applique l'effet de la carte
        :param defausse: défausse du jeu (Defausse) (pas utilisé)
        :param pioche: pioche du jeu (Pioche)
        :param participants: liste des participants de la partie (Participants)
        :param tour: tour en cours
        """
        cartes_a_piocher = self.__nb_cartes_a_piocher
        tour.passer_joueurs(1, participants)
        print(f"/n PASSE TOUR : {tour.get_compteur_tour()}")

        while True:  # quelqu'un pioche
            joueur_actuel = tour.joueur_actuel(participants)

            carte_plus_dans_deck = self.possede_carte_plus(joueur_actuel)

            if not carte_plus_dans_deck:
                # le joueur suivant ne peut pas ajouter de cartes +
                print(f"Tu ne peux pas ajouter de cartes +, tu dois piocher {cartes_a_piocher}")
                time.sleep(2)
                self.piocher_cartes_joueur(joueur_actuel, cartes_a_piocher, pioche)
                break

            else:
                choix = int(input(f"Pioche {cartes_a_piocher} cartes (0) ou pose une autre carte + dessus (1) : "))
                if choix == 0:  # Pioche
                    self.piocher_cartes_joueur(joueur_actuel, cartes_a_piocher, pioche)
                    break
                else:  # Pose
                    cartes_plus = self.recupere_cartes_plus_joueur(joueur_actuel)
                    for i in range(len(cartes_plus)):
                        print(f"{i} : {cartes_plus[i]}")

                    choix_carte = int(input("Quelle carte + veux-tu poser ? "))

                    carte_a_poser = cartes_plus[choix_carte]
                    cartes_a_piocher += self.get_nb_cartes_a_piocher()
                    joueur_actuel.supprimer_carte(carte_a_poser)
                    defausse.ajouter_carte(carte_a_poser)
                    tour.passer_joueurs(1, participants)
                    print("PASSER TOUR3")
                    print(f"TOUR : {tour.get_compteur_tour()}")

    def possede_carte_plus(self, joueur) -> bool:
        """
        Pour vérifier si le joueur possède une carte +
        :param joueur: le joueur à vérifier
        :return: True si le joueur possède une carte +, False sinon
        """
        cartes_joueur_suivant = joueur.get_liste_cartes()

        for carte in cartes_joueur_suivant:
            carte_effet = carte.get_carte_effet()
            if carte_effet is None:
                continue

            for effet in carte_effet.get_effets():
                if isinstance(effet, PlusCarte):
                    return True
        return False

    def piocher_cartes_joueur(self, joueur, nombre, pioche) -> None:
        """
        Fait piocher des cartes au joueur.
        :param joueur: Le joueur qui pioche
        :param nombre: le nombre de cartes à piocher
        :param pioche: la pioche du jeu
        :return: None
        """
        cartes_prises = pioche.prendre_cartes(nombre)

        for carte in cartes_prises:
            joueur.ajouter_carte(carte)

        print(f"Le joueur a pioché {len(cartes_prises)} cartes")

    def recupere_cartes_plus_joueur(self, joueur) -> list:
        """
        Récupère les cartes + du joueur
        :param joueur: le joueur
        :return: une liste des cartes + du joueur
        """
        cartes_joueur_suivant = joueur.get_liste_cartes()
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

        return cartes_plus


class Interdiction(Effet):
    """La class Interdiction qui permet de créer un effet interdictions"""

    def __init__(self, nb_interdictions: int) -> None:
        """
        :param nb_interdictions: le nombre d'interdictions
        """
        self.nb_interdictions = nb_interdictions

    def appliquer(self, tour, participants, pioche, defausse) -> None:
        """
        Applique l'effet de la carte
        :param defausse: défausse du jeu
        :param pioche: pioche du jeu
        :param participants: liste des participants de la partie
        """
        tour.passer_joueurs(1, participants)
        print("Ta mère la gentille")


class ChangerSens(Effet):
    def appliquer(self, tour, participants, pioche, defausse) -> None:
        """
        Applique l'effet de la carte
        :param defausse: défausse du jeu
        :param participants: liste des participants de la partie
        :param pioche: pioche du jeu
        :param tour: tour en cours
        """
        tour.changer_sens()
        print("Le sens du jeu a été changé")
