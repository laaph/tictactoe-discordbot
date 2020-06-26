import random


class TicTacToe:
    # we should not use string constants but rather enums or something here
    # We will do 0/1 for game status for now, and player turn will be
    # 0 - no game 1 - player 1 turn, 2 - player 2 turn.
    # game_status = 0
    player_turn = 0

    # we don't need ids for the players; however, an array of strings will be nice

    player_names = [None] * 3  # player_name[0] is not used
    # player1id = 0
    # player2id = 0

    board = [None] * 9  # A 9 length array will have the tictactoe board.

    # strange question; should I do AI movement here or externally?

    # answer; we will implement the AI here but expect the client to call the
    # appropriate method when it is the AI's turn.

    def cleanup_game(self):
        player_turn = 0
        player_names = [None] * 3
        board = [None] * 9
        return

    def take_ai_turn(self):
        # This will also imply the caller knows to only call this when it is the AIs turn

        flag = True
        while flag:
            r = random.randint(0, 8)
            if self.board[r] == 0:
                self.board[r] = self.player_turn
                flag = False

        if self.player_turn == 1:
            self.player_turn = 2
        else:
            self.player_turn = 1

        # We could skip the following and assume the caller needs to checkforwin, but
        # it's easy enough to add a return value.

        return self.check_for_win

    def take_turn(self, player_num, location):
        if player_num != self.player_turn:
            return "Wrong player taking turn, or possibly no current game"
        if self.board[location] != 0:
            return "location to be played already occupied"
        self.board[location] = player_num
        if player_num == 2:
            player_num = 1
        else:
            player_num = 2

        return self.check_for_win()


    def game_status_string(self):
        results = {0: "no game", 1: "It is player 1's turn", 2: "It is player 2's turn"}
        return results.get(self.player_turn)

    def game_status(self):
        return self.player_turn

    def check_for_win(self):

        win = 0

        for i in [0, 3, 6]:
            if self.board[i] == self.board[i + 1] and self.board[i] == self.board[i + 2]:
                win = self.board[i]
        for i in [0, 1, 2]:
            if self.board[i] == self.board[i + 3] and self.board[i] == self.board[i + 6]:
                win = self.board[i]

        if self.board[0] == self.board[4] and self.board[0] == self.board[8]:
            print("win for {}".format(self.board[0]))
            win = self.board[0]
        if self.board[2] == self.board[4] and self.board[2] == self.board[6]:
            print("win for {}".format(self.board[2]))
            win = self.board[2]

        if win == 1:
            return 1
        if win == 2:
            return 2

        print("did not return yet, not a win for 1 or 2.")

        # bug we should check for tie game before checking for win.
        tie_game = 3

        for i in range(9):
            if self.board[i] == 0:
                print("not a tie")
                tie_game = 0

        print(tie_game)
        return tie_game

    def new_game(self, p1, p2):

        if random.randint(0, 1) == 1:
            self.player_names[0] = p1
            self.player_names[1] = p2
        else:
            self.player_names[1] = p2
            self.player_names[0] = p1


        for i in range(9):
            self.board[i] = 0

        self.player_turn = 1
