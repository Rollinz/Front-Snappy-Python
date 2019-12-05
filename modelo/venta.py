class Venta:
    def __init__(self):
        self.__id_mesa = 0
        self.__id_comestible = 0
        self.__id_bebestible = 0
        self.__total = 0

    @property
    def id_mesa(self):
        return self.__id_mesa

    @property
    def total(self):
        return self.__total

    @id_mesa.setter
    def id_mesa(self, id_mesa):
        self.__id_mesa = id_mesa

    @total.setter
    def total(self, total):
        self.__total = total
    
    