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
        # Make some fancy output for user
        return self.__repr__()

    def __repr__(self):
        rows = self._rowize(self.tiles)
        rows = list(map(str, rows))
        return '\n'.join(rows)

    @property
    def size(self) -> int:
        return self._size

    @property
    def tiles(self) -> list:
        return [t.val for t in self._tiles]

    @property
    def score(self) -> int:
        return self._score

    @property
    def empty_tiles(self) -> list:
        '''
        Returns a list of the empty Tiles
        '''
        return [t for t in self._tiles if t.val == 0]

    def spawn(self) -> None:
        '''
        Fills a random empty tile with a value of 2
        '''
        tiles = self.empty_tiles
        if len(tiles):
            to_spawn = choice(tiles)
            to_spawn.val = 2

    def can_collapse(self) -> bool:
        '''
        Checks if a move can be made in any 4 directions. If not, then game is over.
        '''
        rows = self._rowize(self._tiles)
        columns = self._columnize(self._tiles)
        row_collapse = False
        col_collapse = False

        for row in rows:
            for i in range(self.size - 1):
                if row[i].val == 0 or row[i].val == row[i + 1].val:
                    row_collapse = True
                    break
            if row_collapse:
                break

        for col in columns:
            for i in range(self.size - 1):
                if col[i].val == 0 or col[i].val == col[i + 1].val:
                    col_collapse = True
                    break
            if col_collapse:
                break

        return row_collapse or col_collapse

    def collapse(self, direction: str) -> None:
        '''
        Collapses the board toward a given direction, merging tiles of the same
        value and empty tiles with filled tiles.
        '''
        if direction in ['U', 'D']:
            temp_board = self._columnize(self._tiles)
        else:
            temp_board = self._rowize(self._tiles)

        if direction in ['L', 'U']:
            row_i = 0
            while row_i < len(temp_board):
                row = temp_board[row_i]
                # add pairs
                for i in range(len(row) - 1): # offset to not iterate last tile
                    if row[i] == row[i + 1]:
                        row[i] = row[i] + row[i + 1]
                        self._score = self._score + row[i].val
                        row[i + 1].val = 0
                # collapse
                # remove all zeroes, then append until len(row)
                row = [tile for tile in row if tile.val != 0]
                row.extend([0] * (len(temp_board) - len(row)))
                row_i += 1
        else:
            row_i = 0
            while row_i < len(temp_board):
                row = temp_board[row_i]
                # add pairs
                for i in reversed(range(1, len(row))):
                    if row[i] == row[i - 1]:
                        row[i] = row[i] + row[i - 1]
                        self._score = self._score + row[i].val
                        row[i - 1].val = 0
                # collapse
                # remove all zeroes, then prepend until len(row)
                row = [tile for tile in row if tile.val != 0]
                row = [0] * (len(temp_board) - len(row)) + row
                row_i += 1

        if direction in ['U', 'D']:
            self._tiles = self._linearize_col(temp_board)
        else:
            self._tiles = self._linearize_row(temp_board)

    def _rowize(self, l):
        '''
        Given a linear list, returns a list of lists of the tiles in row major order.
        '''
        width = int(len(l) ** 0.5)
        rows = [[] for i in range(width)]
        for i in range(len(l)):
            rows[i // width].append(l[i])
        return rows

    def _columnize(self, l):
        '''
        Given a linear list, returns a list of lists of the tiles in column major order.
        '''
        width = int(len(l) ** 0.5)
        cols = [[] for i in range(width)]
        for i in range(len(l)):
            cols[i % width].append(l[i])
        return cols

    def _linearize_row(self, l):
        '''
        Given a list of lists in row major order, return a list of its linear
        representation.
        '''
        return reduce(lambda x, y: x + y, l)

    def _linearize_col(self, l):
        '''
        Given a list of lists in column major order, return a list of its linear
        representation.
        '''
        res = []
        for i in range(len(l) ** 2):
            res.append(l[i % len(l)].pop(0))
        return res
