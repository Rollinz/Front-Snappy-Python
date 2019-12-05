class Mesa:
    def __init__(self):
        self.__id_mesa = 0
        self.__numero_mesa = 0

    @property
    def id_mesa(self):
        return self.__id_mesa

    @property
    def numero_mesa(self):
        return self.__numero_mesa

    @id_mesa.setter
    def id_mesa(self, i):
        self.__id_mesa = i
    
    @numero_mesa.setter
    def numero_mesa(self, n):
        self.__numero_mesa = n