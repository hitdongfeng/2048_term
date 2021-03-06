import os

from Board import Board


class Engine():
    def __init__(self):
        size = self._get_settings()
        self.__board = Board(size)

    def _get_settings(self):
        '''
        Get the following settings for the game setup:
        1) Board size
        '''
        os.system('clear')
        size = input('What is your board size? 4x4, 5x5, etc.\n>>> ')
        assert int(size[0]) > 1, 'Board size must be 2x2 or more.'
        size = int(size[0])
        return size

    def start(self):
        while len(self.__board.empty_tiles) > 1 or self.__board.can_collapse():
            self._output()
            move = self._get_move()
            if move in ['U', 'D', 'L', 'R']:
                change = self.__board.collapse(move)
                if change:
                    self.__board.moves += 1
                    self.__board.spawn()
            else:
                # Add support for restarting, quitting
                pass
        self._end()

    def _get_move(self):
        # TODO:
        # Change so the user doesn't have to press 'Enter' every time.
        # Change so there is no output when user types in something that fails
        move = input('>>> ')
        try:
            move = self._process_move(move)
        except ValueError as e:
            print('ValueError: ', e)
            move = self._get_move()
        return move

    def _process_move(self, move):
        move = move.lower()
        if move in ['w', 'k']:
            return 'U'
        elif move in ['s', 'j']:
            return 'D'
        elif move in ['a', 'h']:
            return 'L'
        elif move in ['d', 'l']:
            return 'R'
        else:
            raise ValueError('Your move \'{}\' is not recognized.'.format(move))

    def _output(self):
        os.system('clear')
        print('Score: {}'.format(self.__board.score))
        print('Move: {}'.format(self.__board.moves))
        print()
        self._print_board()
        print()
        print('Moves:\nW, K => Up\nS, J => Down\nA, H => Left\nD, L => Right')

    def _print_board(self):
        i = 0
        tiles = self.__board.tiles
        for row in range(self.__board.width):
            for col in range(self.__board.width):
                print('{:>6}'.format(tiles[i]), end='')
                i += 1
            print()

    def _end(self):
        '''
        Calculate final score, save score, play again?
        '''
        pass


if __name__ == '__main__':
    game = Engine()
    game.start()
