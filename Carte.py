from effet_carte import EffetCarte
class Carte:
    def __init__(self, nombre: int, couleur: int, effet: EffetCarte):

        self.__nombre = nombre
        self.__couleur = couleur
        self.__effet = effet

    def get_nombre(self):
        return self.__nombre

    def get_couleur(self):
        return self.__couleur

    def get_effet(self):
        return self.__effet

    def carte_compatible(self, autre_carte):
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
        return f'Carte de nombre: {self.get_nombre()}, couleur: {self.get_couleur()} et effet {str(self.get_effet())}'