import pytest

import random  # because let's test things at random

import tictactoe

def test_tictactoe():
	tic = tictactoe.TicTacToe()
	assert tic.board[random.randint(0, 8)] is None
	assert tic.player_turn == 0
	assert type(tic.player_names) == list
	assert type(tic.board) == list

def test_taketurnandverifyturnchange():
	tic = tictactoe.TicTacToe()
	tic.new_game("player1", "player2")
	tic.take_ai_turn()

	assert tic.player_turn == 2

# @pytest.patch('random')
# def test_turn(random):
