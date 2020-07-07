import random

import aiohttp
import discord

import tictactoe
import tokeninfo


class MyClient(discord.Client):
    def __init__(self):
        self.tictactoe = tictactoe.TicTacToe()
        self.game_status = "no game"
        self.player_turn = "no game"
        self.player1 = "no game"
        self.player2 = "no game"
        self.player1id = 0
        self.player2id = 0

        self.board_message = 0  # This will hold the message that displays the board
        # and players will react to, to be able to play.

        # python has objc style where you manually call the init method on the parent
        # super.__init() doesn't seem to work, it insists on an argument
        #super.__init__()
        discord.Client.__init__(self)

    music = ["https://www.youtube.com/watch?v=vTIIMJ9tUc8",
             "https://www.youtube.com/watch?v=ib3RcLFAKRQ",
             "https://www.youtube.com/watch?v=fkYBIn9b7oM",
             "https://www.youtube.com/watch?v=wbgbBB98S1c",
             "https://www.youtube.com/watch?v=hHkKJfcBXcw",
             "https://www.youtube.com/watch?v=am2zaeDHpxQ",
             "https://www.youtube.com/watch?v=zpGU355C0ak",
             "https://www.youtube.com/watch?v=ecf4pxeq8CI",
             "https://www.youtube.com/watch?v=lyyoXRPtoB8",
             "https://www.youtube.com/watch?v=DSwoYP90xRE",
             "https://www.youtube.com/watch?v=4GwuMcWfPLY",
             "https://www.youtube.com/watch?v=lSxh-UK7Ays",
             "https://www.youtube.com/watch?v=DM8Tm9ycGz4",
             "https://www.youtube.com/watch?v=cmO6QkJhuu4",
             "https://www.youtube.com/watch?v=chDzjpochB0"]

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        for guild in client.guilds:
            print(
                f'{client.user} is connected to the following guild:\n'
                f'{guild.name}(id: {guild.id})'
            )

    def drawimage(self):
        board_symbols = ["", "", "\n", "", "", "\n", "", "", "\n"]

        tobeshownmessage = ""
        # I have to think about this slowly
        for i in range(9):
            if self.tictactoe.board[i] == 0:
                tobeshownmessage += ":black_square_button: "
            if self.tictactoe.board[i] == 1:
                tobeshownmessage += ":regional_indicator_x: "
            if self.tictactoe.board[i] == 2:
                tobeshownmessage += ":regional_indicator_o: "
            tobeshownmessage += board_symbols[i]

        print(tobeshownmessage)
        return tobeshownmessage

    async def check_for_win(self):

        win = self.tictactoe.check_for_win()

        if win == 1:
            await self.board_message.channel.send("Winner is {}".format(self.player1))
            await self.cleanup_game()
        if win == 2:
            await self.board_message.channel.send("Winner is {}".format(self.player2))
            await self.cleanup_game()

        if win == 3:
            await self.board_message.channel.send("Tie game!")
            await self.cleanup_game()

        if self.player_turn == 0:  # Ai player involved
            await self.take_ai_turn()

    async def cleanup_game(self):
        self.game_status = "no game"
        self.player_turn = "no game"
        self.player1 = "no game"
        self.player2 = "no game"
        self.player1id = 0
        self.player2id = 0
        # self.board_message = 0 We set this below so the following line does not crash

        await self.board_message.channel.send("Cleaning up for next game...")
        self.tictactoe.cleanup_game()
        self.board_message = 0

    async def take_ai_turn(self):

        self.tictactoe.take_ai_turn()

        if self.player1id == 0:
            self.player_turn = self.player2id
        else:
            self.player_turn = self.player1id

        await self.check_for_win()

    async def on_reaction_add(self, reaction, user):
        if self.game_status == "no game":
            print("no game")
            return
        if reaction.message.id != self.board_message.id:
            print("wrong message" + str(reaction.message.id) + " " + str(self.board_message.id))
        if user.id == self.player1id:
            boardtoken = 1
        if user.id == self.player2id:
            boardtoken = 2
        reaction_locations = ["↖️", "⬆️", "↗️", "⬅️", "🔵", "➡️", "↙️", "⬇️", "↘️"]
        a = -1
        try:
            a = reaction_locations.index(reaction.emoji)
        except ValueError:
            await self.board_message.channel.send("That reaction is not used in this game.")
            return

        out = self.tictactoe.take_turn(boardtoken, a)

        #if out > 4:
        await self.board_message.channel.send(out)
        #return // we should probably not mingle strings and ints in the return of take_turn()

        await self.board_message.edit(content=self.drawimage())

        if self.player1id == user.id:
            self.player_turn = self.player2id
        else:
            self.player_turn = self.player1id

        await self.check_for_win()


    async def on_message(self, message):
        if message.author == client.user:
            return

        print('Message from {0.author}: {0.content}'.format(message))

        if message.content.find("!concede") != -1:
            await self.cleanup_game()

        if message.content.find("!status") != -1:
            await message.channel.send("Current status: " + self.game_status)
            if self.game_status != "no game":
                await message.channel.send("It is {}'s turn.".format(self.player_turn))

        if message.content.find("!newgame ai") != -1:
            if self.game_status != "no game":
                await message.channel.send("A game is already happening at " + self.board_message.jump_url)
                return
            m = await message.channel.send("Setting up new game...")

            print(m)

            if random.randint(0, 1) == 1:
                self.player1 = message.author
                self.player2 = "ai"
                self.player1id = message.author.id
                self.player2id = 0
            else:
                self.player1 = "ai"
                self.player2 = message.author
                self.player1id = 0
                self.player2id = message.author.id

            await m.edit(content="New game between {0} and {1} started.".format(self.player1, self.player2))

            self.board_message = m

            self.tictactoe.new_game(self.player1, self.player2)

            await m.edit(content=self.drawimage())

            self.game_status = "game happening at message " + m.jump_url

            self.player_turn = self.player1id
            if self.player_turn == 0:
                await self.take_ai_turn()

            return  # we do not want to be picked up by the below function

        if message.content.find("!newgame") != -1:
            if self.game_status != "no game":
                await message.channel.send("A game is already happening at " + self.board_message.jump_url)
                return
            await message.channel.send("Multiplayer is not yet implemented")

        if message.content.find("!hello") != -1:
            await message.channel.send("Hi")

        if message.content.find("!cat") != -1:
            async with aiohttp.ClientSession() as session:
                async with session.get('http://aws.random.cat/meow') as r:
                    if r.status == 200:
                        js = await r.json()
                        await message.channel.send(js['file'])

        if message.content.find("!music") != -1:
            await message.channel.send(random.choice(self.music))

        if message.content.find("!hyoe") != -1:
            await message.channel.send(random.choice(self.music))

        if message.content.find("!quit") != -1:
            await message.channel.send("Bot shutting down now...")
            await self.close()

        if message.content.find("!help") != -1:
            await message.channel.send(
                "Available commands:\n" +
                "!status               Show current game status\n" +
                "!howtoplay            How to play\n" +
                "!newgame ai           New game against bot\n" +
                "!newgame              New game against the next player who wants to play\n" +
                "!newgame <playerid>   New game against <playerid>\n" +
                "!concede              Concede the game\n")


if __name__ == '__main__':
    client = MyClient()
    client.run(tokeninfo.token)
