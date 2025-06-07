import unittest
from oxo_logic import Game

class TestTicTacToe(unittest.TestCase):
    def test_user_move_valid(self):
        game = Game()
        result = game.user_move(0)
        self.assertEqual(result, "")
        self.assertEqual(game.get_board()[0], 'X')

    def test_user_move_invalid(self):
        game = Game()
        game.user_move(0)
        with self.assertRaises(ValueError):
            game.user_move(0)

    def test_is_winning_move(self):
        game = Game()
        game.board = ['X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ']
        self.assertTrue(game._is_winning_move())

    def test_draw(self):
        game = Game()
        game.board = ['X', 'O', 'X', 'X', 'O', 'O', 'O', 'X', 'X']
        result = game.computer_move()
        self.assertEqual(result, 'D')

if __name__ == '__main__':
    unittest.main()
