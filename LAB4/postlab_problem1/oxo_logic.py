import os
import random
import oxo_data

class Game:
    def __init__(self):
        self.board = [" "] * 9

    def new_game(self):
        self.board = [" "] * 9

    def save_game(self):
        oxo_data.saveGame(self.board)

    def restore_game(self):
        try:
            game = oxo_data.restoreGame()
            if len(game) == 9:
                self.board = game
            else:
                self.new_game()
        except IOError:
            self.new_game()

    def _generate_move(self):
        options = [i for i, cell in enumerate(self.board) if cell == " "]
        if options:
            return random.choice(options)
        else:
            return -1

    def _is_winning_move(self):
        wins = (
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        )
        for a, b, c in wins:
            chars = self.board[a] + self.board[b] + self.board[c]
            if chars == 'XXX' or chars == 'OOO':
                return True
        return False

    def user_move(self, cell):
        if self.board[cell] != ' ':
            raise ValueError('Invalid cell')
        self.board[cell] = 'X'
        if self._is_winning_move():
            return 'X'
        return ""

    def computer_move(self):
        cell = self._generate_move()
        if cell == -1:
            return 'D'  # Draw
        self.board[cell] = 'O'
        if self._is_winning_move():
            return 'O'
        return ""

def test():
    result = ""
    game = Game()
    game.new_game()
    while not result:
        print(game.board)
        try:
            result = game.user_move(game._generate_move())
        except ValueError:
            print("Oops, that shouldn't happen")
        if not result:
            result = game.computer_move()

        if not result:
            continue
        elif result == 'D':
            print("It's a draw")
        else:
            print("Winner is:", result)
        print(game.board)

if __name__ == "__main__":
    test()
