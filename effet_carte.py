class EffetCarte:
    def __init__(self, nom: str, nombre : int):
        self.__nom = nom
        self.__nombre = nombre

    def get_nom(self):
        return self.__nom

    def get_nombre(self):
        return self.__nombre

    def __str__(self):
        return f"Effet {self.get_nom()} de valeur {self.__nombre}"