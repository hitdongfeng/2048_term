from random import sample, choice
from functools import reduce

from Tile import Tile


class Board():
    def __init__(self, size: int):
        self._size = size
        self._score = 0
        self._tiles = [Tile() for i in range(size * size)]
        init_tiles = sample(self._tiles, 2)
        for tile in init_tiles:
            tile.val = 2

    def __str__(self):
        # TODO
        # Make some fancy output for user
        return self.__repr__()

    def __repr__(self):
        rows = self._rowize()
        rows = list(map(str, rows))
        return '\n'.join(rows)

    @property
    def size(self):
        return self._size

    @property
    def tiles(self):
        return [t.val for t in self._tiles]

    @property
    def score(self):
        return self._score

    @property
    def empty_tiles(self):
        '''
        Returns a list of the empty Tiles
        '''
        return [t for t in self._tiles if t.val == 0]

    def spawn(self):
        '''
        Fills a random empty tile with a value of 2
        '''
        empty_tiles = self.empty()
        to_spawn = choice(empty_tiles)
        to_spawn.val = 2

    def can_collapse(self) -> bool:
        '''
        Checks if the board can be collapsed. If not, then game is over.
        '''
        rows = self._rowize()
        columns = self._columnize()
        row_collapse = False
        col_collapse = False

        for row in rows:
            for i in range(self.size - 1):
                if row[i].val != 0 and row[i].val == row[i + 1].val:
                    row_collapse = True

        for col in columns:
            for i in range(self.size - 1):
                if col[i].val != 0 and col[i].val == col[i + 1].val:
                    col_collapse = True

        return row_collapse or col_collapse

    def collapse(self, direction: str):
        # if 3 or more in a row start collapsing from direction side first
        # fill after collapsing
        if direction == 'U':
            temp_board = self._columnize()
        elif direction == 'D':
            temp_board = self._columnize()
        elif direction == 'L':
            temp_board = self._rowize()
        elif direction == 'R':
            temp_board = self._rowize()
            for row in temp_board:
                # possibly change below to while loop
                for i in reversed(range(len(row) - 1)):
                    if row[i] == 0:
                        # collapse down here
                        pass
                    if row[i] == row[i - 1]:
                        row[i] = row[i] * 2

    def _rowize(self):
        '''
        Returns a list of lists of the tiles in row major order.
        '''
        rows = []
        for i in self.size:
            rows.append([])
        for i in range(len(self._tiles)):
            rows[i // self.size].append(self._tiles[i])
        return rows

    def _columnize(self):
        '''
        Returns a list of lists of the tiles in column major order.
        '''
        cols = []
        for i in self.size:
            cols.append([])
        for i in range(len(self._tiles)):
            cols[i % self.size].append(self._tiles[i])
        return cols

    def linearize_row(l):
        return reduce(lambda x, y: x + y, l)

    def linearize_col(self):
        pass
