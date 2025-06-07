import unittest
from oxo_logic import Game

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_initial_board_empty(self):
        self.assertEqual(self.game.board, [' '] * 9)

    def test_make_move(self):
        self.assertTrue(self.game.make_move(0))
        self.assertEqual(self.game.board[0], 'X')
        self.assertFalse(self.game.make_move(0))

    def test_switch_player(self):
        self.assertEqual(self.game.current_player, 'X')
        self.game.switch_player()
        self.assertEqual(self.game.current_player, 'O')

    def test_check_winner(self):
        self.game.board = ['X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ']
        self.assertEqual(self.game.check_winner(), 'X')
        self.game.board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.assertIsNone(self.game.check_winner())

    def test_is_full(self):
        self.game.board = ['X', 'O', 'X', 'O', 'X', 'O', 'O', 'X', 'X']
        self.assertTrue(self.game.is_full())
        self.game.board[0] = ' '
        self.assertFalse(self.game.is_full())

if __name__ == "__main__":
    unittest.main()
