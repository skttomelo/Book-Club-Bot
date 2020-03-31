  
from dotenv import load_dotenv
from pathlib import Path
from data import Form
import os
import discord

# get env
env_path = Path('.') / 'config.env'
load_dotenv(dotenv_path=env_path)

forms = {}
inprogress = {}

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves but we do need to know where are in the form
        if message.author == self.user:
            return
        if message.content == '!vote':
            await self.vote(message)
            return
        await self.form_fill_out(message)

    async def vote(self, message):
        # if sender has never created a form
        if message.author.id not in forms:
            temp = {message.author.id: [Form(message.author.id)]}
            temp2 = {message.author.id: False} # the 0 represents the form that will need to be filled out
            forms.update(temp)
            inprogress.update(temp2)

        # if the sender already has a form going
        if inprogress[message.author.id] == True:
            await message.author.send('You already have a vote form in progress. Please finish it or cancel it by sending the :x: emoji.')
            return
        
        inprogress[message.author.id] = True
        await message.author.send("Let's begin :smile:\nIf at any point you would like to cancel the form, please send the :x: emoji.")

        # grab the form that is incomplete and continue off point that hasn't been filled out
        for form in forms:
            for array in forms[form]:
                if array.completed == True:
                    continue
                for info in array.story_details:
                    if array.story_details[info] == '':
                        await message.author.send(f'Story {info.title()} (if this doesn\'t exist, please message a :no_entry_sign: emoji):')
                        break

    
    # handles where the sender is in the form process as well as cancelling form if user wants that
    async def form_fill_out(self, message):
        
        if await self.dm_chat(message):
            # grab most recent message from user and bot
            history = await message.channel.history(limit=2).flatten()

            if history[0].author == self.user:
                return

            # if the user responds with an x emoji we cancel the form... eventually when I add that in
            if history[0].content == ':x:':
                return
            
            # if it's from the user then we want to store that answer
            # after that we want to ask the next question if there exist one
            # otherwise we mark the form as completed and mark inprogress as false
            loc = 0
            for form in forms:
                for (i, array) in enumerate(forms[form]):
                    if array.completed == True:
                        continue
                    loc = i
                    for info in array.story_details:
                        if array.story_details[info] == '':
                            pass  
                                
    async def dm_chat(self, message):
        return isinstance(message.channel, discord.DMChannel)
            
            
        



client = MyClient()

client.run(os.getenv('token'))
