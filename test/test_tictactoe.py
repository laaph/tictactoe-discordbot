import pytest

import random  # because let's test things at random

import tictactoe


# Because we do not have a setup.py, you will have to either set the
# sys.path variable (via PYTHONPATH) or python -m pytest test/test_tictactoe.py

def test_tictactoe():
    tic = tictactoe.TicTacToe()
    assert tic.board[random.randint(0, 8)] is None
    assert tic.player_turn == 0
    assert type(tic.player_names) == list
    assert type(tic.board) == list


def test_taketurnandverifyturnchange():
    tic = tictactoe.TicTacToe()
    tic.new_game("player1", "player2")
    tic.take_turn(1, 0)

    assert tic.board[0] == 1
    assert tic.player_turn == 2

# @pytest.patch('random')
# def test_turn(random):
