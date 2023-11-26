from carte import Carte  # not used
from joueur import Participants, Joueur
from pile_cartes import Pioche, Defausse


class Tours:
    """ Classe qui gère les tours du jeu"""

    def __init__(self) -> None:
        """
        Initialise le sens du jeu (1 pour le sens normal, -1 pour le sens inverse)
        """
        self.__sens = 1
        self.__compteur_tour = 1
        self.__indice_joueur = 0

    def get_sens(self) -> int:
        """
        :return: le sens du jeu
        """
        return self.__sens

    def get_compteur_tour(self) -> int:
        """
        :return: le compteur de tour
        """
        return self.__compteur_tour

    def changer_sens(self) -> None:
        """
        Change le sens du jeu
        """
        self.__sens *= -1

    def joueur_actuel(self, participants: Participants) -> Joueur:
        """
        :param participants: les participants de la partie
        :return: le joueur actuel
        """
        return participants.get_liste_joueurs()[self.__indice_joueur]

    def joueur_suivant(self, participants: Participants) -> Joueur:
        """
        :param participants: les participants de la partie
        :return: le joueur suivant
        """
        indice_joueur_suivant = self.__indice_joueur + self.get_sens()
        indice_joueur_suivant = self.garder_indice_dans_tableau(indice_joueur_suivant, participants.get_liste_joueurs())
        return participants.get_liste_joueurs()[indice_joueur_suivant]

    def passer_tour(self) -> None:
        """
        Passe le tour
        """
        self.__compteur_tour += 1 * self.__sens

    def passer_joueurs(self, nombre: int, participants: Participants) -> None:
        """
        :param nombre: nombre de joueurs à passer
        :param participants: les participants de la partie
        """
        self.__indice_joueur += nombre * self.__sens
        self.__indice_joueur = self.garder_indice_dans_tableau(self.__indice_joueur, participants.get_liste_joueurs())
        self.passer_tour()

    def garder_indice_dans_tableau(self, indice: int, tab: list) -> int:
        """
        :param indice : indice du tableau
        :param tab : tableau
        Sert à ne pas dépasser les bornes du tableau
        :return: l'indice (changé si dépasse les bornes)
        """
        if indice < 0:
            indice = len(tab) - abs(indice) % (len(tab) + 1)
        else:
            indice = indice % len(tab)
        return indice

    def texte_main_joueur(self, joueur, cartes_compatibles, participants: Participants, pioche: Pioche,
                          defausse: Defausse) -> str:  # joueur, participants, pioche et defausse ne sont pas utilisés.
        """
        :param joueur: le joueur actuel
        :param cartes_compatibles: les cartes compatibles avec la carte du dessus de la défausse
        :param participants: les participants de la partie
        :param pioche: la pioche du jeu
        :param defausse: la défausse du jeu
        :return: le texte qui affiche les cartes du joueur
        """
        res = ""
        for i in range(len(cartes_compatibles)):
            cartes_compatible = cartes_compatibles[i]

            res += f"{i} : {str(cartes_compatible[0])}"

            if cartes_compatible[1]:
                res += " ✔️"
            else:
                res += " ❌"
            res += "\n"

        return res

    def verifier_pile_cartes(self, pioche: Pioche, defausse: Defausse) -> bool:
        """
        Méthode qui vérifie si la partie est finie ou non
        :param pioche: la pioche du jeu
        :param defausse: la défausse du jeu
        :return: un booléen qui indique si la pioche et la défausse sont vides ou non
        """
        if pioche.pioche_vide() and defausse.defausse_vide():
            return True

        if pioche.pioche_vide():
            pioche.ajouter_cartes(defausse.pioche_vide())

        return False

    def pioche_forcee(self, cartes_compatibles) -> bool:
        """
        :param cartes_compatibles: les cartes compatibles avec la carte du dessus de la défausse
        :return: un booléen qui indique si le joueur doit être forcé à piocher ou non.
        """
        for carte_compatible in cartes_compatibles:
            if carte_compatible[1]:
                return False
        return True

    def tour_fini(self, participants: Participants) -> None:
        """
        Méthode qui gère la fin d'un tour
        :param participants: les participants de la partie
        """
        self.passer_joueurs(1, participants)

    def tour_suivant(self, participants: Participants, pioche: Pioche, defausse: Defausse) -> bool:
        """
        Méthode qui gére le déroulement d'un tour
        :param participants: participants a la partie
        :param pioche: pioche du jeu
        :param defausse: défausse du jeu
        :return bool: si la partie est finie ou non (True si la partie est fini, False sinon)
        """
        partie_finie = self.verifier_pile_cartes(pioche, defausse)
        if partie_finie:
            print("La partie est finie, il n'y a plus de cartes dans la pioche et dans la défausse.")
            return True

        joueur = self.joueur_actuel(participants)
        carte_dessus = defausse.carte_dessus()

        cartes_compatibles = joueur.cartes_compatibles(defausse.carte_dessus(), self, participants, pioche, defausse)

        joueur.trier_cartes_joueur()

        print(f"TOUR {self.__compteur_tour} \n")
        print(f"Voici la carte sur la défausse : \n{str(carte_dessus)} \n")
        print(f"Voici les cartes du joueur {joueur.get_pseudo()} : ")
        print(self.texte_main_joueur(joueur, cartes_compatibles, participants, pioche, defausse))

        if self.pioche_forcee(cartes_compatibles):
            print("Vous n'avez pas de carte compatible, vous devez piocher.")
            carte_piochee = joueur.piocher_carte(pioche)
            print(f"Vous avez pioché la carte : \n{str(carte_piochee)} \n")
            self.tour_fini(participants)
            return False

        print("\n\n0 : Piocher une carte \n1 : Jouer une carte \n")
        choix = input("Que voulez-vous faire ? ")

        if choix == "0":
            carte_piochee = joueur.piocher_carte(pioche)
            print(f"Vous avez pioché la carte : \n{str(carte_piochee)} \n")
            self.tour_fini(participants)
            return False

        while True:
            indice_carte = int(input("Quelle carte voulez-vous jouer ? (Donnez l'indice de la carte) "))
            if cartes_compatibles[indice_carte][1]:
                carte_jouee = joueur.supprimer_carte_indice(indice_carte)
                break
            else:
                print("Vous ne pouvez pas jouer cette carte, veuillez en choisir une autre.")

        carte_jouee.appliquer_effet_carte(self, participants, pioche, defausse)

        defausse.ajouter_carte(carte_jouee)

        print("Vous avez joué la carte : \n" + str(carte_jouee) + "\n")

        self.tour_fini(participants)
