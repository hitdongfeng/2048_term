class Tile():
    def __init__(self, n=0):
        self._val = n

    def __add__(self, other):
        assert type(other) == Tile, "Error: Trying to add incompatible types."
        return self.val + other.val

    def __eq__(self, other):
        assert type(other) == Tile, "Error: Trying to compare incompatible types."
        return self.val == other.val

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, n):
        self._val = n

    @val.deleter
    def val(self):
        self._val = 0
