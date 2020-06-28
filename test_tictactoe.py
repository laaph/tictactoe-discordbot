import pytest

import tictactoe


def test_tictactoe():
    # arrange
    board = tictactoe.TicTacToe()
    # act
    # assert
    assert board.player_turn == 0
    assert type(board.player_names) == list
    assert type(board.board) == list


def test_turn():
    # TODO: test bad position or player id
    # arrange
    board = tictactoe.TicTacToe()
    p1 = 'p1'
    p2 = 'p2'
    board.new_game(p1, p2)
    # act
    board.take_turn(player=1, location=0)
    # assert
    assert board.board[0] == 1
    assert board.player_turn == 2
