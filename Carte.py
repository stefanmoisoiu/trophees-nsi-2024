import random

class Carte:
    def __init__(self,nombre:int, couleur:int, effet:int):
        
        self.__nombre = nombre
        self.__couleur = couleur
        self.__effet = effet
    
    def get_nombre(self):
        return self.__nombre
    def get_couleur(self):
        return self.__couleur
    def get_effet(self):
        return self.__effet
    
    def carte_compatible(self,autre_carte):
        autre_effet = autre_carte.get_effet()
        notre_effet = self.get_effet()
        
        if notre_effet is not None and autre_effet is not None and autre_effet == notre_effet:
            return True
        if notre_effet is None and autre_effet is None and autre_carte.get_nombre() == self.get_nombre():
            return True
        if autre_carte.get_couleur() == self.get_couleur():
            return True
        
        return False
    
    def __str__(self):
        return f'Carte de nombre: {self.get_nombre()}, couleur: {self.get_couleur()} et effet {self.get_effet()}'

class Joueur:
    def __init__(self, id:int, pseudo:str):
        self.__id = id
        self.__pseudo = pseudo
        self.__liste_cartes = []
    
    def get_id(self):
        return self.__id
    def get_pseudo(self):
        return self.__pseudo
    def get_liste_cartes(self):
        return self.__liste_cartes
    def ajouter_carte(self,carte):
        self.__liste_cartes.append(carte)
    
    def supprimer_carte(self,carte):
        liste_cartes = self.get_liste_cartes()
        
        for i in range(len(liste_cartes)):
            if liste_cartes[i] == carte:
                liste_cartes.pop(i)
                return True
        return False
    
    def supprimer_carte_indice(self,carte_indice):
        self.get_liste_cartes().pop(carte_indice)
        return True
    
    def recupere_points(self):
        points = 0
        for carte in liste_cartes:
            points += carte.get_nombre()
        return points
    
    def __str__(self):
        res = f'Joueur {self.get_pseudo()} avec id {self.get_id()} possède ces cartes:\n'
        for carte in self.get_liste_cartes():
            res += carte.__str__() + '\n'
        return res

class Pioche:
    def __init__(self):
        self.__liste_cartes = [Carte(5,0,None),Carte(5,0,None),Carte(5,0,None)]
    
    def get_liste_cartes(self):
        return self.__liste_cartes
    
    def pioche_vide(self):
        return len(self.get_liste_cartes()) <= 0
    
    def prendre_cartes(self,nombre:int):
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
    
    def ajouter_carte(self,carte):
        self.__liste_cartes.append(carte)
    
    def carte_dessus(self):
        if self.__liste_cartes == []:
            return None
        return self.__liste_cartes[-1]
    
    def reinitialiser_defausse(self):
        carte_restante = self.__liste_cartes.pop()
        
        cartes_melangees = []
        for carte in self.__liste_cartes:
            cartes_melanges.append(carte)
        
        self.__liste_cartes = [carte_restante]
        
        random.shuffle(cartes_melangees)
        
        return cartes_melangees
    
    def __str__(self):
        res = 'Defausse qui contient:\n'
        for carte in self.get_liste_cartes():
            res += carte.__str__() + '\n'
        return res
        