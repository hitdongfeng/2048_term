class Tile():
    def __init__(self, n=0):
        self.__val = n

    def __add__(self, other):
        if type(other) is Tile:
            return Tile(self.__val + other.val)
        else:
            raise TypeError('Unable to add incompatible types.')

    def __eq__(self, other):
        if type(other) is Tile:
            return self.__val == other.val
        else:
            raise TypeError('Unable to compare incompatible types.')

    def __str__(self):
        return str(self.__val)

    @property
    def val(self):
        return self.__val

    @val.setter
    def val(self, n):
        if type(n) is int:
            self.__val = n
        else:
            raise TypeError('Assigning bad type for Tile value')
