import random
from carte import Carte
from effet_carte import EffetCarte

class Joueur:
    def __init__(self, id: int, pseudo: str):
        self.__id = id
        self.__pseudo = pseudo
        self.__liste_cartes = []

    def get_id(self):
        return self.__id

    def get_pseudo(self):
        return self.__pseudo

    def get_liste_cartes(self):
        return self.__liste_cartes

    def ajouter_carte(self, carte):
        self.__liste_cartes.append(carte)

    def supprimer_carte(self, carte):
        liste_cartes = self.get_liste_cartes()

        for i in range(len(liste_cartes)):
            if liste_cartes[i] == carte:
                liste_cartes.pop(i)
                return True
        return False

    def supprimer_carte_indice(self, carte_indice):
        self.get_liste_cartes().pop(carte_indice)
        return True

    def recupere_points(self):
        points = 0
        for carte in self.get_liste_cartes():
            points += carte.get_nombre()
        return points

    def __str__(self):
        res = f'Joueur {self.get_pseudo()} avec id {self.get_id()} possède ces cartes:\n'
        for carte in self.get_liste_cartes():
            res += carte.__str__() + '\n'
        return res

class Participants:
    def __init__(self):
        self.__liste_joueurs = []

    def get_liste_joueurs(self):
        return self.__liste_joueurs

    def get_joueur_id(self, id):
        for joueur in self.get_liste_joueurs():
            if joueur.get_id() == id:
                return joueur
        return None

    def ajouter_joueur(self, joueur):
        self.__liste_joueurs.append(joueur)

    def supprimer_joueur(self, joueur):
        liste_joueurs = self.get_liste_joueurs()

        for i in range(len(liste_joueurs)):
            if liste_joueurs[i] == joueur:
                liste_joueurs.pop(i)
                return True
        return False

    def __str__(self):
        res = 'Participants qui contient:\n'
        for joueur in self.get_liste_joueurs():
            res += joueur.__str__() + '\n'
        return res

cartes_test = [Carte(5, 0, None), Carte(5, 0, None), Carte(5, 0, None)]
class Pioche:
    def __init__(self):
        self.__liste_cartes = cartes_test

    def get_liste_cartes(self):
        return self.__liste_cartes

    def pioche_vide(self):
        return len(self.get_liste_cartes()) <= 0

    def prendre_cartes(self, nombre: int):
        if nombre > len(self.__liste_cartes):
            return []

        cartes_prises = []
        for i in range(nombre):
            cartes_prises.append(self.__liste_cartes.pop())

        return cartes_prises

    def __str__(self):
        res = 'Pioche qui contient:\n'
        for carte in self.get_liste_cartes():
            res += carte.__str__() + '\n'
        return res

class Defausse:
    def __init__(self):
        self.__liste_cartes = []

    def get_liste_cartes(self):
        return self.__liste_cartes

    def ajouter_carte(self, carte):
        self.__liste_cartes.append(carte)

    def carte_dessus(self):
        if not self.__liste_cartes:
            return None
        return self.__liste_cartes[-1]

    def reinitialiser_defausse(self):
        carte_restante = self.__liste_cartes.pop()

        cartes_melangees = []
        for carte in self.__liste_cartes:
            self.carte_melange.append(carte)

        self.__liste_cartes = [carte_restante]

        random.shuffle(cartes_melangees)

        return cartes_melangees

    def __str__(self):
        res = 'Defausse qui contient:\n'
        for carte in self.get_liste_cartes():
            res += carte.__str__() + '\n'
        return res

class Tours:
    def __init__(self):
        self.sens = 1
        self.compteur_tour = 0

class Deck:
    def __init__(self, couleurs: list[str], nombre_max: int, effets: list[tuple[EffetCarte, int, bool]]):
        self.__couleurs = couleurs
        self.__nombre_max = nombre_max
        # tuple de la forme (effet, nb_apparations, une seule couleur)
        self.__effets = effets

    def get_couleurs(self):
        return self.__couleurs

    def get_nombre_max(self):
        return self.__nombre_max

    def get_effets(self):
        return self.__effets

    def creer_deck(self):
        deck = []

        for nombre in range(self.get_nombre_max() + 1):
            for i_couleur in range(len(self.get_couleurs())):
                deck.append(Carte(nombre, i_couleur, None))


        for effet in self.get_effets():
            for i in range(effet[1]):
                if effet[2] is True:
                    deck.append(Carte(effet[0].get_nombre(), None, effet[0]))
                else:
                    for i_couleur in range(len(self.get_couleurs())):
                        deck.append(Carte(effet[0].get_nombre(), i_couleur, effet[0]))
        return deck

    def __str__(self):
        return f'Deck de couleurs: {self.get_couleurs()}, nombre max: {self.get_nombre_max()} et effets {self.get_effets()}'

class Partie:
    def __init__(self, nb_joueurs):
        self.tour = Tours()
        self.initialisation = 0
        self.lst_joueur = []
        for i in range(nb_joueurs):
            self.lst_joueur.append(Joueur(i, f"Joueur {i + 1}"))
        self.defausse = Defausse()
        self.pioche = Pioche()

    def initialisation_partie(self):
        pass
