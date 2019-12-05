class Bebestible:
    def __init__(self):
        self.__id_bebestible = 0
        self.__nombre_bebestible = ''
        self.__precio = 0
    
    @property
    def id_bebestible(self):
        return self.__id_bebestible

    @property
    def nombre_bebestible(self):
        return self.__nombre_bebestible

    @property
    def precio(self):
        return self.__precio

    @id_bebestible.setter
    def id_bebestible(self, id_bebestible):
        self.__id_bebestible = id_bebestible

    @nombre_bebestible.setter
    def nombre_bebestible(self, nombre_bebestible):
        self.__nombre_bebestible = nombre_bebestible

    @precio.setter
    def precio(self, precio):
        self.__precio = precio