import random

import aiohttp
import discord


class MyClient(discord.Client):
    
    gamestatus = "no game"
    playerturn = "no game"
    player1    = "no game"
    player2    = "no game"
    player1id  = 0
    player2id  = 0
    
    board = [None] * 9 # A 9 length array will have the tictactoe board.
    
    boardmessage = 0  # This will hold the message that displays the board
                        # and players will react to, to be able to play.
    
    music = ["https://www.youtube.com/watch?v=vTIIMJ9tUc8",
             "https://www.youtube.com/watch?v=ib3RcLFAKRQ",
             "https://www.youtube.com/watch?v=hHkKJfcBXcw",
             "https://www.youtube.com/watch?v=p1lGR0LC_2s",
             "https://www.youtube.com/watch?v=zLZKuAY2tkc",
             "https://www.youtube.com/watch?v=zpGU355C0ak",
             "https://www.youtube.com/watch?v=s6E3xVz01bw",
             "https://www.youtube.com/watch?v=4GwuMcWfPLY",
             "https://youtu.be/gMkrvTraVZ0",
             "http://youtu.be/lSxh-UK7Ays",
             "https://www.youtube.com/watch?v=chDzjpochB0"]

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    def drawimage(self):
        boardsymbols = ["", "", "\n", "", "", "\n", "", "", "\n"]
            #boardsymbols = ["⬛", "⬛", "\n", "⬛", "⬛", "\n", "⬛", "⬛", "\n"]
        
        tobeshownmessage = ""
        # I have to think about this slowly
        for i in range(9):
            if(self.board[i] == 0):
                tobeshownmessage += ":black_square_button: "
            if(self.board[i] == 1):
                tobeshownmessage += ":regional_indicator_x: "
            if(self.board[i] == 2):
                tobeshownmessage += ":regional_indicator_o: "
            tobeshownmessage += boardsymbols[i]
            
#            if(i == 2 or i == 5):
#                tobeshownmessage += "⬛⬛⬛⬛⬛\n"

        print(tobeshownmessage)
        return tobeshownmessage

    async def checkforwin(self):

        win = 0
        
        for i in [0,3,6]:
            if(self.board[i] == self.board[i+1] and self.board[i] == self.board[i+2]):
                win = self.board[i]
        for i in [0,1,2]:
            if(self.board[i] == self.board[i+3] and self.board[i] == self.board[i+6]):
                win = self.board[i]
     
        if(self.board[0] == self.board[4] and self.board[0] == self.board[8]):
            print("win for {}".format(self.board[0]))
            win = self.board[0]
        if(self.board[2] == self.board[4] and self.board[2] == self.board[6]):
            print("win for {}".format(self.board[2]))
            win = self.board[2]

        if(win == 1):
            await self.boardmessage.channel.send("Winner is {}".format(self.player1))
            await self.cleanup_game()
        if(win == 2):
            await self.boardmessage.channel.send("Winner is {}".format(self.player2))
            await self.cleanup_game()

        tiegame = 1

        for i in range(9):
            if(self.board[i] == 0):
                tiegame = 0

        if(tiegame):
            await self.boardmessage.channel.send("Tie game!")
            await self.cleanup_game()

        if(self.playerturn == 0): # Ai player involved
                await self.take_ai_turn()

    async def cleanup_game(self):
        await self.boardmessage.channel.send("Cleaning up for next game...")
        self.gamestatus = "no game"
        self.playerturn = "no game"
        self.player1    = "no game"
        self.player2    = "no game"
        self.player1id  = 0
        self.player2id  = 0
        self.board = [None] * 9
        self.boardmessage = 0
        
    async def take_ai_turn(self):
        if(self.player1id == 0):
            boardtoken = 1
        if(self.player2id == 0):
            boardtoken = 2

        flag = True
        while(flag):
            r = random.randint(0, 8)
            if(self.board[r] == 0):
                self.board[r] = boardtoken
                flag = False
                await self.boardmessage.edit(content=self.drawimage())
        
        if(self.player1id == 0):
            self.playerturn = self.player2id
        else:
            self.playerturn = self.player1id
        
        await self.checkforwin()

    async def on_reaction_add(self, reaction, user):
        if(self.gamestatus == "no game"):
            print("no game")
            return
        if(reaction.message.id != self.boardmessage.id):
            print("wrong message" + str(reaction.message.id) + " " + str(self.boardmessage.id))
        if(user.id == self.player1id):
            boardtoken = 1
        if(user.id == self.player2id):
            boardtoken = 2
        reaction_locations = ["↖", "⬆", "↗", "⬅", "🔵", "➡", "↙", "⬇", "↘"]
        a = -1
        try:
            a = reaction_locations.index(reaction.emoji)
        except ValueError:
            print("ValueError: " + ValueError)
            return

        if(self.board[a] == 0):
            self.board[a] = boardtoken
        else:
            await self.boardmessage.channel.send("You can not play there since there is already a symbol in that position.")
            return

        await self.boardmessage.edit(content=self.drawimage())

        if(self.player1id == user.id):
            self.playerturn = self.player2id
        else:
            self.playerturn = self.player1id

        await self.checkforwin()
        

        
    async def on_message(self, message):
        if(message.author == client.user):
            return

        print('Message from {0.author}: {0.content}'.format(message))
        
        if message.content.find("!concede") != -1:
            await self.cleanup_game()

        if message.content.find("!status") != -1:
            await message.channel.send("Current status: " + self.gamestatus)
            if(self.gamestatus != "no game"):
                await message.channel.send("It is {}'s turn.".format(self.playerturn))
    
        if message.content.find("!newgame ai") != -1:
            if(self.gamestatus != "no game"):
                await message.channel.send("A game is already happening at " + self.boardmessage.jump_url)
                return
            m = await message.channel.send("Setting up new game...")
            
            print(m)
            
            if(random.randint(0,1) == 1):
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
        
            self.boardmessage = m
            for i in range(9):
                self.board[i] = 0

            await m.edit(content=self.drawimage())
            
            self.gamestatus = "game happenening at message " + m.jump_url
            
            self.playerturn = self.player1id
            if(self.playerturn == 0):
                await self.take_ai_turn()
                    
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
            await message.channel.send(\
                "Available commands:\n" +\
                "!status               Show current game status\n" +\
                "!howtoplay            How to play\n" +\
                "!newgame ai           New game against bot\n" +\
                "!newgame              New game against the next player who wants to play\n" +\
                "!newgame <playerid>   New game against <playerid>\n" +\
                "!concede              Concede the game\n")

client = MyClient()
client.run('-add your own token here-')

