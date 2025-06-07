''' oxo_data is the data module for a tic-tac-toe (or OXO) game. 
    It saves and restores a game board. The functions are:
         saveGame(game) -> None
         restoreGame() -> game
    Note that no limits are placed on the size of the data.
    The game implementation is responsible for validating
    all data in and out.'''

import os
import pickle

filename = "game.dat"

def saveGame(game):
    """Save the game board (list of 9 strings) to a file."""
    with open(filename, "wb") as f:
        pickle.dump(game, f)

def restoreGame():
    """Load the game board from the file and return it."""
    with open(filename, "rb") as f:
        return pickle.load(f)
