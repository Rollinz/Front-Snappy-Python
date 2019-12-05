class Comestible:
    def __init__(self):
        self.__id_comestible = 0
        self.__nombre_comestible = ''
        self.__precio = 0

    @property
    def id_comestible(self):
        return self.__id_comestible

    @property
    def nombre_comestible(self):
        return self.__nombre_comestible

    @property
    def precio(self):
        return self.__precio

    @id_comestible.setter
    def id_comestible(self, id_comestible):
        self.__id_comestible = id_comestible

    @nombre_comestible.setter
    def nombre_comestible(self, nombre_comestible):
        self.__nombre_comestible = nombre_comestible

    @precio.setter
    def precio(self, precio):
        self.__precio = precio