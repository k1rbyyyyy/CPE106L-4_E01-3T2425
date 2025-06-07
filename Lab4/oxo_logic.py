import os, random
import oxo_data

class Game:
    def __init__(self):
        self.board = [" "] * 9
        self.result = ""

    def new_game(self):
        self.board = [" "] * 9
        self.result = ""

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
        options = [i for i in range(len(self.board)) if self.board[i] == " "]
        return random.choice(options) if options else -1

    def _is_winning_move(self):
        wins = ((0,1,2), (3,4,5), (6,7,8),
                (0,3,6), (1,4,7), (2,5,8),
                (0,4,8), (2,4,6))
        for a,b,c in wins:
            chars = self.board[a] + self.board[b] + self.board[c]
            if chars == 'XXX' or chars == 'OOO':
                return True
        return False

    def user_move(self, cell):
        if self.board[cell] != ' ':
            raise ValueError("Invalid cell")
        self.board[cell] = 'X'
        if self._is_winning_move():
            self.result = 'X'
        return self.result

    def computer_move(self):
        cell = self._generate_move()
        if cell == -1:
            self.result = 'D'
            return self.result
        self.board[cell] = 'O'
        if self._is_winning_move():
            self.result = 'O'
        return self.result

    def get_board(self):
        return self.board

if __name__ == "__main__":
    game = Game()
    while not game.result:
        print(game.get_board())
        try:
            game.user_move(game._generate_move())
        except ValueError:
            print("Oops, that shouldn't happen")
        if not game.result:
            game.computer_move()
        if game.result:
            if game.result == 'D':
                print("It's a draw")
            else:
                print("Winner is:", game.result)
            print(game.get_board())
