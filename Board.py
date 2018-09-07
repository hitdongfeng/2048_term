from random import sample, choice
from functools import reduce

from Tile import Tile


class Board():
    def __init__(self, size: int):
        self.__width = size
        self.__score = 0
        self.__tiles = [Tile() for i in range(size * size)]
        self.__moves = 0
        init_tiles = sample(self.__tiles, 2)
        for tile in init_tiles:
            tile.val = 2

    def __repr__(self):
        rows = self._rowize(self.tiles)
        rows = list(map(str, rows))
        return '\n'.join(rows)

    @property
    def width(self) -> int:
        return self.__width

    @property
    def tiles(self) -> list:
        return [t.val for t in self.__tiles]

    @property
    def score(self) -> int:
        return self.__score

    @property
    def moves(self) -> int:
        return self.__moves

    @moves.setter
    def moves(self, n):
        self.__moves = n

    @property
    def empty_tiles(self) -> list:
        '''
        Returns a list of the empty Tiles
        '''
        return [t for t in self.__tiles if t.val == 0]

    def spawn(self) -> None:
        '''
        Fills a random empty tile with a value of 2
        '''
        tiles = self.empty_tiles
        if len(tiles):
            to_spawn = choice(tiles)
            to_spawn.val = 2

    def can_collapse(self):
        # TODO:
        # dont allow a move if it does not change the board
        '''
        Checks if a move can be made in any 4 directions. If not, then game is over.
        '''
        rows = self._rowize(self.__tiles)
        columns = self._columnize(self.__tiles)
        row_collapse = False
        col_collapse = False

        for row in rows:
            for i in range(self.__width - 1):
                if row[i].val == 0 or row[i].val == row[i + 1].val:
                    row_collapse = True
                    break
            if row_collapse:
                break

        for col in columns:
            for i in range(self.__width - 1):
                if col[i].val == 0 or col[i].val == col[i + 1].val:
                    col_collapse = True
                    break
            if col_collapse:
                break

        return row_collapse or col_collapse

    def collapse(self, direction) -> bool:
        check_board = self.__tiles
        temp_board = self._columnize(self.__tiles) if direction in ['U', 'D'] else self._rowize(self.__tiles)

        self._push_tiles(temp_board, direction)
        self._add_pairs(temp_board, direction)
        self._push_tiles(temp_board, direction)

        temp_board = self._linearize_col(temp_board) if direction in ['U', 'D'] else self._linearize_row(temp_board)

        # check before assigning
        for i in range(self.__width * self.__width - 1):
            if check_board[i] != temp_board[i]:
                self.__tiles = temp_board
                return True

        return False

    def _push_tiles(self, board, direction):
        for row_i in range(len(board)):
            row = board[row_i]
            row = [tile for tile in row if tile.val != 0]
            filler_tiles = [Tile() for i in range(len(board) - len(row))]
            if direction in ['L', 'U']:
                row.extend(filler_tiles)
            else:
                row = filler_tiles + row
            board[row_i] = row

    def _add_pairs(self, board, direction):
        for row_i in range(len(board)):
            row = board[row_i]
            if direction in ['L', 'U']:
                for i in range(len(row) - 1):
                    if row[i] == row[i + 1]:
                        row[i] = row[i] + row[i + 1]
                        self.__score = self.__score + row[i].val
                        row[i + 1].val = 0
            else:
                for i in reversed(range(1, len(row))):
                    if row[i] == row[i - 1]:
                        row[i] = row[i] + row[i - 1]
                        self.__score = self.__score + row[i].val
                        row[i - 1].val = 0

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
